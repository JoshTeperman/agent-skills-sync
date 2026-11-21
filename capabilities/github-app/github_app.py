#!/usr/bin/env python3
"""Act on GitHub as the GitHub App's bot, with a short-lived token scoped to one repository.

Tokens come from gh-token-service on the tailnet. Nothing is configured on the machine:
every call passes the repository, the permissions and who is asking.

  github-app gh    --repository OWNER/NAME (--permission-profile read|write | --permissions JSON)
                   --agent-name NAME [--agent-provider P] [--agent-model M] [--purpose TEXT] -- <gh args>
  github-app git   <same options> -- <git args>
  github-app token <same options>            print a token on stdout
  github-app credential get                  internal: git's credential helper

Service URL: $GITHUB_TOKEN_SERVICE_URL, else skills/github-app/.env, else
https://vps.<this machine's MagicDNS suffix>/github-token.
"""

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

PROFILES = {
    "read": {"contents": "read", "pull_requests": "read", "issues": "read", "metadata": "read"},
    "write": {"contents": "write", "pull_requests": "write", "issues": "write", "metadata": "read"},
}
SERVICE_HOST = "vps"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "gh-token-service")
REUSE_MARGIN_SECONDS = 5 * 60
NAME = re.compile(r"^[A-Za-z0-9._-]{1,100}$")
SKILL_ENV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
    "skills", "github-app", ".env",
)


class Fail(Exception):
    pass


def main(argv):
    if argv and argv[0] == "credential":
        return credential(argv[1:])
    if not argv or argv[0] not in ("gh", "git", "token"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    command, rest = argv[0], argv[1:]
    passthrough = []
    if "--" in rest:
        i = rest.index("--")
        rest, passthrough = rest[:i], rest[i + 1:]
    opts = parse_options(command, rest)
    if command in ("gh", "git") and not passthrough:
        fail(f"give the {command} arguments after --, e.g. github-app {command} ... -- "
             + ("pr list" if command == "gh" else "push origin HEAD"))
    if command == "token" and passthrough:
        fail("token takes no arguments after --")

    grant = get_token(opts["owner"], opts["name"], opts["permissions"], opts["agent"])
    if command == "token":
        print(grant["token"])
        return 0
    if command == "gh":
        env = dict(os.environ, GH_TOKEN=grant["token"])
        env.pop("GITHUB_TOKEN", None)
        return run(["gh"] + passthrough, env)
    return run(git_command(passthrough), git_env(opts, grant))


def parse_options(command, args):
    p = argparse.ArgumentParser(prog=f"github-app {command}", allow_abbrev=False)
    p.add_argument("--repository", required=True, metavar="OWNER/NAME")
    perm = p.add_mutually_exclusive_group(required=True)
    perm.add_argument("--permission-profile", choices=sorted(PROFILES))
    perm.add_argument("--permissions", metavar="JSON", help='e.g. \'{"contents":"read","checks":"read"}\'')
    p.add_argument("--agent-name")
    p.add_argument("--agent-provider")
    p.add_argument("--agent-model")
    p.add_argument("--purpose")
    a = p.parse_args(args)

    parts = a.repository.split("/")
    if len(parts) != 2 or not all(NAME.match(x) for x in parts):
        p.error("--repository must be OWNER/NAME, e.g. JoshTeperman/agent-skills-sync")
    if a.permission_profile:
        permissions = dict(PROFILES[a.permission_profile])
    else:
        try:
            permissions = json.loads(a.permissions)
        except json.JSONDecodeError:
            p.error("--permissions must be a JSON object")
        if not isinstance(permissions, dict) or not permissions or not all(
            isinstance(k, str) and v in ("read", "write") for k, v in permissions.items()
        ):
            p.error('--permissions must be a non-empty JSON object of "read" or "write" values')

    agent = {
        "name": a.agent_name or os.environ.get("AGENT_NAME"),
        "provider": a.agent_provider or os.environ.get("AGENT_PROVIDER"),
        "model": a.agent_model or os.environ.get("AGENT_MODEL"),
        "purpose": a.purpose or os.environ.get("AGENT_PURPOSE"),
    }
    if not agent["name"]:
        p.error("--agent-name is required (or set AGENT_NAME)")
    return {"owner": parts[0], "name": parts[1], "repository": a.repository,
            "permissions": permissions, "agent": agent}


def git_command(args):
    me = shlex.quote(os.path.abspath(sys.argv[0]))
    return ["git",
            "-c", "credential.helper=",
            "-c", f"credential.helper=!{me} credential",
            "-c", "credential.useHttpPath=true"] + args


def git_env(opts, grant):
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": grant["bot_name"],
        "GIT_COMMITTER_NAME": grant["bot_name"],
        "GIT_AUTHOR_EMAIL": grant["bot_email"],
        "GIT_COMMITTER_EMAIL": grant["bot_email"],
        "GITHUB_APP_REPOSITORY": opts["repository"],
        "GITHUB_APP_PERMISSIONS": json.dumps(opts["permissions"], sort_keys=True),
        "GIT_TERMINAL_PROMPT": "0",
    })
    for key, value in opts["agent"].items():
        if value:
            env["AGENT_" + key.upper()] = value
    return env


