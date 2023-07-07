c = get_config()

## Authenticator Setting
# Use custom authenticator
# c.JupyterHub.authenticator_class = 'jwtauth.JwtAuth'
c.JupyterHub.authenticator_class = 'dummy'

## Spawner Settings
# Use custom spawner
# c.JupyterHub.spawner_class = 'filespawner.FileSpawner'
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Default image for user server containers
c.DockerSpawner.image = 'jupyter/datascience-notebook'

# Network used to communicate with user containers
c.DockerSpawner.network_name = 'jupyter'

# Delete containers when they are stopped
c.DockerSpawner.remove = True
