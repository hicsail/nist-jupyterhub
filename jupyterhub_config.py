c = get_config()

## Network Settings
# we need the hub to listen on all ips when it is in a container
c.JupyterHub.hub_ip = '0.0.0.0'
# the hostname/ip that should be used to connect to the hub
# this is usually the hub container's name
c.JupyterHub.hub_connect_ip = 'jupyterhub'

## Authenticator Setting
# Use null authenticator so login is only possible through API
c.JupyterHub.authenticator_class = 'null'

## Spawner Settings
# Use custom spawner
c.JupyterHub.spawner_class = 'filespawner.FileSpawner'

# Default image for user server containers
c.DockerSpawner.image = 'jupyter/datascience-notebook'

# Network used to communicate with user containers
c.DockerSpawner.network_name = 'jupyterhub'

# Delete containers when they are stopped
c.DockerSpawner.remove = True
