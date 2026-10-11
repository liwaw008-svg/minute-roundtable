# Minute Roundtable

Minute Roundtable turns several human-written accounts of one meeting into a bounded, attributable decision record. A chair enters the agenda and three to five minute books directly; no hosted fixture or GitHub URL is required.

## Real workflow

1. `convene(meeting_id, title, agenda_json, minutes_json, quorum)` creates an immutable `SEATED` meeting and rejects reused IDs or identical records.
2. `reconcile(meeting_id)` asks GenLayer validators to compare the books semantically.
3. Deterministic checks require every agenda item exactly once, declared decision codes only, valid source indexes, and quorum before `AGREED`.
4. The terminal `MINUTED` record exposes agreed, disputed, and omitted items with exact source attribution.

The frontend guides a normal person through naming the meeting, setting two agenda questions, writing three minute books, creating the on-chain meeting, and running consensus.

## Verify

```text
python -m pytest -q
genvm-lint contracts/contract.py
```

## Public artifacts

- Site: https://minute-roundtable.pages.dev/
- Repository: https://github.com/liwaw008-svg/minute-roundtable
- Contract: https://explorer-studio.genlayer.com/address/0x9761dEdc56Ca8bd18Cc091ED282E4BE231F3ec2D
- Network: StudioNet

