# System Architecture

## 1. Overview

The Secure Health Records system uses a layered architecture combining a web frontend, REST API backend, Algorand smart contract, and Algorand LocalNet.

The architecture separates the user interface from blockchain interaction. The frontend communicates with the FastAPI backend through HTTP requests, while the backend uses the Algorand client to interact with the deployed smart contract.

---

## 2. Architecture Diagram

```text
+------------------------------------------------------+
|                    USER LAYER                        |
|                                                      |
|              Patient / Healthcare Provider           |
+---------------------------+--------------------------+
                            |
                            | Browser
                            v
+------------------------------------------------------+
|                  PRESENTATION LAYER                  |
|                                                      |
|       HTML5 + CSS3 + JavaScript Frontend             |
|                                                      |
|   - Register Record                                  |
|   - Retrieve Record Information                      |
|   - Grant Provider Access                             |
|   - Revoke Provider Access                            |
|   - Check Provider Access                             |
+---------------------------+--------------------------+
                            |
                            | HTTP / REST
                            v
+------------------------------------------------------+
|                    API LAYER                         |
|                                                      |
|                    FastAPI                           |
|                                                      |
|   /health                                            |
|   /records                                           |
|   /records/{id}/hash                                 |
|   /records/{id}/owner                                |
|   /records/{id}/grant                                |
|   /records/{id}/revoke                               |
|   /records/{id}/access/{provider}                    |
+---------------------------+--------------------------+
                            |
                            | Python
                            v
+------------------------------------------------------+
|                BLOCKCHAIN INTEGRATION                |
|                                                      |
|              blockchain.py                           |
|                                                      |
|        Algorand Typed Contract Client                |
+---------------------------+--------------------------+
                            |
                            | Application Calls
                            v
+------------------------------------------------------+
|                 SMART CONTRACT                       |
|                                                      |
|             HealthRecordsContract                    |
|                                                      |
|   Record Owner       -> record_owner                 |
|   Record Hash        -> record_hash                  |
|   Provider Access    -> access                       |
+---------------------------+--------------------------+
                            |
                            v
+------------------------------------------------------+
|                 ALGORAND LOCALNET                    |
|                                                      |
|                 Application ID: 1001                 |
+------------------------------------------------------+