#!/usr/bin/env python3
import json
import urllib.request
import ssl
import sys

FIREBASE_URL = "https://siena-snowy-adventure-default-rtdb.firebaseio.com"

if len(sys.argv) < 4:
    print("Usage: update_firebase_version.py <version> <download_url> <changelog> [file_size_mb] [channel]")
    print("  channel: 'production' (default) or 'staging'")
    sys.exit(1)

version = sys.argv[1]
download_url = sys.argv[2]
changelog = sys.argv[3]
file_size_mb = int(sys.argv[4]) if len(sys.argv) > 4 else 112
channel = sys.argv[5] if len(sys.argv) > 5 else 'production'

version_data = {
    "latest": version,
    "download_url": download_url,
    "changelog": changelog,
    "file_size_mb": file_size_mb
}

# Choose endpoint based on channel
if channel == 'staging':
    url = f"{FIREBASE_URL}/version-staging.json"
    print(f"🧪 Updating STAGING channel...")
else:
    url = f"{FIREBASE_URL}/version.json"
    print(f"🚀 Updating PRODUCTION channel...")

json_data = json.dumps(version_data).encode('utf-8')
req = urllib.request.Request(url, data=json_data, method='PUT', headers={'Content-Type': 'application/json'})

try:
    ssl_context = ssl._create_unverified_context()
    response = urllib.request.urlopen(req, context=ssl_context)
    print(f"✅ Firebase {channel} channel updated to v{version}")
    print(json.dumps(version_data, indent=2))
except Exception as e:
    print(f"❌ Error: {e}")
