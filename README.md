# Minute Roundtable

Minute Roundtable is a GenLayer quorum-intersection primitive for independently published meeting minutes. A docket fixes the agenda, three to six minutes sources, ordered agenda IDs, and an explicit quorum. Validators refetch every source and produce a complete decision vector with exact support and dissent indexes.

## Why consensus is necessary

Different note-takers describe the same decision in different language. Semantic comparison finds the intersection; deterministic guards ensure no agenda item disappears, every source index is valid, and `AGREED` is impossible without the frozen quorum.

## Lifecycle

1. `convene(manifest_url)` freezes the docket, agenda, all minutes, and ordered content digests as `SEATED`.
2. `reconcile(docket_id)` refetches every frozen byte and classifies each agenda item as `AGREED`, `DISPUTED`, or `OMITTED`.
3. The terminal `MINUTED` record exposes canonical decisions, disputed IDs, omitted IDs, and exact source attribution.

## Verify

```text
python -m pytest -q
genvm-lint contracts/contract.py
```

## Public artifacts

- Site: https://minute-roundtable.pages.dev/
- Repository: https://github.com/liwaw008-svg/minute-roundtable
- Network: StudioNet
