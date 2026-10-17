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

## Setup and Run

Run these commands from the repository root with Python 3.11 or newer.
Configure OCI API-key authentication in `~/.oci/config` first
(`%USERPROFILE%\.oci\config` on Windows).

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
.\.venv\Scripts\python.exe src/oci_demo.py
```

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env with your compartment OCID and destination bucket before running.
.venv/bin/python src/oci_demo.py
```

Copy the template only on first setup; keep an existing `.env` when updating.
If your Windows installation uses `python` instead of `py -3.11`, substitute
that command when creating the environment. No environment activation is needed.

### Configuration and Permissions

| Setting | Meaning |
| --- | --- |
| `OCI_COMPARTMENT_OCID` | Required: the compartment to inspect. |
| `OCI_BUCKET_NAME` | Destination bucket; defaults to `ace-oci-demo-bucket`. |
| `OCI_OBJECT_PREFIX` | Report object prefix; defaults to `ace-demo`. |
| `OCI_PROFILE` | OCI SDK profile name; defaults to `DEFAULT`. |

The configured identity must be allowed to read the tenancy and Compute instances,
resolve the Object Storage namespace, and upload objects to the selected bucket.
The script checks the bucket and creates a private bucket if it is missing,
so it also needs permission to read the bucket and create it when necessary.
Reports are uploaded directly as text objects; no local report file is written.
The optional `src/oci_storage_list.py` helper still uses the `DEFAULT` profile,
`ace-oci-demo-bucket` and `ace-demo/` directly; it does not load `.env`.

Local `.env` files, signing keys, environments and generated reports are ignored by Git.

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



