# OCI Core Services Demo (Compute + Object Storage)

This repo is a small hands-on demo using the official Oracle Cloud Infrastructure (OCI) Python SDK.

## What it does

1. Lists Compute instances in a target compartment
2. Creates (or verifies) a private Object Storage bucket
3. Uploads a timestamped report file to the bucket

## Requirements

- Python 3.9+
- OCI config set up at `~/.oci/config`
- An OCI compartment OCID you have access to

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Output
<img width="1444" height="211" alt="image" src="https://github.com/user-attachments/assets/bd03bcde-8259-4405-a9ea-d9a1884ecd8d" />
<img width="1100" height="109" alt="image" src="https://github.com/user-attachments/assets/a01b345a-d6e4-4243-86de-cbb4f8281a33" />
<img width="940" height="421" alt="image" src="https://github.com/user-attachments/assets/07b0cb83-866d-46ae-ac6a-fccb18b87dde" />

## Details
<img width="940" height="474" alt="image" src="https://github.com/user-attachments/assets/0ef639a7-efd1-454a-b5e8-0f8a0f51acc8" />

## Architecture Overview
- OCI Compute used for workload execution
- OCI Object Storage used for artifact storage
- OCI IAM and API Keys used for secure authentication

## Key Learnings
- How OCI SDK authentication works
- Difference between tenancy, compartment, and namespace
- Practical Object Storage usage patterns



