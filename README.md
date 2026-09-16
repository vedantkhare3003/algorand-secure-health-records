# Secure Health Records Using Algorand

A blockchain-based secure health record management system using the Algorand blockchain.

## Overview

This project explores the use of Algorand blockchain technology to provide secure access control, record integrity, and transparent authorization for healthcare records.

The system follows a patient-controlled model in which patients can grant or revoke access to authorized healthcare providers.

## Objectives

- Develop a secure healthcare record management system.
- Use Algorand blockchain for access-control management.
- Maintain healthcare record integrity using cryptographic hashes.
- Allow patients to grant and revoke access.
- Maintain a transparent authorization and audit trail.
- Prevent unauthorized access to healthcare records.

## System Architecture

The system consists of:

1. Patient
2. Hospital / Doctor
3. Application Backend
4. Algorand Smart Contract
5. Off-chain encrypted record storage

Sensitive healthcare records are not stored directly on the blockchain. Instead, cryptographic hashes and access-control information are maintained on-chain while the actual records remain in protected off-chain storage.

## Key Features

### Patient

- Register healthcare records
- Grant access to healthcare providers
- Revoke previously granted access
- View authorization history
- Verify record integrity

### Healthcare Provider

- Request access to records
- Verify authorization
- Access records when permission is granted
- Verify record integrity

### Blockchain

- Access-control management
- Record hash verification
- Authorization tracking
- Tamper-evident audit trail

## Technology Stack

- Algorand
- Algorand Smart Contracts
- Python
- JavaScript
- HTML
- CSS
- Git
- GitHub

## Security Approach

Actual healthcare records are kept off-chain.

```text
Healthcare Record
       |
       v
Encrypted Off-chain Storage
       |
       v
Cryptographic Hash
       |
       v
Algorand Blockchain
