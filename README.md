# GitHub Unfollow Script

Fast and safe Python script to unfollow all users you follow on GitHub. Uses **multithreading** to speed up the process while respecting API rate limits.

**📦 Published on Docker Hub:** https://hub.docker.com/r/venanciofuentes/github-unfollow

## One-Liner Quickstart

No installation, no cloning, just Docker:

```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_ABC123xyz venanciofuentes/github-unfollow
```

Replace `ghp_ABC123xyz` with your GitHub token. That's it!

## Features

✨ **Key Features:**
- ⚡ **4 concurrent workers** - 4x faster than sequential execution
- 🛡️ **Rate limit aware** - Automatically pauses if rate limit runs low
- 📊 **Real-time progress** - Shows which users are unfollowed and remaining API requests
- 🔒 **Secure** - Token stored in `.env` file (not versioned)
- ✅ **Safe** - Asks for confirmation before unfollowing anyone
- 📋 **Comprehensive logging** - Shows success/failure for each user

## Quick Start

### Option 1: Docker (Fastest - No Setup Required!)

**Already published on Docker Hub!** https://hub.docker.com/r/venanciofuentes/github-unfollow

Just run:

```bash
# Pass your GitHub token directly
docker run --rm -i -e GITHUB_TOKEN=ghp_ABC123xyz venanciofuentes/github-unfollow

# Or with .env file
docker run --rm -i --env-file .env venanciofuentes/github-unfollow
```

**Or from Docker Compose:**

```bash
docker compose run --rm unfollow
```

That's it! No cloning, no setup, no venv. Just Docker.

---

### Option 2: Local Installation (Best for Development)

#### 1. Create virtual environment

**Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Windows (cmd):**
```bash
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Linux/macOS (manual):**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Configure your token

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and paste your GitHub token:
```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 3. Run the script

**Local:**
```bash
# With venv activated
python unfollow.py

# Or using helper script (Linux/macOS)
./unfollow.sh local
```

---


**Step 1: Clone the repository**

```bash
git clone https://github.com/VenancioFuentes/github-unfollow.git
cd github-unfollow
```

**Step 2: Build the image**

```bash
docker build -t github-unfollow .
```

**Step 3: Run the container**

```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_ABC123xyz github-unfollow
```

---

## Get your GitHub Token

1. Go to **https://github.com/settings/tokens**
2. Click **"Generate new token"** (classic)
3. Give it a name (e.g., "GitHub Unfollow")
4. Select **only** the `user:follow` scope
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)

---

## Get your GitHub Token

1. Go to **https://github.com/settings/tokens**
2. Click **"Generate new token"** (classic)
3. Give it a name (e.g., "GitHub Unfollow")
4. Select **only** the `user:follow` scope
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)

---

## How to Choose Your Installation Method

| Method | Best For | Setup Time | Runtime | Cleanup |
|--------|----------|-----------|---------|---------|
| **Docker (Published)** | One-time use, no setup | ~1 sec (pull) | 25 sec | Auto (`--rm`) ✅ |
| **Local + venv** | Development, modifications | 2 min | 25 sec | Manual (but simple) |
| **Docker (Local build)** | Testing locally first | 1-2 min | 25 sec | Auto (`--rm`) |
| **Docker Compose** | Team projects, CI/CD | 1 min | 25 sec | Auto |

## Quick Comparison

### Fastest Way (Docker Published Image)
```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_xxx venanciofuentes/github-unfollow
```
✅ No install, no clone, just Docker + token = done

**Docker Hub:** https://hub.docker.com/r/venanciofuentes/github-unfollow

### Development Way (Local)
```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
python unfollow.py
```
✅ Good for making changes to the code

---

## Image Registry

The published image is available on Docker Hub:

### Docker Hub

**Repository:** https://hub.docker.com/r/venanciofuentes/github-unfollow

```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_ABC123xyz venanciofuentes/github-unfollow
```

**Pull image:**
```bash
docker pull venanciofuentes/github-unfollow
```

**Pull specific version:**
```bash
docker pull venanciofuentes/github-unfollow:v1.0
```

### Available Tags

