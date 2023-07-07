from dockerspawner import DockerSpawner

class FileSpawner(DockerSpawner):
    def options_from_query(self, query_data):
        print('query data')
        print(query_data)
        return super().options_from_query(query_data)

    async def start(self):
        print('Form Data')
        print(self.user_options)

        print('cmd')
        print(self.cmd)

        return await super().start()
