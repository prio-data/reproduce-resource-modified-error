from datetime import datetime
import io
import uuid
import random
import asyncio
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob.aio import BlobServiceClient
from constring import vanilla_connection_string

timestamp = lambda: datetime.now().strftime("%H:%M:%S.%f")

async def ensure_container(container_client):
    try:
        return await container_client.create_container()
    except ResourceExistsError:
        pass

async def write_to_blob(container_client, blob_name, data):
    await asyncio.sleep(1)
    print(f"{timestamp()} "
          f"Writing data of size {len(data.encode('utf-8'))} to blob \"{blob_name}\" ({data[:10]}...)")
    blob_client = container_client.get_blob_client(blob_name)
    await blob_client.upload_blob(data, overwrite = True)
    print(f"{timestamp()} "
          f"Wrote data of size {len(data.encode('utf-8'))} to blob \"{blob_name}\"")

async def read_blob(container_client, blob_name):
    me = str(uuid.uuid4())[:5]
    mock_output = io.BytesIO()
    await asyncio.sleep(random.random() * 2)
    blob_client = container_client.get_blob_client(blob_name)
    download = await blob_client.download_blob()
    await download.download_to_stream(mock_output)
    data = mock_output.getvalue()
    print(f"{timestamp()} {me} read {len(data)} ({data[:5]}...)")

async def test():
    service_client = BlobServiceClient.from_connection_string(vanilla_connection_string,
            max_read_size = 1024*1024*10,
            max_chunk_size = 1024*1024*10)
    async with service_client:
        foo_client = service_client.get_container_client("foo")
        await ensure_container(foo_client)

        await write_to_blob(foo_client, "bar", "a"*(1024*1024*10))

        await asyncio.gather(
            *[read_blob(foo_client,"bar") for _ in range(1000)],
            write_to_blob(foo_client, "bar", "b"* (1024*1024*1)))

if __name__ == "__main__":
    print("trying to break blob storage")
    asyncio.run(test())
