# GitHub Unfollow Script

Fast and safe Python script to unfollow all users you follow on GitHub. Uses **multithreading** to speed up the process while respecting API rate limits.

## Features

✨ **Key Features:**
- ⚡ **4 concurrent workers** - 4x faster than sequential execution
- 🛡️ **Rate limit aware** - Automatically pauses if rate limit runs low
- 📊 **Real-time progress** - Shows which users are unfollowed and remaining API requests
- 🔒 **Secure** - Token stored in `.env` file (not versioned)
- ✅ **Safe** - Asks for confirmation before unfollowing anyone
- 📋 **Comprehensive logging** - Shows success/failure for each user

## Quick Start

### 1. Clone/Setup the project

```bash
cd github-unfollow
```

### 2. Create virtual environment

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

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Get your GitHub Token

1. Go to **https://github.com/settings/tokens**
2. Click **"Generate new token"** (classic)
3. Give it a name (e.g., "GitHub Unfollow")
4. Select **only** the `user:follow` scope
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)

### 4. Configure the script

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit `.env` and paste your token:

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5. Run the script

```bash
python unfollow.py
```

## How It Works

```
1. Activate virtual environment
2. Script reads token from .env
3. Fetches list of all users you follow (paginated)
4. Shows the list and asks for confirmation
5. Unfollows users using 4 concurrent threads
6. Monitors API rate limit in real-time
7. Pauses automatically if rate limit drops below 100
8. Shows summary with success/failure stats
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
├── venv/                    # Virtual environment (generated)
├── unfollow.py             # Main script
├── requirements.txt        # Dependencies
├── .env.example           # Configuration example
├── .env                   # Your configuration (local, not versioned)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## FAQ

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

## Requirements

- Python 3.7+
- Internet connection
- GitHub personal access token with `user:follow` scope

## License

MIT - Feel free to use and modify as needed.
