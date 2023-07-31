from dotenv import load_dotenv
import os
import pathlib

# Load environment variables, assume the .env file is in the same directory
# as this config file
config_dir = pathlib.Path(__file__).parent.resolve()
env_file_path = config_dir / '.env'
print(env_file_path)
load_dotenv(dotenv_path=env_file_path)

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


# Network used to communicate with user containers
c.DockerSpawner.network_name = 'jupyterhub'

# Delete containers when they are stopped
c.DockerSpawner.remove = True

## API Settings
# Create the NIST service
c.JupyterHub.services = [
    { 'name': 'service-NIST', 'api_token': os.getenv('SERVICE_API_TOKEN') }
]

# Grant NIST service account admin privledges
c.JupyterHub.load_roles = [
    {
        'name': 'service-role',
        'scopes': [
            # Ability to control users
            'admin:users',
            # Ability to start/stop/delete servers
            'admin:servers',
            # Ability to make tokens
            'tokens',
            # See current users
            'list:users'
        ],
        'services': [
            # assign the service the above permissions
            'service-NIST'
        ],
    }
]
