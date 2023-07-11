from dockerspawner import DockerSpawner
import requests
from tornado import web
import docker
import os
import tarfile


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
    async def start(self):
        # Get the URL of the file to download
        file_url = self.user_options.get('fileURL', None)
        if file_url is None:
            raise web.HTTPError(400, 'Missing fileURL')

        # Download and save the file
        request = requests.get(file_url)
        open('file.ipynb', 'wb').write(request.content)

        # Pass the file to the notebook

        # Start the docker notebook
        result = await super().start()

        # Pass the file to the container
        await copy_to(self.docker, 'file.ipynb', self.container_id)

        return result
