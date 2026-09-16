const API_BASE = "http://127.0.0.1:8000";


// ============================================================
// HELPER — DISPLAY RESULT
// ============================================================

function showResult(elementId, message, type = "success") {
    const element = document.getElementById(elementId);

    element.textContent = message;
    element.className = `result ${type}`;
}


// ============================================================
// HELPER — BUTTON LOADING STATE
// ============================================================

function setButtonLoading(buttonId, loading, text = "") {
    const button = document.getElementById(buttonId);

    if (!button) {
        return;
    }

    if (loading) {
        button.dataset.originalText = button.textContent;
        button.textContent = "Processing...";
        button.disabled = true;
    } else {
        button.textContent =
            text || button.dataset.originalText || "Submit";

        button.disabled = false;
    }
}


// ============================================================
// HELPER — COPY TEXT
// ============================================================

async function copyText(elementId) {

    const element = document.getElementById(elementId);

    if (!element) {
        return;
    }

    const text = element.textContent.trim();

    if (!text || text === "-") {
        return;
    }

    try {

        await navigator.clipboard.writeText(text);

        const buttons = document.querySelectorAll(
            `[onclick="copyText('${elementId}')"]`
        );

        buttons.forEach(button => {

            const originalText = button.textContent;

            button.textContent = "Copied!";

            setTimeout(() => {
                button.textContent = originalText;
            }, 1200);

        });

    } catch (error) {

        console.error("Copy failed:", error);

    }
}


// ============================================================
// BLOCKCHAIN STATUS
// ============================================================

async function checkBlockchainStatus() {

    const statusDot =
        document.getElementById("statusDot");

    const statusText =
        document.getElementById("statusText");

    try {

        const response =
            await fetch(`${API_BASE}/health`);

        if (!response.ok) {
            throw new Error("Backend unavailable");
        }

        const data =
            await response.json();


        document.getElementById("network").textContent =
            data.network;


        document.getElementById("appId").textContent =
            data.application_id;


        document.getElementById("appAddress").textContent =
            data.application_address;


        statusDot.className =
            "status-dot connected";

        statusText.textContent =
            "Blockchain Connected";

    } catch (error) {

        console.error(error);

        statusDot.className =
            "status-dot error";

        statusText.textContent =
            "Blockchain Offline";


        document.getElementById("network").textContent =
            "-";

        document.getElementById("appId").textContent =
            "-";

        document.getElementById("appAddress").textContent =
            "-";
    }
}


// ============================================================
// REGISTER HEALTH RECORD
// ============================================================

async function registerRecord() {

    const recordId =
        document
            .getElementById("registerRecordId")
            .value
            .trim();


    const recordHash =
        document
            .getElementById("registerHash")
            .value
            .trim();


    if (!recordId || !recordHash) {

        showResult(
            "registerResult",
            "Please enter both Record ID and Record Hash.",
            "error"
        );

        return;
    }


    setButtonLoading(
        "registerBtn",
        true
    );


    try {

        const response =
            await fetch(
                `${API_BASE}/records`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        record_id: recordId,
                        record_hash: recordHash
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Registration failed"
            );

        }


        showResult(
            "registerResult",
            `Record registered successfully. Transaction ID: ${data.transaction_id}`,
            "success"
        );


        document
            .getElementById("lookupRecordId")
            .value = recordId;


        document
            .getElementById("accessRecordId")
            .value = recordId;


    } catch (error) {

        showResult(
            "registerResult",
            error.message,
            "error"
        );

    } finally {

        setButtonLoading(
            "registerBtn",
            false,
            "Register Record"
        );

    }
}


// ============================================================
// GET RECORD INFORMATION
// ============================================================

async function getRecordInfo() {

    const recordId =
        document
            .getElementById("lookupRecordId")
            .value
            .trim();


    if (!recordId) {

        showResult(
            "recordResult",
            "Please enter a Record ID.",
            "error"
        );

        return;
    }


    setButtonLoading(
        "searchBtn",
        true
    );


    try {

        const [hashResponse, ownerResponse] =
            await Promise.all([

                fetch(
                    `${API_BASE}/records/${encodeURIComponent(recordId)}/hash`
                ),

                fetch(
                    `${API_BASE}/records/${encodeURIComponent(recordId)}/owner`
                )

            ]);


        const hashData =
            await hashResponse.json();

        const ownerData =
            await ownerResponse.json();


        if (!hashResponse.ok) {

            throw new Error(
                hashData.detail ||
                "Unable to retrieve record hash"
            );

        }


        if (!ownerResponse.ok) {

            throw new Error(
                ownerData.detail ||
                "Unable to retrieve record owner"
            );

        }


        document
            .getElementById("recordHash")
            .textContent =
            hashData.record_hash;


        document
            .getElementById("recordOwner")
            .textContent =
            ownerData.owner;


        showResult(
            "recordResult",
            "Record information retrieved successfully.",
            "success"
        );


    } catch (error) {

        document
            .getElementById("recordHash")
            .textContent = "-";


        document
            .getElementById("recordOwner")
            .textContent = "-";


        showResult(
            "recordResult",
            error.message,
            "error"
        );


    } finally {

        setButtonLoading(
            "searchBtn",
            false,
            "Search"
        );

    }
}


