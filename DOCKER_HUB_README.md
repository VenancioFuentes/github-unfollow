# GitHub Unfollow Docker Image

Fast and safe way to unfollow all users you follow on GitHub using multithreading and respecting API rate limits.

## Quick Start

```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_ABC123xyz venanciofuentes/github-unfollow
```

Replace `ghp_ABC123xyz` with your GitHub personal access token.

## Features

- ⚡ **4 concurrent workers** - 4x faster than sequential execution
- 🛡️ **Rate limit aware** - Automatically pauses if rate limit runs low
- 📊 **Real-time progress** - Shows which users are unfollowed and remaining API requests
- ✅ **Safe** - Asks for confirmation before unfollowing anyone
- 📦 **Ultra-lightweight** - Only 50MB with Alpine Linux
- 🔒 **Secure** - Token passed via environment variable, never stored in image

## Usage Examples

### With token inline (simplest)

```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_ABC123xyz venanciofuentes/github-unfollow
```

### With .env file

```bash
docker run --rm -i --env-file .env venanciofuentes/github-unfollow
```

### With environment variable

**PowerShell:**
```powershell
$TOKEN = "ghp_ABC123xyz"
docker run --rm -i -e GITHUB_TOKEN=$TOKEN venanciofuentes/github-unfollow
```

**Bash:**
```bash
export TOKEN="ghp_ABC123xyz"
docker run --rm -i -e GITHUB_TOKEN=$TOKEN venanciofuentes/github-unfollow
```

## How to Get Your GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" (classic)
3. Select **only** the `user:follow` scope
4. Click "Generate token"
5. Copy the token and use it above

## Image Details

- **Base:** `python:3.11-alpine` - Ultra-lightweight official image
- **Size:** ~50MB
- **Entrypoint:** Runs `python unfollow.py`
- **Stdin:** Enabled for interactive prompts (use `-i` flag)

## Docker Flags Explained

```bash
docker run --rm -i -e GITHUB_TOKEN=... venanciofuentes/github-unfollow
```

- `--rm` - Auto-delete container after exit (clean up)
- `-i` - Keep stdin open for interactive prompts
- `-t` - Allocate pseudo-TTY (optional, for colors)
- `-e GITHUB_TOKEN=...` - Set environment variable with token

Full example with all options:
```bash
docker run --rm -it -e GITHUB_TOKEN=ghp_xyz venanciofuentes/github-unfollow
```

## Available Tags

- `latest` - Always the most recent stable version
- `v1.0`, `v1.1`, etc. - Specific version releases

**Example using specific version:**
```bash
docker run --rm -i -e GITHUB_TOKEN=ghp_xyz venanciofuentes/github-unfollow:v1.0
```

## Supported Platforms

- Linux (amd64, arm64)
- macOS (Intel, Apple Silicon)
- Windows with Docker Desktop

## What It Does

1. ✅ Reads your GitHub token from environment variable
2. ✅ Fetches the list of all users you follow (with pagination)
3. ✅ Shows you the list and asks for confirmation
4. ✅ Unfollows each user using 4 concurrent threads
5. ✅ Monitors GitHub API rate limit in real-time
6. ✅ Pauses automatically if rate limit runs low
7. ✅ Shows summary with success/failure stats

## Rate Limiting

GitHub API allows 5000 requests per hour. The script:
- Shows remaining requests after each unfollow
- Automatically pauses for 60 seconds if below 100 remaining
- Continues gracefully once rate limit has recovered

## Security

- ✅ Token passed via environment variable (not in image)
- ✅ No credentials logged or printed
- ✅ Uses minimal `user:follow` scope only
- ✅ Container deleted after use with `--rm`

## Repository

Full source code and documentation: https://github.com/VenancioFuentes/github-unfollow

## License

MIT
