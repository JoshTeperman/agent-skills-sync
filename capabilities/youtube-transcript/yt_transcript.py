#!/usr/bin/env python3
"""Fetch a YouTube transcript from captions, without YouTube-specific libraries.

Uses the undocumented Innertube player API to list caption tracks, then
downloads timed text as json3 (falling back to srv3 XML). Stdlib only.

Exit codes: 0 ok, 1 other error, 2 usage or bad URL, 3 no captions in the
requested language, 4 rate-limited or bot-checked by YouTube.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape

PLAYER_URL = "https://www.youtube.com/youtubei/v1/player"

# Client versions taken from yt-dlp 2026.10.26. ANDROID is tried first because
# the WEB player response often omits captionTracks unless a PO token is present.
CLIENTS = (
    {
        "name": "ANDROID",
        "context": {
            "clientName": "ANDROID",
            "clientVersion": "21.26.364",
        },
        "user_agent": "com.google.android.youtube/21.26.364 (Linux; U; Android 11) gzip",
    },
    {
        "name": "WEB",
        "context": {
            "clientName": "WEB",
            "clientVersion": "2.20260708.00.00",
        },
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    },
)

VIDEO_ID_RE = re.compile(
    r"(?:youtu\.be/|youtube\.com/(?:watch\?.*v=|embed/|shorts/|live/|v/))([A-Za-z0-9_-]{11})"
)


class TranscriptError(Exception):
    exit_code = 1


class UsageError(TranscriptError):
    exit_code = 2


class NoCaptionsError(TranscriptError):
    exit_code = 3


class BlockedError(TranscriptError):
    exit_code = 4


def extract_video_id(url_or_id: str) -> str:
    value = url_or_id.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value
    match = VIDEO_ID_RE.search(value)
    if match:
        return match.group(1)
    parsed = urllib.parse.urlparse(value)
    query_id = urllib.parse.parse_qs(parsed.query).get("v", [None])[0]
    if query_id and re.fullmatch(r"[A-Za-z0-9_-]{11}", query_id):
        return query_id
    raise UsageError(f"Could not parse a YouTube video id from: {url_or_id}")


def http_request(url: str, *, data: bytes | None = None, headers: dict[str, str]) -> bytes:
    request = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read()
        snippet = body[:300].decode("utf-8", errors="replace")
        if exc.code == 429:
            raise BlockedError(f"HTTP 429 rate-limited by {urllib.parse.urlsplit(url).path}") from exc
        raise TranscriptError(f"HTTP {exc.code} for {url}: {snippet}") from exc
    except urllib.error.URLError as exc:
        raise TranscriptError(f"Network error for {url}: {exc}") from exc


def fetch_player(video_id: str, client: dict) -> dict:
    payload = {
        "context": {"client": client["context"]},
        "videoId": video_id,
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": client["user_agent"],
        "Accept": "application/json",
    }
    raw = http_request(PLAYER_URL, data=json.dumps(payload).encode(), headers=headers)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TranscriptError(f"Invalid player JSON from {client['name']}: {exc}") from exc


def caption_tracks(player: dict) -> list[dict]:
    tracks = (
        player.get("captions", {})
        .get("playerCaptionsTracklistRenderer", {})
        .get("captionTracks")
        or []
    )
    return [track for track in tracks if track.get("baseUrl")]


def select_track(tracks: list[dict], lang: str) -> dict:
    lang = lang.lower()

    def language_code(track: dict) -> str:
        return (track.get("languageCode") or "").lower()

    def is_generated(track: dict) -> bool:
        return track.get("kind") == "asr"

    def matches(track: dict) -> bool:
        code = language_code(track)
        return code == lang or code.startswith(lang + "-") or code.startswith(lang)

    # Prefer an exact language match, manual captions before auto-generated.
    ranked = [t for t in tracks if matches(t) and not is_generated(t)]
    ranked += [t for t in tracks if matches(t) and is_generated(t)]
    if ranked:
        return ranked[0]
    available = ", ".join(
        f"{language_code(t) or '?'}{' (auto)' if is_generated(t) else ''}" for t in tracks
    )
    raise NoCaptionsError(f"No {lang} caption track found. Available: {available or 'none'}")


def with_fmt(url: str, fmt: str) -> str:
    parts = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
    query = [(key, value) for key, value in query if key != "fmt"]
    query.append(("fmt", fmt))
    return urllib.parse.urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urllib.parse.urlencode(query), parts.fragment)
    )


def clean_caption_text(text: str) -> str:
    text = unescape(text).replace("\xa0", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()


def parse_json3(raw: bytes) -> list[dict]:
    data = json.loads(raw)
    segments = []
    for event in data.get("events") or []:
        segs = event.get("segs") or []
        text = clean_caption_text("".join(part.get("utf8") or "" for part in segs))
        if not text:
            continue
        segments.append(
            {
                "start_ms": int(event.get("tStartMs") or 0),
                "duration_ms": int(event.get("dDurationMs") or 0),
                "text": text,
            }
        )
    return segments


def parse_srv3(raw: bytes) -> list[dict]:
    root = ET.fromstring(raw)
    segments = []
    for node in root.iter():
        tag = node.tag.lower().rsplit("}", 1)[-1]
        if tag not in {"p", "text"}:
            continue
        text = clean_caption_text("".join(node.itertext()))
        if not text:
            continue
        start = node.get("t") or node.get("start") or "0"
        duration = node.get("d") or node.get("dur") or "0"
        # srv3 uses milliseconds in t/d; the older srv1 XML uses seconds in start/dur.
        start_val = float(start)
        duration_val = float(duration)
        if tag == "text" and "start" in node.attrib:
            start_ms = int(start_val * 1000)
            duration_ms = int(duration_val * 1000)
        else:
            start_ms = int(start_val)
            duration_ms = int(duration_val)
        segments.append({"start_ms": start_ms, "duration_ms": duration_ms, "text": text})
    return segments


def download_segments(track: dict, user_agent: str) -> list[dict]:
    headers = {"User-Agent": user_agent, "Accept": "*/*"}
    last_error = None
    for fmt, parser in (("json3", parse_json3), ("srv3", parse_srv3)):
        url = with_fmt(track["baseUrl"], fmt)
        try:
            raw = http_request(url, headers=headers)
            segments = parser(raw)
        except BlockedError:
            raise
        except (TranscriptError, json.JSONDecodeError, ET.ParseError) as exc:
            last_error = exc
            continue
        if segments:
            return segments
    raise TranscriptError(f"Could not parse caption track: {last_error}")


def format_timestamp(start_ms: int) -> str:
    seconds, millis = divmod(max(start_ms, 0), 1000)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}.{millis:03d}"
    return f"{minutes}:{seconds:02d}.{millis:03d}"


def render(segments: list[dict], timestamps: bool) -> str:
    if timestamps:
        lines = [f"[{format_timestamp(s['start_ms'])}] {s['text']}" for s in segments]
        return "\n".join(lines) + ("\n" if lines else "")
    return clean_caption_text(" ".join(s["text"] for s in segments)) + ("\n" if segments else "")


def fetch_transcript(video_id: str, lang: str) -> tuple[list[dict], dict, str]:
    errors = []
    blocked = False
    for client in CLIENTS:
        try:
            player = fetch_player(video_id, client)
        except TranscriptError as exc:
            blocked = blocked or isinstance(exc, BlockedError)
            errors.append(f"{client['name']} player: {exc}")
            continue
        status = (player.get("playabilityStatus") or {}).get("status")
        tracks = caption_tracks(player)
        if not tracks:
            reason = (player.get("playabilityStatus") or {}).get("reason") or status or "no tracks"
            blocked = blocked or "not a bot" in reason.lower()
            errors.append(f"{client['name']}: {reason}")
            continue
        track = select_track(tracks, lang)
        segments = download_segments(track, client["user_agent"])
        meta = {
            "client": client["name"],
            "language": track.get("languageCode"),
            "generated": track.get("kind") == "asr",
            "playability": status,
            "track_count": len(tracks),
        }
        return segments, meta, client["name"]
    detail = "All Innertube clients failed: " + " | ".join(errors)
    if blocked:
        raise BlockedError(detail)
    raise NoCaptionsError(detail)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a YouTube caption transcript as plain text.")
    parser.add_argument("url_or_id", help="YouTube URL or 11-character video id")
    parser.add_argument("--lang", default="en", help="Caption language code (default: en)")
    parser.add_argument("--timestamps", action="store_true", help="Prefix each cue with its start time")
    parser.add_argument("--json", action="store_true", help="Print JSON with metadata and timed segments")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        video_id = extract_video_id(args.url_or_id)
        segments, meta, _client = fetch_transcript(video_id, args.lang)
    except TranscriptError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return exc.exit_code
    if args.json:
        payload = {
            "video_id": video_id,
            "language": meta["language"],
            "generated": meta["generated"],
            "segments": segments,
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return 0
    sys.stdout.write(render(segments, args.timestamps))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
