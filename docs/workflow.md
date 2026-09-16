# System Workflow

## 1. Overall Workflow

The system follows a patient-controlled blockchain authorization workflow.

```text
Patient
   |
   v
Register Health Record
   |
   v
Generate / Obtain Record Hash
   |
   v
FastAPI Backend
   |
   v
Algorand Smart Contract
   |
   +----------------------+
   |                      |
   v                      v
Record Owner          Record Hash
   |
   v
Provider Access Control
   |
   +------------+
   |            |
   v            v
Grant        Revoke
Access       Access
   |            |
   v            v
Access = 1    Access = 0