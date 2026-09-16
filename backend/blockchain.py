from algokit_utils import (
    AlgoAmount,
    AlgorandClient,
    CommonAppCallParams,
)

from algosdk.encoding import decode_address

from backend.health_records_client import HealthRecordsContractClient


# ============================================================
# ALGOrAND CONFIGURATION
# ============================================================

APP_ID = 1001


# Connect to Algorand LocalNet
algorand = AlgorandClient.default_localnet()


# LocalNet test account
account = algorand.account.localnet_dispenser()


# Typed smart contract client
client = HealthRecordsContractClient(
    algorand=algorand,
    app_id=APP_ID,
    default_sender=account.address,
    default_signer=account.signer,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_owner_box(record_id: bytes) -> bytes:
    """Return the BoxMap key used for record ownership."""
    return b"owner_" + record_id


def get_hash_box(record_id: bytes) -> bytes:
    """Return the BoxMap key used for record hash."""
    return b"hash_" + record_id


def get_access_box(record_id: bytes, provider: str) -> bytes:
    """Return the BoxMap key used for provider access."""
    provider_bytes = decode_address(provider)
    return b"access_" + record_id + provider_bytes


def ensure_app_funded() -> None:
    """
    Ensure the application account has enough ALGO
    for Box storage.
    """

    app_balance = algorand.account.get_information(
        client.app_address
    ).amount

    if app_balance < AlgoAmount.from_algo(1):
        client.app_client.fund_app_account(
            amount=AlgoAmount.from_algo(1)
        )


# ============================================================
# REGISTER HEALTH RECORD
# ============================================================

def register_record(record_id: str, record_hash: str) -> str:
    """
    Register a new health record on Algorand.

    The actual medical file remains off-chain.
    Only its cryptographic hash is stored on-chain.
    """

    ensure_app_funded()

    record_id_bytes = record_id.encode()
    record_hash_bytes = record_hash.encode()

    owner_box = get_owner_box(record_id_bytes)
    hash_box = get_hash_box(record_id_bytes)

    result = client.send.register_record(
        args=(
            record_id_bytes,
            record_hash_bytes,
        ),
        params=CommonAppCallParams(
            box_references=[
                owner_box,
                hash_box,
            ]
        ),
    )

    return result.tx_id


# ============================================================
# GRANT ACCESS
# ============================================================

def grant_access(record_id: str, provider: str) -> str:
    """
    Grant a provider access to a health record.

    The transaction is signed by the patient account.
    """

    record_id_bytes = record_id.encode()

    owner_box = get_owner_box(record_id_bytes)
    access_box = get_access_box(
        record_id_bytes,
        provider,
    )

    result = client.send.grant_access(
        args=(
            record_id_bytes,
            provider,
        ),
        params=CommonAppCallParams(
            box_references=[
                owner_box,
                access_box,
            ]
        ),
    )

    return result.tx_id


# ============================================================
# REVOKE ACCESS
# ============================================================

def revoke_access(record_id: str, provider: str) -> str:
    """
    Revoke a provider's access to a health record.
    """

    record_id_bytes = record_id.encode()

    owner_box = get_owner_box(record_id_bytes)
    access_box = get_access_box(
        record_id_bytes,
        provider,
    )

    result = client.send.revoke_access(
        args=(
            record_id_bytes,
            provider,
        ),
        params=CommonAppCallParams(
            box_references=[
                owner_box,
                access_box,
            ]
        ),
    )

    return result.tx_id


# ============================================================
# CHECK ACCESS
# ============================================================

def has_access(record_id: str, provider: str) -> int:
    """
    Check whether a provider has access to a health record.

    This uses transaction simulation, so it does NOT create
    a new blockchain transaction.
    """

    record_id_bytes = record_id.encode()

    owner_box = get_owner_box(record_id_bytes)
    access_box = get_access_box(
        record_id_bytes,
        provider,
    )

    method_call = client.params.has_access(
        args=(
            record_id_bytes,
            provider,
        ),
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


# ============================================================
# GET RECORD HASH
# ============================================================

def get_record_hash(record_id: str) -> str:
    """
    Retrieve the cryptographic hash stored for a health record.
    """

    record_id_bytes = record_id.encode()

    owner_box = get_owner_box(record_id_bytes)
    hash_box = get_hash_box(record_id_bytes)

    method_call = client.params.get_record_hash(
        args=(record_id_bytes,),
        params=CommonAppCallParams(
            box_references=[
                owner_box,
                hash_box,
            ]
        ),
    )

    result = (
        algorand.new_group()
        .add_app_call_method_call(method_call)
        .simulate()
    )

    value = result.returns[0].value

    if isinstance(value, bytes):
        return value.decode()

    if isinstance(value, list):
        return bytes(value).decode()

    return str(value)


# ============================================================
# GET RECORD OWNER
# ============================================================

def get_record_owner(record_id: str) -> str:
    """
    Retrieve the Algorand address that owns a health record.
    """

    record_id_bytes = record_id.encode()

    owner_box = get_owner_box(record_id_bytes)

    method_call = client.params.get_record_owner(
        args=(record_id_bytes,),
        params=CommonAppCallParams(
            box_references=[
                owner_box,
            ]
        ),
    )

    result = (
        algorand.new_group()
        .add_app_call_method_call(method_call)
        .simulate()
    )

    value = result.returns[0].value

    return str(value)


# ============================================================
# BASIC CONNECTION TEST
# ============================================================

def get_blockchain_status() -> dict:
    """
    Return basic information about the Algorand connection.
    """

    app_info = algorand.app.get_by_id(APP_ID)

    return {
        "network": "Algorand LocalNet",
        "application_id": APP_ID,
        "application_address": client.app_address,
        "connected": True,
        "account": account.address,
        "app_exists": app_info is not None,
    }