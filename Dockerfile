# Start with JupyterHub base
ARG JUPYTERHUB_VERSION=4.0.1
FROM jupyterhub/jupyterhub:$JUPYTERHUB_VERSION

# Install custom spawner
COPY filespawner /tmp/filespawner
RUN cd /tmp/filespawner && python3 -m pip install .

# Include jupyter hub config
COPY jupyterhub_config.py /srv/jupyterhub_config.py

CMD ["jupyterhub", "-f", "/srv/jupyterhub_config.py"]
