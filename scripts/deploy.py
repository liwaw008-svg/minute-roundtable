import hashlib, json, re, subprocess
from pathlib import Path
from genlayer_py import create_client, create_account
from genlayer_py.chains import studionet

ROOT = Path(__file__).parents[1]
ENV = (ROOT.parents[3] / "accounts.env").read_text(encoding="utf-8")
KEY = re.search(r'^ACCOUNT_4_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', ENV, re.M).group(1).strip()
client = create_client(chain=studionet, account=create_account(account_private_key=KEY))
code = (ROOT / "contracts" / "contract.py").read_text(encoding="utf-8")
tx = client.deploy_contract(code=code, args=[]); print("deploy_tx=" + str(tx), flush=True)
receipt = client.wait_for_transaction_receipt(transaction_hash=tx, wait_until="finalized", retries=180, interval=5000, full_transaction=True)
leaders = receipt.get("consensus_data", {}).get("leader_receipt") or []; leaders = [leaders] if isinstance(leaders, dict) else leaders
assert receipt.get("result_name") == "MAJORITY_AGREE" and any(item.get("execution_result") == "SUCCESS" for item in leaders)
address = receipt.get("data", {}).get("contract_address") or receipt.get("to_address")
out = {"network":"StudioNet","contractAddress":address,"deploymentTransaction":str(tx),"sourceSha256":hashlib.sha256(code.encode()).hexdigest(),"sourceCommit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),"repository":"https://github.com/liwaw008-svg/minute-roundtable","publicSite":"https://minute-roundtable.pages.dev/"}
(ROOT / "deployment.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8"); print(json.dumps(out, indent=2))
