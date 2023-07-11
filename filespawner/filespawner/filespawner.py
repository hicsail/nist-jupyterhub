from docker.utils.build import tempfile
from dockerspawner import DockerSpawner
from dockerspawner.dockerspawner import asyncio
from tornado import web
import os
import tarfile
import aiohttp
import aiofiles
from io import BytesIO
import time


async def copy_to(docker, src, container_id):
    srcname = os.path.basename(src)
    tar = tarfile.open(src + '.tar', mode='w')
    try:
        tar.add(srcname)
    finally:
        tar.close()

    data = open(src + '.tar', 'rb').read()
    await docker('put_archive', container=container_id, path='/home/jovyan', data=data)



class FileSpawner(DockerSpawner):
    async def send_to_container(self, file_data: bytes):
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
                tarinfo = tarfile.TarInfo(name='test.ipynb')
                tarinfo.size = len(file_data)
                tarinfo.mtime = int(time.time())
                tar.addfile(tarinfo, BytesIO(file_data))

            # Copy the contents to the docker file
            data_stream.seek(0)
            return data_stream

        # Build the tar
        loop = asyncio.get_event_loop()
        tar_data = await loop.run_in_executor(None, build_tar_blocking)

        await self.docker('put_archive', container=self.container_id, path='/home/jovyan', data=tar_data)

    async def add_file(self, file_url: str):
        """
        Download the file and add the file to the running container
        """
        # Download the file into a temporary files
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                async with aiofiles.tempfile.NamedTemporaryFile('wb', dir='.') as file:
                    # Download the file
                    file_data = await response.content.read()

                    # Send the file into the container
                    # Ignore type checking, leveraging named python file
                    await self.send_to_container(file_data)  # type: ignore

    async def start(self):
        # Get the URL of the file to download
        file_url = self.user_options.get('fileURL', None)
        if file_url is None:
            raise web.HTTPError(400, 'Missing fileURL')

        """
        # Download and save the file
        request = requests.get(file_url)
        open('file.ipynb', 'wb').write(request.content)
        """

        # Start the docker notebook
        result = await super().start()

        await self.add_file(file_url)

        return result
