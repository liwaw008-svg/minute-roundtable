import json, re, time
from pathlib import Path
from genlayer_py import create_client, create_account
from genlayer_py.chains import studionet

ROOT = Path(__file__).parents[1]; ENV = (ROOT.parents[3] / "accounts.env").read_text(encoding="utf-8")
KEY = re.search(r'^ACCOUNT_4_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', ENV, re.M).group(1).strip()
client = create_client(chain=studionet, account=create_account(account_private_key=KEY)); deployment = json.loads((ROOT / "deployment.json").read_text())
contract = client.get_contract_at(deployment["contractAddress"]); manifest = "https://raw.githubusercontent.com/liwaw008-svg/minute-roundtable/main/fixtures/manifest.json"
run = {"network":"StudioNet","contract":deployment["contractAddress"],"manifest":manifest,"transactions":[]}
for method, args in (("convene", [manifest]), ("reconcile", ["CIVIC-TABLE-07"])):
    tx = contract.write_transaction(method_name=method, args=args)
    receipt = client.wait_for_transaction_receipt(transaction_hash=tx, wait_until="finalized", retries=180, interval=5000, full_transaction=True)
    run["transactions"].append({"method":method,"hash":str(tx),"result":receipt.get("result_name")}); assert receipt.get("result_name") == "MAJORITY_AGREE"; time.sleep(1)
run["finalRecord"] = contract.read(method_name="get_docket", args=["CIVIC-TABLE-07"])
(ROOT / "evidence" / "live-run.json").parent.mkdir(exist_ok=True); (ROOT / "evidence" / "live-run.json").write_text(json.dumps(run, indent=2, default=str) + "\n")
print(json.dumps(run, indent=2, default=str))
