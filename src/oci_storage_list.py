import oci

config = oci.config.from_file()
os_client = oci.object_storage.ObjectStorageClient(config)

namespace = os_client.get_namespace().data
buckets = os_client.list_buckets(namespace, config["tenancy"]).data

print("Buckets:")
for b in buckets:
    print("-", b.name)

print("\nObjects in ace-oci-demo-bucket:")
objects = os_client.list_objects(
    namespace,
    "ace-oci-demo-bucket",
    prefix="ace-demo/"
).data.objects

for obj in objects:
    print("-", obj.name)
