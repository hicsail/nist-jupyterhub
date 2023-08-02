# Start with JupyterHub base
ARG JUPYTERHUB_VERSION=2.3.1
FROM jupyterhub/jupyterhub:$JUPYTERHUB_VERSION

# Install custom spawner
COPY filespawner /tmp/filespawner
RUN cd /tmp/filespawner && python3 -m pip install .

# Include jupyter hub config
COPY jupyterhub_config.py /srv/jupyterhub_config.py
COPY .env /srv/.env

# Install top level requirements
COPY requirements.txt /srv/requirements.txt
RUN pip install -r /srv/requirements.txt

CMD ["jupyterhub", "-f", "/srv/jupyterhub_config.py"]
