
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient
from constring import vanilla_connection_string

def ensure_container(container_client):
    try:
        container_client.create_container()
    except ResourceExistsError:
        pass

write_to_blob = lambda container_client, blob_name, data: (container_client
        .get_blob_client(blob_name)
        .upload_blob(data, overwrite = True))

blob_iterator = lambda container_client, blob_name: (container_client
        .get_blob_client(blob_name)
        .download_blob()
        .chunks())

def overwrite_while_reading(container_client, blob_name):
    write_to_blob(container_client, blob_name, "a" * 100000000)
    iterator = blob_iterator(container_client, blob_name)
    for it,ch in enumerate(iterator):
        if it == 1:
            write_to_blob(container_client, blob_name, "b" * 100000000)
            print("overwrote")
        print(f"Chunk {it}: {len(ch)} ({ch[:10]} ...)")

if __name__ == "__main__":
    print("trying to break blob storage")
    service_client = BlobServiceClient.from_connection_string(vanilla_connection_string)
    container_client = service_client.get_container_client("foo")
    ensure_container(container_client)
    overwrite_while_reading(container_client, "bar")