Images are typically published with these tags:
- `latest` - Always the most recent stable version
- `v1.0`, `v1.1`, etc. - Specific version releases
- `v1-latest` - Latest patch for major version 1
- `main` - Built from main branch (development)

**Example using a specific version:**
```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_xxx venanciofuentes/github-unfollow:v1.0
```

## Performance
| Setup | Time for 100 users | Time for 500 users |
|-------|---|---|
| Sequential (1 worker) | ~100 seconds | ~500 seconds |
| **This script (4 workers)** | **~25 seconds** | **~125 seconds** |

**Why it's fast:**
- Requests run in parallel, not waiting for each response
- 4 concurrent threads minimize idle time
- Smart rate limit handling prevents wasted requests

## Threading & Rate Limiting

### How Threads Work

- **4 concurrent workers** submit unfollow requests in parallel
- Threads finish independently - results are processed as they complete
- ThreadPoolExecutor manages thread lifecycle automatically

### Rate Limit Protection

GitHub API allows **5000 requests per hour** for authenticated requests:
- The script monitors `X-RateLimit-Remaining` header after each request
- If remaining requests < 100, it pauses for 60 seconds
- After pause, API limit has likely reset, continues gracefully
- Shows remaining count in real-time so you can see progress

### Customizing Concurrency

To change the number of concurrent workers, edit `unfollow.py`:

```python
# Line 135 - Change 4 to your desired number
with ThreadPoolExecutor(max_workers=4) as executor:
```

**Recommendation:**
- `max_workers=2` - Very conservative, safer for accounts with restrictions
- `max_workers=4` - **Default, balanced approach**
- `max_workers=8` - Faster, but be careful near rate limits

## Security

⚠️ **Important Security Notes:**

1. **Token Protection**
   - `.env` file is in `.gitignore` - won't be committed
   - Never share your token with anyone
   - Tokens in `.env` are never logged or printed
   - Use tokens with minimal permissions (`user:follow` only)

2. **Token Scope**
   - This script only needs `user:follow` permission
   - Don't grant more permissions than necessary
   - You can revoke tokens anytime at https://github.com/settings/tokens

