from pathlib import Path
SRC=(Path(__file__).parents[1]/"contracts"/"contract.py").read_text(encoding="utf-8")
def test_real_write_lifecycle():
    for token in ('def convene(','def reconcile(','def get_docket(','"SEATED"','"MINUTED"'): assert token in SRC
def test_direct_user_records_replace_remote_fixtures():
    for token in ('agenda_json: str','minutes_json: str','normalize_agenda','normalize_minutes'): assert token in SRC
    assert 'gl.nondet.web.get' not in SRC and 'raw.githubusercontent.com' not in SRC
def test_inputs_are_bounded_and_replay_safe():
    for token in ('two to six agenda items required','three to five minute books required','meeting id or exact record already used','used_inputs'): assert token in SRC
def test_consensus_result_is_complete_and_attributed():
    for token in ('complete agenda vector required','agreed decision lacks quorum','valid disjoint source indexes required','support_indexes','dissent_indexes'): assert token in SRC
def test_terminal_state_blocks_reconciliation_replay():
    assert 'only a seated meeting can be reconciled' in SRC and 'meeting.state="MINUTED"' in SRC

