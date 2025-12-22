"""Quick test to check Firebase read access"""
import urllib.request
import json
from dotenv import load_dotenv
import os

load_dotenv()

firebase_url = os.environ.get('FIREBASE_URL')
print(f"Testing Firebase read access...")
print(f"URL: {firebase_url}")

# Try simple read without orderBy
try:
    url = f"{firebase_url.rstrip('/')}/leaderboards/level_1.json"
    print(f"\nTesting simple GET: {url}")

    req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read().decode('utf-8')
        scores = json.loads(data)
        print(f"✅ Simple GET works! Found {len(scores) if scores else 0} scores")
        if scores:
            print(f"Sample keys: {list(scores.keys())[:3]}")
except Exception as e:
    print(f"❌ Simple GET failed: {e}")

# Try with orderBy
try:
    url = f"{firebase_url.rstrip('/')}/leaderboards/level_1.json?orderBy=\"time\"&limitToFirst=10"
    print(f"\nTesting GET with orderBy: {url}")

    req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read().decode('utf-8')
        scores = json.loads(data)
        print(f"✅ orderBy GET works! Found {len(scores) if scores else 0} scores")
except urllib.error.HTTPError as e:
    print(f"❌ orderBy GET failed: {e.code} - {e.reason}")
    try:
        error_body = e.read().decode('utf-8')
        print(f"Error details: {error_body}")
    except:
        pass
except Exception as e:
    print(f"❌ orderBy GET failed: {e}")