3. **Local Storage**
   - Keep `.env` file local (don't push to git)
   - Delete or rotate your token after running if desired
   - Consider using a temporary token just for this script

## Troubleshooting

### Error: "GITHUB_TOKEN not found"
- Run `cp .env.example .env` to create `.env` file
- Make sure you've pasted your token in `.env`
- Check that there are no extra spaces: `GITHUB_TOKEN=ghp_xxx` ✓

### Error: "Invalid or expired token"
- Your token may have expired or been revoked
- Go to https://github.com/settings/tokens and generate a new one
- Update `.env` with the new token

### Error: "Insufficient permissions"
- Your token doesn't have `user:follow` scope
- Delete the old token and generate a new one with `user:follow` selected

### Script runs but unfollows fail silently
- Check your internet connection
- Verify the API is working: `curl https://api.github.com/user`
- Make sure your account doesn't have 2FA restrictions on API tokens

### Rate limit exceeded (X-RateLimit-Remaining: 0)
- Wait 1 hour for the limit to reset
- Alternatively, use a token from a different account if available
- Consider reducing `max_workers` to go slower

### PowerShell execution policy error
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Example Output

```
Fetching following list...

Total users you are following: 42
First 10 users:
  - octocat
  - torvalds
  - gvanrossum
  - guido
  - wycats
  - rails
  - golang
  - mozilla
  - kubernetes
  - docker
  ... and 32 more

Do you want to unfollow 42 users? (y/n): y

Unfollowing 42 users with 4 concurrent threads...

[1/42] ✓ octocat (Remaining: 4999)
[2/42] ✓ torvalds (Remaining: 4998)
[3/42] ✓ gvanrossum (Remaining: 4997)
[4/42] ✓ guido (Remaining: 4996)
[5/42] ✓ wycats (Remaining: 4995)
...
[42/42] ✓ docker (Remaining: 4958)

--- Results ---
Successful unfollows: 42
Errors: 0
Total: 42
Remaining API requests: 4958
```

## Project Structure

```
github-unfollow/
├── venv/                    # Virtual environment (local, generated)
├── unfollow.py             # Main script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── README.md              # Main documentation (this file)
├── DOCKER_BUILD.md        # How to build and publish Docker image
├── DOCKER_HUB_README.md   # Content for Docker Hub page
├── .env.example           # Token configuration example
├── .env                   # Your configuration (local, not versioned)
├── .gitignore            # Git ignore file
└── .dockerignore         # Docker ignore file
```
**Q: Is it safe to use?**
A: Yes. The script only needs `user:follow` permission and never deletes accounts or sensitive data. It only unfollows users you're following.

**Q: Will I get rate limited?**
A: Unlikely. The script monitors rate limits and pauses if necessary. It uses 4 threads which is relatively conservative. For GitHub's 5000 requests/hour, this is safe.

**Q: Can I modify the number of workers?**
A: Yes! Edit line 135 in `unfollow.py` and change `max_workers=4` to your desired number. See "Customizing Concurrency" section above.

**Q: What if the script crashes?**
A: It's designed to be idempotent - you can run it again and it will only unfollow remaining users. It won't try to unfollow the same person twice.

**Q: How long does it take?**
A: For 100 users: ~25 seconds. For 1000 users: ~250 seconds (4 minutes). Sequential would take 100-1000+ seconds for the same.

**Q: Can I undo it?**
A: There's no built-in undo. You'll need to manually follow users again. Consider testing with a small batch first!

**Q: What permissions does the token need?**
A: Only `user:follow`. This is the minimal security approach. Other tokens might work but this is recommended.

**Q: Why Alpine instead of Slim?**
A: Alpine images are much smaller (~50MB vs ~150MB for Slim). Alpine is based on musl libc and busybox, making it ideal for lightweight containers. The tradeoff is slightly slower build time, but runtime is identical. For this script, Alpine is perfect.

**Q: How big is the Docker image?**
A: Only ~50MB! This makes it fast to pull and build. Compare:
- Alpine: ~50MB ⭐ (our choice)
- Slim: ~150MB
- Full Python: ~300-400MB

**Q: Can I use the Docker image without .env?**
A: Yes! Pass token directly: `docker run --rm -i -e GITHUB_TOKEN=ghp_xxx github-unfollow`

**Q: Is Docker safe for my token?**
A: Yes. Environment variables are passed to the container, not stored in the image. The `-e` flag keeps it in memory only. Use `--rm` to delete the container after it exits.

**Q: How do I pass my token safely in CI/CD?**
A: Use CI/CD secrets to set environment variables:

```yaml
# GitHub Actions example
- name: Run GitHub Unfollow
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: docker run --rm -i -e GITHUB_TOKEN=$GITHUB_TOKEN github-unfollow
```

**Q: Does it work on Raspberry Pi?**
A: Yes! The published Docker image supports multiple architectures:
- ✅ linux/amd64 (your PC/Mac)
- ✅ linux/arm64 (Raspberry Pi 4/5 with 64-bit OS)
- ✅ linux/arm/v7 (older Raspberry Pi, 32-bit)

Just use the same command: `docker run --rm -i -e GITHUB_TOKEN=ghp_xxx venanciofuentes/github-unfollow`

**Q: I get "no matching manifest" error on my Raspberry Pi**
A: This means the image was built for a single architecture. If you built it yourself, use Docker Buildx to build for multiple architectures. See "Building for Multiple Architectures" section in the Docker section above for detailed instructions.

### Using the Published Image (Recommended)

The image is published on Docker Hub for easy access:

**Docker Hub Repository:** https://hub.docker.com/r/venanciofuentes/github-unfollow

**Supported Architectures:** 
- ✅ linux/amd64 (Intel/AMD PCs, Macs)
- ✅ linux/arm64 (Raspberry Pi 3B+, 4, 5 with 64-bit OS)
- ✅ linux/arm/v7 (32-bit ARM devices, older Raspberry Pi)

```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_ABC123xyz venanciofuentes/github-unfollow
```

**That's it!** No cloning, no setup, no venv. Just one command. Works on your PC, Mac, Raspberry Pi, or any Linux system with Docker.

#### Different ways to use the published image:

**1. With inline token:**
```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_ABC123xyz venanciofuentes/github-unfollow
```

**2. With .env file:**
```bash
docker run --rm -i --env-file .env venanciofuentes/github-unfollow
```

**3. With environment variable (Windows PowerShell):**
```powershell
$TOKEN = "ghp_ABC123xyz"
docker run --rm -i -e GITHUB_TOKEN=$TOKEN venanciofuentes/github-unfollow
```

**4. With environment variable (Linux/macOS):**
```bash
TOKEN="ghp_ABC123xyz"
docker run --rm -i -e GITHUB_TOKEN=$TOKEN venanciofuentes/github-unfollow
```

**5. Using Docker Compose (with .env file):**

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  unfollow:
    image: venanciofuentes/github-unfollow
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    stdin_open: true
    tty: true
```

Then run:
```bash
docker compose run --rm unfollow
```

---

### Building the Image Locally

If you prefer to build the image yourself:

#### Step 1: Clone the repository

```bash
git clone https://github.com/VenancioFuentes/github-unfollow.git
cd github-unfollow
```

#### Step 2: Build the image

```bash
docker build -t github-unfollow .

# Or with tags
docker build -t github-unfollow:latest -t github-unfollow:v1.0 .
```

#### Step 3: Run the container

```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_ABC123xyz github-unfollow
```

---

### Building for Multiple Architectures (Raspberry Pi Support)

If you want to publish images that work on Raspberry Pi, ARM devices, and regular PCs:

#### Step 1: Setup Docker Buildx (one-time)

```bash
# Create a buildx builder for multi-architecture builds
docker buildx create --name multiarch --driver docker-container
docker buildx use multiarch
```

#### Step 2: Build and Push Multi-Arch Image

```bash
# Build for amd64 (Intel/AMD), arm64 (Raspberry Pi 64-bit), and arm/v7 (32-bit ARM)
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t venanciofuentes/github-unfollow:latest \
  -t venanciofuentes/github-unfollow:v1.0 \
  --push \
  .
```

**That's it!** The image now works on all architectures:
- Your PC/Mac ✅
- Raspberry Pi 4/5 (64-bit) ✅
- Older Raspberry Pi (32-bit) ✅
- Any Linux system with Docker ✅

For more details, see [DOCKER_BUILD.md](DOCKER_BUILD.md).

---

### Publishing Your Image

To share your image on Docker Hub or GitHub Container Registry:

#### Pushing to Docker Hub:

```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag github-unfollow venanciofuentes/github-unfollow:latest

# Push to Docker Hub
docker push venanciofuentes/github-unfollow:latest
```

To update existing tags:

```bash
# Tag with version
docker tag github-unfollow venanciofuentes/github-unfollow:v1.0

# Push
docker push venanciofuentes/github-unfollow:v1.0
```

---

## How to Build and Publish the Docker Image

### Complete Workflow

This is the complete process to build and publish a new version:

#### 1. Update your code (if needed)

Make changes to `unfollow.py`, `requirements.txt`, etc.

#### 2. Build the image locally

```bash
docker build -t github-unfollow .
```

This creates a local image tagged as `github-unfollow`.

#### 3. Tag the image for Docker Hub

```bash
# Tag for latest
docker tag github-unfollow venanciofuentes/github-unfollow:latest

# Tag with version
docker tag github-unfollow venanciofuentes/github-unfollow:v1.0
```

#### 4. Login to Docker Hub

```bash
docker login
# Enter your Docker Hub credentials
```

#### 5. Push to Docker Hub

```bash
# Push latest
docker push venanciofuentes/github-unfollow:latest

# Push version tag
docker push venanciofuentes/github-unfollow:v1.0
```

#### 6. Verify on Docker Hub

Visit https://hub.docker.com/r/venanciofuentes/github-unfollow to verify the new images are published.

### Quick One-Liner (after code changes)

```bash
docker build -t github-unfollow . && \
docker tag github-unfollow venanciofuentes/github-unfollow:latest && \
docker tag github-unfollow venanciofuentes/github-unfollow:v1.0 && \
docker login && \
docker push venanciofuentes/github-unfollow:latest && \
docker push venanciofuentes/github-unfollow:v1.0
```

### Important: Always Update Version Tags

When pushing a new version, use semantic versioning:

```bash
# For bug fixes
docker tag github-unfollow venanciofuentes/github-unfollow:v1.0.1
docker push venanciofuentes/github-unfollow:v1.0.1

# For minor features
docker tag github-unfollow venanciofuentes/github-unfollow:v1.1.0
docker push venanciofuentes/github-unfollow:v1.1.0

# For major changes
docker tag github-unfollow venanciofuentes/github-unfollow:v2.0.0
docker push venanciofuentes/github-unfollow:v2.0.0

# Always keep latest updated
docker tag github-unfollow venanciofuentes/github-unfollow:latest
docker push venanciofuentes/github-unfollow:latest
```

### What Gets Published

When you push to Docker Hub, users can pull and run:

```bash
# Latest version
docker run --rm -i -e GITHUB_TOKEN=ghp_xxx venanciofuentes/github-unfollow

# Specific version
docker run --rm -i -e GITHUB_TOKEN=ghp_xxx venanciofuentes/github-unfollow:v1.0

# Development version
docker run --rm -i -e GITHUB_TOKEN=ghp_xxx venanciofuentes/github-unfollow:main
```

---

---

### Docker Image Details

- **Base Image:** `python:3.11-alpine` (official, secure, ultra-lightweight)
- **Image Size:** ~50MB total (vs 150MB+ with other Python images)
- **Workdir:** `/app`
- **Entrypoint:** `python unfollow.py`
- **Stdin/TTY:** Add `-it` flags for interactive prompts
- **Cleanup:** Use `--rm` flag to auto-delete container after exit

### Understanding the docker run flags

```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_xxx venanciofuentes/github-unfollow
```

- `--rm` - Automatically remove container after it exits (clean up)
- `-i` - Keep stdin open even if not attached (for interactive prompts)
- `-t` - Allocate a pseudo-TTY (for colors in output)
- `-e GITHUB_TOKEN=...` - Set environment variable for the token
- `venanciofuentes/github-unfollow` - Image reference

**Optional flags:**
- `--name mycontainer` - Give container a custom name
- `--env-file .env` - Load all environment variables from .env file

**Full example with all options:**
```bash
docker run --rm -it -e GITHUB_TOKEN=ghp_xxx venanciofuentes/github-unfollow
```

### Quick Docker Reference

| Task | Command |
|------|---------|
| **Use published image** | `docker run --rm -i -e GITHUB_TOKEN=ghp_xxx venanciofuentes/github-unfollow` |
| **Build locally** | `docker build -t github-unfollow .` |
| **Run locally built image** | `docker run --rm -i -e GITHUB_TOKEN=ghp_xxx github-unfollow` |
| **With .env file** | `docker run --rm -i --env-file .env venanciofuentes/github-unfollow` |
| **With Docker Compose** | `docker compose run --rm unfollow` |
| **Pull latest version** | `docker pull venanciofuentes/github-unfollow:latest` |
- 📦 **No installation** - Just Docker (works everywhere)
- 🚀 **Ultra-fast** - Published images pull in seconds
- 🔄 **Reproducible** - Same behavior on any system
- 🧹 **Isolated** - Doesn't affect your system
- 🗑️ **Auto-cleanup** - Use `--rm` to delete after done
- 📉 **Lightweight** - Only 50MB with Alpine
- ☁️ **Cloud-ready** - Works in GitHub Actions, CI/CD, etc.

---

---

## Updating Docker Hub Description

The file `DOCKER_HUB_README.md` contains the description to use on Docker Hub's repository page.

To update the Docker Hub description:

1. Go to https://hub.docker.com/r/venanciofuentes/github-unfollow
2. Click the "Edit" button or go to Repository settings
3. Copy the content from `DOCKER_HUB_README.md`
4. Paste it into the "Full description" field on Docker Hub
5. Save changes

This keeps the Docker Hub page in sync with the repository documentation.

---

## License

MIT - Feel free to use and modify as needed.
