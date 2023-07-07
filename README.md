# NIST JupyterHub

## Development Instructions

1. Create network

```bash
docker network create jupyterhub
```

2. Create volume

```bash
docker volume create jupyterhub
```

3. Build Docker Image

```bash
docker build -t hub . --no-cache
```

4. Run the deployment

```bash
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jupyterhub:/srv/jupyterhub \
  --net jupyterhub \
  --name jupyterhub \
  -p8000:8000\
  hub
```
