#!/usr/bin/env python3
"""Script to unfollow all users you follow on GitHub."""

import os
import requests
from dotenv import load_dotenv
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from threading import Lock

# Load environment variables from .env file
load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_API_URL = 'https://api.github.com'

# Thread-safe counters
counter_lock = Lock()
unfollowed_count = 0
failed_count = 0
rate_limit_remaining = 5000


def get_following_list() -> List[str]:
    """Get the list of users you are following."""
    if not GITHUB_TOKEN:
        raise ValueError('GITHUB_TOKEN is not configured in the .env file')
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    following = []
    page = 1
    
    print('Fetching following list...')
    
    while True:
        try:
            response = requests.get(
                f'{GITHUB_API_URL}/user/following',
                headers=headers,
                params={'per_page': 100, 'page': page}
            )
            response.raise_for_status()
            
            users = response.json()
            if not users:
                break
            
            for user in users:
                following.append(user['login'])
            
            page += 1
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise ValueError('Invalid or expired token')
            elif response.status_code == 403:
                raise ValueError('Insufficient permissions')
            else:
                raise e
    
    return following


def unfollow_user(username: str) -> tuple:
    """Unfollow a specific user. Returns (username, success, remaining_requests)"""
    if not GITHUB_TOKEN:
        raise ValueError('GITHUB_TOKEN is not configured in the .env file')
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        response = requests.delete(
            f'{GITHUB_API_URL}/user/following/{username}',
            headers=headers
        )
        
        # Get remaining requests from response headers
        remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        
        response.raise_for_status()
        return (username, True, remaining)
    except requests.exceptions.HTTPError as e:
        remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        return (username, False, remaining)


def main():
    """Main function."""
    global unfollowed_count, failed_count, rate_limit_remaining
    
    try:
        # Get following list
        following = get_following_list()
        total = len(following)
        
        if total == 0:
            print('You are not following anyone.')
            return
        
        print(f'\nTotal users you are following: {total}')
        print('\nFirst 10 users:')
        for user in following[:10]:
            print(f'  - {user}')
        
        if total > 10:
            print(f'  ... and {total - 10} more')
        
        # Confirmation
        confirm = input(f'\nDo you want to unfollow {total} users? (y/n): ').strip().lower()
        
        if confirm != 'y':
            print('Operation cancelled.')
            return
        
        # Unfollowing with multiple threads
        print(f'\nUnfollowing {total} users with {4} concurrent threads...\n')
        
        unfollowed_count = 0
        failed_count = 0
        rate_limit_remaining = 5000
        
        # Use ThreadPoolExecutor for concurrent requests
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all unfollow tasks
            futures = {executor.submit(unfollow_user, username): username for username in following}
            
            # Process completed tasks as they finish
            completed = 0
            for future in as_completed(futures):
                completed += 1
                try:
                    username, success, remaining = future.result()
                    
                    with counter_lock:
                        rate_limit_remaining = remaining
                        
                        if success:
                            unfollowed_count += 1
                            status = '✓'
                        else:
                            failed_count += 1
                            status = '✗'
                        
                        print(f'[{completed}/{total}] {status} {username} (Remaining: {remaining})')
                    
                    # Check if we're running low on rate limit
                    if remaining < 100:
                        print(f'\n⚠️  WARNING: Rate limit running low ({remaining} remaining). Pausing for 60 seconds...')
                        time.sleep(60)
                
                except Exception as e:
                    with counter_lock:
                        failed_count += 1
                    print(f'[{completed}/{total}] ✗ Error with {futures[future]}: {e}')
        
        print(f'\n--- Results ---')
        print(f'Successful unfollows: {unfollowed_count}')
        print(f'Errors: {failed_count}')
        print(f'Total: {total}')
        print(f'Remaining API requests: {rate_limit_remaining}')
        
    except ValueError as e:
        print(f'Configuration error: {e}')
        exit(1)
    except requests.exceptions.ConnectionError:
        print('Connection error. Check your internet connection.')
        exit(1)
    except Exception as e:
        print(f'Unexpected error: {e}')
        exit(1)


if __name__ == '__main__':
    main()
