# Secure Health Records Using Algorand

A blockchain-based secure health record management system using the Algorand blockchain, Python, FastAPI, and a web-based frontend.

## Overview

This project demonstrates how Algorand blockchain technology can be used to manage healthcare record ownership, record integrity, and provider access permissions.

The system follows a patient-controlled access model. A health record is represented on-chain using a unique record ID and a cryptographic hash. The patient who registers the record becomes its owner and can grant or revoke access for a healthcare provider identified by an Algorand address.

Actual medical files are not stored directly in the smart contract. The current implementation stores record metadata, ownership information, cryptographic hashes, and access permissions on Algorand LocalNet.

---

## Objectives

- Develop a blockchain-based healthcare record management system.
- Use Algorand smart contracts for access-control management.
- Maintain record integrity using cryptographic hashes.
- Allow a patient to grant provider access.
- Allow a patient to revoke provider access.
- Retrieve record ownership and cryptographic hash information.
- Provide a web-based interface for interacting with the blockchain.
- Demonstrate blockchain-backed authorization using Algorand LocalNet.

---

## System Architecture

The system consists of the following components:

1. Patient / Record Owner
2. Healthcare Provider
3. Web Frontend
4. FastAPI Backend
5. Algorand Typed Client
6. Algorand Smart Contract
7. Algorand LocalNet

```text
                    Secure Health Records
                            |
                            v
                    +---------------+
                    | Web Frontend  |
                    | HTML/CSS/JS   |
                    +-------+-------+
                            |
                            | HTTP / REST API
                            v
                    +---------------+
                    | FastAPI       |
                    | Backend       |
                    +-------+-------+
                            |
                            v
                    +---------------+
                    | Blockchain    |
                    | Integration   |
                    +-------+-------+
                            |
                            v
                    +---------------+
                    | Algorand      |
                    | Typed Client  |
                    +-------+-------+
                            |
                            v
                    +---------------+
                    | Smart         |
                    | Contract      |
                    +-------+-------+
                            |
                            v
                    +---------------+
                    | Algorand      |
                    | LocalNet      |
                    +---------------+