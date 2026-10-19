### Investigate

Investigation requests are read-only and asked in context of existing code and/or systems. They produce a cited explanation or a recommendation, not a code change.

1. Route through the **how** skill.
2. Produce the `how`-shaped output (Overview / Key Concepts / How It Works / Where Things Live / Gotchas), or a recommendation with a tradeoffs table if the request is a decision between alternatives.
3. Apply the **unslop** skill to the reply.

No PR, only response output unless the investigation precedes a code change. If it does, provide **Reply** reponse, and hand back to the user and suggest appropriate action (eg Bugfix, new Feature).

**Reply:** the investigation output. For "are we sure?" answers, include your real judgment with reasons. Push back if the premise is wrong (see Autonomy).
