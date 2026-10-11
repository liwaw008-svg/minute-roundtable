from pathlib import Path
SRC = (Path(__file__).parents[1] / "contracts" / "contract.py").read_text(encoding="utf-8")

def test_distinct_lifecycle():
    for token in ('def convene(', 'def reconcile(', 'def get_docket(', '"SEATED"', '"MINUTED"'):
        assert token in SRC

def test_all_records_are_refetched_and_digest_bound():
    assert SRC.count("gl.nondet.web.get") >= 4
    assert 'for index, source_url in enumerate([manifest["agenda_url"]] + manifest["minute_urls"])' in SRC
    for token in ("manifest_digest", "record_digests", "frozen docket changed", "frozen meeting record changed"):
        assert token in SRC

def test_quorum_and_complete_agenda_are_enforced():
    for token in ("complete agenda vector required", "agreed decision lacks quorum", 'len(support) < manifest["quorum"]'):
        assert token in SRC

def test_attribution_is_bounded():
    for token in ("valid disjoint source indexes required", "support_indexes", "dissent_indexes"):
        assert token in SRC

def test_replay_and_url_guards():
    for token in ("docket or manifest already convened", "distinct agenda and minute URLs required", "public HTTPS URL required"):
        assert token in SRC
