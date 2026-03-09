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

## Building for Multiple Architectures (Raspberry Pi, ARM, etc.)

If you want to build and publish images for multiple architectures (linux/amd64, linux/arm64, linux/arm/v7), use Docker Buildx:

### Setup Buildx (One-time)

```bash
# Enable experimental Docker features
docker buildx create --name multiarch --driver docker-container
docker buildx use multiarch
```

### Build and Push Multi-Arch Image

```bash
# Build for multiple architectures and push directly to Docker Hub
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t venanciofuentes/github-unfollow:latest \
  -t venanciofuentes/github-unfollow:v1.0 \
  --push \
  .
```

### Build Specific Version with Multi-Arch

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t venanciofuentes/github-unfollow:v1.0.1 \
  --push \
  .
```

### One-Liner for Multi-Arch Build

```bash
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t venanciofuentes/github-unfollow:latest -t venanciofuentes/github-unfollow:v1.0 --push .
```

### Supported Platforms

With this approach, your image will work on:
- **linux/amd64** - Standard PC, Macs with Intel
- **linux/arm64** - Raspberry Pi 3B+, 4, 5 (64-bit)
- **linux/arm/v7** - Older Raspberry Pi, 32-bit ARM devices

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
| `docker build -t github-unfollow .` | Build local image (single arch) |
| `docker buildx build --platform ... -t TAG --push .` | Build multi-arch & push |
| `docker tag github-unfollow venanciofuentes/github-unfollow:TAG` | Tag image |
| `docker login` | Login to Docker Hub |
| `docker push venanciofuentes/github-unfollow:TAG` | Push to Docker Hub |
| `docker pull venanciofuentes/github-unfollow:latest` | Pull latest from Docker Hub |
| `docker images` | List local images |
| `docker rmi IMAGE_ID` | Delete local image |
| `docker buildx ls` | List buildx builders |
| `docker buildx inspect` | Check buildx builder details |

---

**Repository:** https://hub.docker.com/r/venanciofuentes/github-unfollow