// ============================================================
// GET ACCESS FORM VALUES
// ============================================================

function getAccessValues() {

    const recordId =
        document
            .getElementById("accessRecordId")
            .value
            .trim();


    const provider =
        document
            .getElementById("providerAddress")
            .value
            .trim();


    return {
        recordId,
        provider
    };
}


// ============================================================
// VALIDATE ACCESS INPUT
// ============================================================

function validateAccessInput(recordId, provider) {

    if (!recordId) {

        showResult(
            "accessResult",
            "Please enter a Record ID.",
            "error"
        );

        return false;
    }


    if (!provider) {

        showResult(
            "accessResult",
            "Please enter the provider Algorand address.",
            "error"
        );

        return false;
    }


    if (provider.length !== 58) {

        showResult(
            "accessResult",
            "Provider address must contain exactly 58 characters.",
            "error"
        );

        return false;
    }


    return true;
}


// ============================================================
// GRANT PROVIDER ACCESS
// ============================================================

async function grantAccess() {

    const { recordId, provider } =
        getAccessValues();


    if (!validateAccessInput(recordId, provider)) {
        return;
    }


    setButtonLoading(
        "grantBtn",
        true
    );


    try {

        const response =
            await fetch(
                `${API_BASE}/records/${encodeURIComponent(recordId)}/grant`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        record_id: recordId,
                        provider: provider
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Grant access failed"
            );

        }


        showResult(
            "accessResult",
            `Provider access granted successfully. Transaction ID: ${data.transaction_id}`,
            "success"
        );


        await checkAccess(false);


    } catch (error) {

        showResult(
            "accessResult",
            error.message,
            "error"
        );


    } finally {

        setButtonLoading(
            "grantBtn",
            false,
            "Grant Access"
        );

    }
}


// ============================================================
// REVOKE PROVIDER ACCESS
// ============================================================

async function revokeAccess() {

    const { recordId, provider } =
        getAccessValues();


    if (!validateAccessInput(recordId, provider)) {
        return;
    }


    setButtonLoading(
        "revokeBtn",
        true
    );


    try {

        const response =
            await fetch(
                `${API_BASE}/records/${encodeURIComponent(recordId)}/revoke`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        record_id: recordId,
                        provider: provider
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Revoke access failed"
            );

        }


        showResult(
            "accessResult",
            `Provider access revoked successfully. Transaction ID: ${data.transaction_id}`,
            "success"
        );


        await checkAccess(false);


    } catch (error) {

        showResult(
            "accessResult",
            error.message,
            "error"
        );


    } finally {

        setButtonLoading(
            "revokeBtn",
            false,
            "Revoke Access"
        );

    }
}


// ============================================================
// CHECK PROVIDER ACCESS
// ============================================================

async function checkAccess(showMessage = true) {

    const { recordId, provider } =
        getAccessValues();


    if (!validateAccessInput(recordId, provider)) {
        return;
    }


    setButtonLoading(
        "checkBtn",
        true
    );


    try {

        const response =
            await fetch(
                `${API_BASE}/records/${encodeURIComponent(recordId)}/access/${encodeURIComponent(provider)}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to check access"
            );

        }


        const badge =
            document.getElementById("accessStatus");


        if (data.has_access) {

            badge.textContent =
                "Access Granted";

            badge.className =
                "access-badge granted";

        } else {

            badge.textContent =
                "Access Revoked";

            badge.className =
                "access-badge revoked";
        }


        if (showMessage) {

            showResult(
                "accessResult",
                `Provider access status: ${data.has_access ? "GRANTED" : "REVOKED"} (value: ${data.access_value})`,
                "success"
            );

        }


    } catch (error) {

        document
            .getElementById("accessStatus")
            .textContent =
            "Unknown";


        document
            .getElementById("accessStatus")
            .className =
            "access-badge neutral";


        if (showMessage) {

            showResult(
                "accessResult",
                error.message,
                "error"
            );

        }


    } finally {

        setButtonLoading(
            "checkBtn",
            false,
            "Check Access"
        );

    }
}


// ============================================================
// INITIALIZE DASHBOARD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        checkBlockchainStatus();

    }
);