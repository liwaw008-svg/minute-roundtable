import json,re,time
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
from genlayer_py.contracts import actions as contract_actions
def compat(method=None,args=None,kwargs=None):
    out={}
    if method is not None: out["method"]=method
    if args: out["args"]=args
    if kwargs: out["kwargs"]=kwargs
    return out
contract_actions.make_calldata_object=compat
ROOT=Path(__file__).parents[1]; ENV=(ROOT.parents[3]/"accounts.env").read_text(encoding="utf-8")
KEY=re.search(r'^ACCOUNT_4_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',ENV,re.M).group(1).strip()
ADDRESS=json.loads((ROOT/"deployment.json").read_text())["contractAddress"]
client=create_client(chain=studionet,account=create_account(account_private_key=KEY))
def write(name,args):
    tx=client.write_contract(address=ADDRESS,function_name=name,args=args); print(name+"_tx="+str(tx),flush=True)
    receipt=client.wait_for_transaction_receipt(transaction_hash=tx,wait_until="finalized",retries=180,interval=5000,full_transaction=True)
    leaders=receipt.get("consensus_data",{}).get("leader_receipt") or []; leaders=[leaders] if isinstance(leaders,dict) else leaders
    assert receipt.get("result_name")=="MAJORITY_AGREE" and any(item.get("execution_result")=="SUCCESS" for item in leaders)
    return str(tx)
meeting_id="LIVE-TABLE-"+str(int(time.time()))
agenda=[{"id":"A1","prompt":"Which release window did the table approve?","options":[{"code":"MORNING","label":"Morning release"},{"code":"EVENING","label":"Evening release"}]},{"id":"A2","prompt":"Should public review remain open for a full week?","options":[{"code":"SEVEN_DAYS","label":"Seven days"},{"code":"THREE_DAYS","label":"Three days"}]}]
minutes=[{"label":"North seat","text":"The table selected the morning release window. Members also approved keeping the public review open for seven full days."},{"label":"West seat","text":"Consensus formed around a morning release. The recorded review period was seven days before final publication."},{"label":"East seat","text":"The chair confirmed MORNING as the release window and SEVEN_DAYS as the public review duration."}]
transactions={"convene":write("convene",[meeting_id,"Public release coordination",json.dumps(agenda),json.dumps(minutes),2])}; transactions["reconcile"]=write("reconcile",[meeting_id])
final=client.read_contract(address=ADDRESS,function_name="get_docket",args=[meeting_id])
assert final["state"]=="MINUTED" and len(final["decisions"])+len(final["disputed"])+len(final["omitted"])==2
proof={"meetingId":meeting_id,"contract":ADDRESS,"transactions":transactions,"final":final,"disclosure":"The three note books are repository-owner demonstration records supplied directly to the contract."}
(ROOT/"evidence").mkdir(exist_ok=True); (ROOT/"evidence"/"live-run.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8"); print(json.dumps(proof,indent=2))

