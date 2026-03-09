# Docker Build & Publish Quick Reference

## Build and Publish Complete Workflow

```bash
# 1. Make code changes if needed
# (edit unfollow.py, requirements.txt, etc.)

# 2. Build the image locally
docker build -t github-unfollow .

# 3. Tag for Docker Hub (latest + version)
docker tag github-unfollow venanciofuentes/github-unfollow:latest
docker tag github-unfollow venanciofuentes/github-unfollow:v1.0

# 4. Login to Docker Hub
docker login

# 5. Push to Docker Hub
docker push venanciofuentes/github-unfollow:latest
docker push venanciofuentes/github-unfollow:v1.0

# 6. Verify at https://hub.docker.com/r/venanciofuentes/github-unfollow
```

## One-Liner

```bash
docker build -t github-unfollow . && docker tag github-unfollow venanciofuentes/github-unfollow:latest && docker tag github-unfollow venanciofuentes/github-unfollow:v1.0 && docker login && docker push venanciofuentes/github-unfollow:latest && docker push venanciofuentes/github-unfollow:v1.0
```

## Semantic Versioning for Releases

```bash
# Bug fix version (v1.0.1)
docker tag github-unfollow venanciofuentes/github-unfollow:v1.0.1
docker push venanciofuentes/github-unfollow:v1.0.1

# Minor version (v1.1.0)
docker tag github-unfollow venanciofuentes/github-unfollow:v1.1.0
docker push venanciofuentes/github-unfollow:v1.1.0

# Major version (v2.0.0)
docker tag github-unfollow venanciofuentes/github-unfollow:v2.0.0
docker push venanciofuentes/github-unfollow:v2.0.0

# Always update latest
docker tag github-unfollow venanciofuentes/github-unfollow:latest
docker push venanciofuentes/github-unfollow:latest
```

## Verify Build

```bash
# Test the locally built image
docker run --rm -i -e GITHUB_TOKEN=ghp_ABC123xyz github-unfollow

# Or if testing from Docker Hub after push
docker run --rm -i -e GITHUB_TOKEN=ghp_ABC123xyz venanciofuentes/github-unfollow:latest
```

## Common Commands

| Command | Purpose |
|---------|---------|
| `docker build -t github-unfollow .` | Build local image |
| `docker tag github-unfollow venanciofuentes/github-unfollow:TAG` | Tag image |
| `docker login` | Login to Docker Hub |
| `docker push venanciofuentes/github-unfollow:TAG` | Push to Docker Hub |
| `docker pull venanciofuentes/github-unfollow:latest` | Pull latest from Docker Hub |
| `docker images` | List local images |
| `docker rmi IMAGE_ID` | Delete local image |

---

**Repository:** https://hub.docker.com/r/venanciofuentes/github-unfollow
