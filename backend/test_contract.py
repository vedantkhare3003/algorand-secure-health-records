from algokit_utils import (
    AlgoAmount,
    AlgorandClient,
    CommonAppCallParams,
)

from algokit_utils.applications.app_client import FundAppAccountParams
from algosdk.encoding import decode_address

from health_records_client import HealthRecordsContractClient


# --------------------------------------------------
# Connect to Algorand LocalNet
# --------------------------------------------------

algorand = AlgorandClient.default_localnet()
account = algorand.account.localnet_dispenser()

print("Connected to Algorand LocalNet")
print(f"Test account: {account.address}")


# --------------------------------------------------
# Connect to deployed application
# --------------------------------------------------

client = HealthRecordsContractClient(
    algorand=algorand,
    app_id=1001,
    default_sender=account.address,
    default_signer=account.signer,
)

print(f"Connected to Application ID: {client.app_id}")
print(f"Application Address: {client.app_address}")


# --------------------------------------------------
# Fund application account for Box storage
# --------------------------------------------------

print("\n[0] Checking application account balance...")

app_balance = algorand.account.get_information(
    client.app_address
).amount

print(f"Application balance: {app_balance.micro_algo} microALGO")

if app_balance < AlgoAmount.from_algo(1):
    print("Funding application account...")

    fund_result = client.app_client.fund_app_account(
        FundAppAccountParams(
            amount=AlgoAmount.from_algo(1)
        )
    )

    print("Application account funded successfully!")
    print(f"Funding transaction ID: {fund_result.tx_id}")
else:
    print("Application account already has sufficient balance.")


# --------------------------------------------------
# Test data
# --------------------------------------------------

record_id = b"patient-005"
record_hash = b"sha256-example-hash-005"

provider = account.address


# --------------------------------------------------
# Box references
# --------------------------------------------------

owner_box = b"owner_" + record_id
hash_box = b"hash_" + record_id

provider_bytes = decode_address(provider)

access_box = b"access_" + record_id + provider_bytes


print("\nBox references:")
print(f"Owner box:  {owner_box}")
print(f"Hash box:   {hash_box}")
print(f"Access box length: {len(access_box)} bytes")


# --------------------------------------------------
# Helper: simulate read-only has_access call
# --------------------------------------------------

def check_access():
    """
    Simulate has_access() without submitting a transaction.
    """

    method_call = client.params.has_access(
        args=(record_id, provider),
        params=CommonAppCallParams(
            box_references=[
                owner_box,
                access_box,
            ]
        ),
    )

    result = (
        algorand.new_group()
        .add_app_call_method_call(method_call)
        .simulate()
    )

    return result.returns[0].value


# --------------------------------------------------
# TEST 1: Register health record
# --------------------------------------------------

print("\n[1] Registering health record...")

result = client.send.register_record(
    args=(record_id, record_hash),
    params=CommonAppCallParams(
        box_references=[
            owner_box,
            hash_box,
        ]
    ),
)

print("Record registered successfully!")
print(f"Transaction ID: {result.tx_id}")


# --------------------------------------------------
# TEST 2: Read record hash
# --------------------------------------------------

print("\n[2] Reading record hash...")

result = client.send.get_record_hash(
    args=(record_id,),
    params=CommonAppCallParams(
        box_references=[
            owner_box,
            hash_box,
        ]
    ),
)

print(f"Stored record hash: {result.abi_return}")


# --------------------------------------------------
# TEST 3: Read record owner
# --------------------------------------------------

print("\n[3] Reading record owner...")

result = client.send.get_record_owner(
    args=(record_id,),
    params=CommonAppCallParams(
        box_references=[
            owner_box,
        ]
    ),
)

print(f"Record owner: {result.abi_return}")


# --------------------------------------------------
# TEST 4: Check provider access BEFORE granting
# --------------------------------------------------

print("\n[4] Checking provider access...")

access_before = check_access()

print(f"Access before granting: {access_before}")


# --------------------------------------------------
# TEST 5: Grant provider access
# --------------------------------------------------

print("\n[5] Granting provider access...")

result = client.send.grant_access(
    args=(record_id, provider),
    params=CommonAppCallParams(
        box_references=[
            owner_box,
            access_box,
        ]
    ),
)

print("Access granted successfully!")
print(f"Transaction ID: {result.tx_id}")


# --------------------------------------------------
# TEST 6: Check provider access AFTER granting
# --------------------------------------------------

print("\n[6] Checking access after granting...")

access_after_grant = check_access()

print(f"Access after granting: {access_after_grant}")


# --------------------------------------------------
# TEST 7: Revoke provider access
# --------------------------------------------------

print("\n[7] Revoking provider access...")

result = client.send.revoke_access(
    args=(record_id, provider),
    params=CommonAppCallParams(
        box_references=[
            owner_box,
            access_box,
        ]
    ),
)

print("Access revoked successfully!")
print(f"Transaction ID: {result.tx_id}")


# --------------------------------------------------
# TEST 8: Check provider access AFTER revoking
# --------------------------------------------------

print("\n[8] Checking access after revoking...")

access_after_revoke = check_access()

print(f"Access after revoking: {access_after_revoke}")


# --------------------------------------------------
# Final validation
# --------------------------------------------------

print("\n========================================")
print("HEALTH RECORD TEST RESULTS")
print("========================================")

print(f"Register Record       : PASS")
print(f"Read Record Hash      : PASS")
print(f"Read Record Owner     : PASS")
print(f"Initial Access        : {access_before}")
print(f"Grant Access          : PASS")
print(f"Access After Grant    : {access_after_grant}")
print(f"Revoke Access         : PASS")
print(f"Access After Revoke   : {access_after_revoke}")

print("========================================")

if access_before == 0 and access_after_grant == 1 and access_after_revoke == 0:
    print("ALL TESTS PASSED SUCCESSFULLY!")
else:
    print("TEST COMPLETED, BUT ACCESS VALUES ARE UNEXPECTED.")

print("========================================")