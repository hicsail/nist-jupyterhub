from dockerspawner import DockerSpawner
from dockerspawner.dockerspawner import asyncio
from tornado import web
import tarfile
import aiohttp
import aiofiles
from io import BytesIO
import time


class FileSpawner(DockerSpawner):
    async def send_to_container(self, file_data: bytes, file_name: str):
        """
        Send the file to the container
        """
        def build_tar_blocking():
            """
            Blocking for construction of tarball
            """
            data_stream = BytesIO()

            # Make the tarball
            with tarfile.open(fileobj=data_stream, mode='w') as tar:
                tarinfo = tarfile.TarInfo(name=file_name)
                tarinfo.size = len(file_data)
                tarinfo.mtime = int(time.time())
                tar.addfile(tarinfo, BytesIO(file_data))

            # Copy the contents to the docker file
            data_stream.seek(0)
            return data_stream

        # Build the tar
        loop = asyncio.get_event_loop()
        tar_data = await loop.run_in_executor(None, build_tar_blocking)

        # Copy the tar to the container
        await self.docker('put_archive', container=self.container_id, path='/home/jovyan', data=tar_data)

    async def add_file(self, file_url: str, file_name: str):
        """
        Download the file and add the file to the running container
        """
        # Download the file into a temporary files
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                # Download the file
                file_data = await response.content.read()

        # Send the file into the container
        # Ignore type checking, leveraging named python file
        await self.send_to_container(file_data, file_name)  # type: ignore

    async def start(self):
        # Get the URL and name of the file to download
        file_url = self.user_options.get('fileURL', None)
        if file_url is None:
            raise web.HTTPError(400, 'Missing fileURL')
        file_name = self.user_options.get('fileName', None)
        if file_name is None:
            raise web.HTTPError(400, 'Unknown file name')

        # Start the docker notebook
        result = await super().start()

        # Copy the file to the container
        await self.add_file(file_url, file_name)

        return result
