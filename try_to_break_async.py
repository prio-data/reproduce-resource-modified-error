
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
    await asyncio.sleep(random.random()*.2)
    print(f"Writing data of size {len(data.encode('utf-8'))} to blob \"{blob_name}\" ({data[:10]}...)")
    blob_client = container_client.get_blob_client(blob_name)
    await blob_client.upload_blob(data, overwrite = True)
    print(f"Wrote data of size {len(data.encode('utf-8'))} to blob \"{blob_name}\"")

async def blob_chunks(container_client, blob_name):
    blob_client = container_client.get_blob_client(blob_name)
    data = await blob_client.download_blob()
    return data.chunks()

async def read_chunks(container_client, blob_name):
    me = str(uuid.uuid4())
    await asyncio.sleep(random.random()*.1)
    it = 0
    async for ch in await blob_chunks(container_client, blob_name):
        await asyncio.sleep(random.random()*0.2)
        print(f"{me[:4]}: Chunk {it}: {len(ch)} ({ch[:10]} ...)")
        it += 1

async def test():
    service_client = BlobServiceClient.from_connection_string(
            vanilla_connection_string,
            max_single_get_size = 1024,
            max_chunk_get_size = 1024)
    async with service_client:
        foo_client = service_client.get_container_client("foo")
        await ensure_container(foo_client)

        await write_to_blob(foo_client, "bar", "a"*(1024*1024*10))

        await asyncio.gather(
            read_chunks(foo_client, "bar"),
            write_to_blob(foo_client, "bar", "b"* (1024*1024*10)))

if __name__ == "__main__":
    print("trying to break blob storage")
    asyncio.run(test())
