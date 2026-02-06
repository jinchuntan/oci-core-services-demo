import os
import sys
from datetime import datetime

import oci
from dotenv import load_dotenv


def get_config_and_signer():
    """
    Uses OCI config file (~/.oci/config) by default.
    Optionally allow setting OCI_PROFILE via env var.
    """
    profile = os.getenv("OCI_PROFILE", "DEFAULT")
    config_file = os.path.expanduser("~/.oci/config")

    if not os.path.exists(config_file):
        print("ERROR: OCI config file not found at ~/.oci/config")
        print("Create it via OCI Console instructions or use oci setup config.")
        sys.exit(1)

    config = oci.config.from_file(config_file, profile_name=profile)
    signer = oci.signer.Signer(
        tenancy=config["tenancy"],
        user=config["user"],
        fingerprint=config["fingerprint"],
        private_key_file_location=config["key_file"],
        pass_phrase=config.get("pass_phrase"),
    )
    return config, signer


def require_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        print(f"ERROR: Missing env var: {name}")
        sys.exit(1)
    return v


def list_instances(compute_client, compartment_id: str):
    instances = compute_client.list_instances(compartment_id=compartment_id).data
    print(f"\nFound {len(instances)} instance(s):")
    for inst in instances:
        print(f"- {inst.display_name} | {inst.lifecycle_state} | {inst.id}")
    return instances


def ensure_bucket(os_client, namespace: str, compartment_id: str, bucket_name: str):
    # Try get bucket
    try:
        os_client.get_bucket(namespace_name=namespace, bucket_name=bucket_name)
        print(f"\nBucket exists: {bucket_name}")
        return
    except oci.exceptions.ServiceError as e:
        if e.status != 404:
            raise

    # Create bucket
    print(f"\nCreating bucket: {bucket_name}")
    details = oci.object_storage.models.CreateBucketDetails(
        name=bucket_name,
        compartment_id=compartment_id,
        public_access_type="NoPublicAccess",
        storage_tier="Standard",
        versioning="Disabled",
    )
    os_client.create_bucket(namespace_name=namespace, create_bucket_details=details)
    print("Bucket created.")


def upload_text_object(os_client, namespace: str, bucket_name: str, object_name: str, content: str):
    print(f"\nUploading object: {object_name}")
    os_client.put_object(
        namespace_name=namespace,
        bucket_name=bucket_name,
        object_name=object_name,
        put_object_body=content.encode("utf-8"),
    )
    print("Upload complete.")


def main():
    load_dotenv()

    compartment_id = require_env("OCI_COMPARTMENT_OCID")
    bucket_name = os.getenv("OCI_BUCKET_NAME", "ace-oci-demo-bucket")
    object_prefix = os.getenv("OCI_OBJECT_PREFIX", "ace-demo")

    config, signer = get_config_and_signer()

    region = config.get("region")
    print(f"Using region: {region}")

    identity_client = oci.identity.IdentityClient(config=config, signer=signer)
    compute_client = oci.core.ComputeClient(config=config, signer=signer)
    os_client = oci.object_storage.ObjectStorageClient(config=config, signer=signer)

    namespace = os_client.get_namespace().data
    tenancy = identity_client.get_tenancy(tenancy_id=config["tenancy"]).data

    print(f"Tenancy: {tenancy.name}")
    print(f"Object Storage Namespace: {namespace}")

    # 1) List Compute instances
    instances = list_instances(compute_client, compartment_id=compartment_id)

    # 2) Create/ensure a private bucket
    ensure_bucket(os_client, namespace, compartment_id, bucket_name)

    # 3) Upload a small report as an object
    now = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S_UTC")
    object_name = f"{object_prefix}/run_report_{now}.txt"

    report_lines = [
        "ACE OCI Demo Report",
        f"Timestamp: {now}",
        f"Region: {region}",
        f"Tenancy: {tenancy.name}",
        f"Compartment OCID: {compartment_id}",
        f"Instances found: {len(instances)}",
    ]
    for inst in instances:
        report_lines.append(f" - {inst.display_name} | {inst.lifecycle_state}")

    upload_text_object(os_client, namespace, bucket_name, object_name, "\n".join(report_lines))

    print("\nDone !!!")


if __name__ == "__main__":
    main()