def run(cmd, env):
    if shutil.which(cmd[0]) is None:
        fail(f"{cmd[0]} is not installed")
    try:
        return subprocess.run(cmd, env=env).returncode
    except KeyboardInterrupt:
        return 130


def credential(args):
    request = {}
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            break
        key, _, value = line.partition("=")
        request[key] = value
    if not args or args[0] != "get":
        return 0

    repository = os.environ.get("GITHUB_APP_REPOSITORY", "")
    path = request.get("path", "").strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    if (request.get("protocol") != "https" or request.get("host", "").lower() != "github.com"
            or not repository or path.lower() != repository.lower()):
        print("quit=true")
        return 0
    try:
        permissions = json.loads(os.environ["GITHUB_APP_PERMISSIONS"])
        owner, name = repository.split("/")
        agent = {k: os.environ.get("AGENT_" + k.upper()) for k in ("name", "provider", "model", "purpose")}
        if not agent["name"]:
            raise Fail("AGENT_NAME is not set")
        grant = get_token(owner, name, permissions, agent)
    except (Fail, KeyError, ValueError) as e:
        print(f"github-app: {e}", file=sys.stderr)
        print("quit=true")
        return 0
    print("username=x-access-token")
    print(f"password={grant['token']}")
    return 0


def get_token(owner, name, permissions, agent):
    key = json.dumps([owner.lower(), [name.lower()], permissions], sort_keys=True)
    cache_file = os.path.join(CACHE_DIR, hashlib.sha256(key.encode()).hexdigest() + ".json")
    cached = read_cache(cache_file)
    if cached:
        return cached

    url = service_url().rstrip("/") + "/token"
    body = json.dumps({"owner": owner, "repositories": [name], "permissions": permissions}).encode()
    headers = {"Content-Type": "application/json", "X-Agent-Name": agent["name"]}
    for field, header in (("provider", "X-Agent-Provider"), ("model", "X-Agent-Model"), ("purpose", "X-Agent-Purpose")):
        if agent.get(field):
            headers[header] = agent[field]
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            grant = json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            detail = json.load(e)
            msg = f"{detail.get('error', e.reason)} (request_id {detail.get('request_id', '?')})"
        except ValueError:
            msg = str(e.reason)
        raise Fail(f"token service returned {e.code}: {msg}")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        reason = getattr(e, "reason", e)
        raise Fail(f"token service unreachable at {url}: {reason}")
    if not all(grant.get(k) for k in ("token", "expires_at", "bot_name", "bot_email")):
        raise Fail("token service response is missing fields")
    write_cache(cache_file, grant)
    return grant


def read_cache(path):
    try:
        with open(path) as f:
            grant = json.load(f)
        expires = datetime.fromisoformat(grant["expires_at"].replace("Z", "+00:00"))
    except (OSError, ValueError, KeyError):
        return None
    if expires.timestamp() - time.time() <= REUSE_MARGIN_SECONDS:
        return None
    return grant


def write_cache(path, grant):
    os.makedirs(CACHE_DIR, mode=0o700, exist_ok=True)
    os.chmod(CACHE_DIR, 0o700)
    keep = {k: grant[k] for k in ("token", "expires_at", "bot_name", "bot_email", "permissions", "repositories") if k in grant}
    fd, tmp = tempfile.mkstemp(dir=CACHE_DIR, prefix=".tmp-")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(keep, f)
        os.replace(tmp, path)
    except OSError:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def service_url():
    url = os.environ.get("GITHUB_TOKEN_SERVICE_URL") or dotenv(SKILL_ENV).get("GITHUB_TOKEN_SERVICE_URL")
    if url:
        return url
    suffix = magic_dns_suffix()
    if not suffix:
        raise Fail("can't find the tailnet: tailscale isn't running or its CLI isn't installed. "
                   "Set GITHUB_TOKEN_SERVICE_URL, or tell the user.")
    return f"https://{SERVICE_HOST}.{suffix}/github-token"


def magic_dns_suffix():
    for cli in ("tailscale", "/Applications/Tailscale.app/Contents/MacOS/Tailscale"):
        exe = shutil.which(cli) or (cli if os.path.isfile(cli) else None)
        if not exe:
            continue
        try:
            out = subprocess.run([exe, "status", "--json"], capture_output=True, timeout=10, check=True).stdout
            status = json.loads(out)
        except (OSError, subprocess.SubprocessError, ValueError):
            continue
        suffix = status.get("MagicDNSSuffix") or (status.get("CurrentTailnet") or {}).get("MagicDNSSuffix")
        if suffix:
            return suffix.strip(".")
    return None


def dotenv(path):
    values = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    values[k.strip()] = v.strip().strip("'\"")
    except OSError:
        pass
    return values


def fail(msg):
    raise Fail(msg)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Fail as e:
        print(f"github-app: error: {e}", file=sys.stderr)
        print("github-app: stop and tell the user; don't fall back to other GitHub credentials.", file=sys.stderr)
        sys.exit(1)
