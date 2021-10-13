"""
Tests fixing the problem by not chunking the download, but downloading
everything in one go.  Does not work, as I can still trigger the
ResourceModifiedError by doing lots of reads trying to "catch" the write in the
act.
"""
import uuid
import random
import asyncio
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob.aio import BlobServiceClient
from constring import vanilla_connection_string

async def ensure_container(container_client):
    try:
        return await container_client.create_container()
    except ResourceExistsError:
        pass

async def write_to_blob(container_client, blob_name, data):
    await asyncio.sleep(0.1 * 5)
    print(f"Writing data of size {len(data.encode('utf-8'))} to blob \"{blob_name}\" ({data[:10]}...)")
    blob_client = container_client.get_blob_client(blob_name)
    await blob_client.upload_blob(data, overwrite = True)
    print(f"Wrote data of size {len(data.encode('utf-8'))} to blob \"{blob_name}\"")

async def read_blob(container_client, blob_name):
    me = str(uuid.uuid4())[:5]
    await asyncio.sleep(random.random() * .1)
    blob_client = container_client.get_blob_client(blob_name)
    download = await blob_client.download_blob()
    data = await download.readall()
    print(f"{me} read {len(data)} ({data[:5]}...)")

async def test():
    service_client = BlobServiceClient.from_connection_string(
            vanilla_connection_string,
            max_single_get_size = 1024*1024,
            max_chunk_get_size = 1024*1024)
    async with service_client:
        foo_client = service_client.get_container_client("foo")
        await ensure_container(foo_client)

        await write_to_blob(foo_client, "bar", "a"*(1024*1024*10))

        await asyncio.gather(
            *[read_blob(foo_client,"bar") for _ in range(100)],
            write_to_blob(foo_client, "bar", "b"* (1024*1024*10)))

if __name__ == "__main__":
    print("trying to break blob storage")
    asyncio.run(test())
