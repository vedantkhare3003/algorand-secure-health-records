import json
from pathlib import Path

from algokit_utils import AlgorandClient


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_DIR = PROJECT_ROOT / "contracts"

ARC56_PATH = CONTRACTS_DIR / "HealthRecordsContract.arc56.json"


# --------------------------------------------------
# Connect to Algorand LocalNet
# --------------------------------------------------

algorand = AlgorandClient.default_localnet()

# Get funded LocalNet dispenser account
dispenser = algorand.account.localnet_dispenser()

print("Connected to Algorand LocalNet")
print(f"Deployer address: {dispenser.address}")


# --------------------------------------------------
# Load ARC-56 application specification
# --------------------------------------------------

with ARC56_PATH.open("r", encoding="utf-8") as file:
    app_spec = json.load(file)

print(f"Loaded contract specification: {ARC56_PATH.name}")


# --------------------------------------------------
# Create application factory
# --------------------------------------------------

factory = algorand.client.get_app_factory(
    app_spec=app_spec,
    default_sender=dispenser.address,
    default_signer=dispenser.signer,
    app_name="HealthRecordsContract",
)


# --------------------------------------------------
# Deploy application
# --------------------------------------------------

app_client, result = factory.deploy()


# --------------------------------------------------
# Display deployment information
# --------------------------------------------------

print("\n========================================")
print("Health Records Contract Deployed")
print("========================================")
print(f"Application ID: {app_client.app_id}")
print(f"Application Address: {app_client.app_address}")
print(f"Operation: {result.operation_performed}")
print("========================================")