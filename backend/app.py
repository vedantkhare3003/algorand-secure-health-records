from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.blockchain import (
    get_blockchain_status,
    register_record,
    grant_access,
    revoke_access,
    has_access,
    get_record_hash,
    get_record_owner,
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Secure Health Records API",
    description="Backend API for an Algorand-based secure health records system.",
    version="1.0.0",
)


# ============================================================
# REQUEST MODELS
# ============================================================

class RegisterRecordRequest(BaseModel):
    record_id: str
    record_hash: str


class AccessRequest(BaseModel):
    record_id: str
    provider: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Secure Health Records API",
        "status": "running",
        "blockchain": "Algorand LocalNet",
        "application_id": 1001,
    }


# ============================================================
# BLOCKCHAIN STATUS
# ============================================================

@app.get("/health")
def health():
    try:
        return get_blockchain_status()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# REGISTER HEALTH RECORD
# ============================================================

@app.post("/records")
def create_record(request: RegisterRecordRequest):

    try:
        tx_id = register_record(
            request.record_id,
            request.record_hash,
        )

        return {
            "success": True,
            "message": "Health record registered successfully",
            "record_id": request.record_id,
            "transaction_id": tx_id,
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ============================================================
# GET RECORD HASH
# ============================================================

@app.get("/records/{record_id}/hash")
def read_record_hash(record_id: str):

    try:
        record_hash = get_record_hash(record_id)

        return {
            "success": True,
            "record_id": record_id,
            "record_hash": record_hash,
        }

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


# ============================================================
# GET RECORD OWNER
# ============================================================

@app.get("/records/{record_id}/owner")
def read_record_owner(record_id: str):

    try:
        owner = get_record_owner(record_id)

        return {
            "success": True,
            "record_id": record_id,
            "owner": owner,
        }

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


# ============================================================
# GRANT PROVIDER ACCESS
# ============================================================

@app.post("/records/{record_id}/grant")
def grant_provider_access(
    record_id: str,
    request: AccessRequest,
):

    if request.record_id != record_id:

        raise HTTPException(
            status_code=400,
            detail="Record ID in URL and request body must match",
        )

    try:

        tx_id = grant_access(
            record_id,
            request.provider,
        )

        return {
            "success": True,
            "message": "Provider access granted successfully",
            "record_id": record_id,
            "provider": request.provider,
            "transaction_id": tx_id,
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ============================================================
# REVOKE PROVIDER ACCESS
# ============================================================

@app.post("/records/{record_id}/revoke")
def revoke_provider_access(
    record_id: str,
    request: AccessRequest,
):

    if request.record_id != record_id:

        raise HTTPException(
            status_code=400,
            detail="Record ID in URL and request body must match",
        )

    try:

        tx_id = revoke_access(
            record_id,
            request.provider,
        )

        return {
            "success": True,
            "message": "Provider access revoked successfully",
            "record_id": record_id,
            "provider": request.provider,
            "transaction_id": tx_id,
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ============================================================
# CHECK PROVIDER ACCESS
# ============================================================

@app.get("/records/{record_id}/access/{provider}")
def check_provider_access(
    record_id: str,
    provider: str,
):

    try:

        access = has_access(
            record_id,
            provider,
        )

        return {
            "success": True,
            "record_id": record_id,
            "provider": provider,
            "has_access": bool(access),
            "access_value": access,
        }

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )