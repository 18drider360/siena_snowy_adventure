"""Check if .env is being loaded properly"""
import os
import sys

print("=" * 60)
print("Environment Loading Test")
print("=" * 60)

print(f"\nCurrent working directory: {os.getcwd()}")
print(f"Script location: {os.path.dirname(os.path.abspath(__file__))}")

print("\n1. BEFORE loading .env:")
print(f"   SIENA_ONLINE_ENABLED: {os.environ.get('SIENA_ONLINE_ENABLED', 'NOT SET')}")
print(f"   FIREBASE_URL: {os.environ.get('FIREBASE_URL', 'NOT SET')}")

print("\n2. Loading .env file...")
from dotenv import load_dotenv

# Try loading from current directory
env_path = os.path.join(os.getcwd(), '.env')
print(f"   Looking for .env at: {env_path}")
print(f"   File exists: {os.path.exists(env_path)}")

loaded = load_dotenv()
print(f"   load_dotenv() returned: {loaded}")

print("\n3. AFTER loading .env:")
print(f"   SIENA_ONLINE_ENABLED: {os.environ.get('SIENA_ONLINE_ENABLED', 'NOT SET')}")
print(f"   FIREBASE_URL: {os.environ.get('FIREBASE_URL', 'NOT SET')}")

print("\n4. Checking .env file contents:")
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        contents = f.read()
        print("   .env file contents:")
        for line in contents.split('\n'):
            if line.strip() and not line.startswith('#'):
                print(f"      {line}")
else:
    print("   ❌ .env file not found!")

print("\n5. Checking hardcoded defaults in secure_leaderboard.py:")
print("   These should work even without .env file:")

# Import after .env loading attempt
from src.utils.secure_leaderboard import get_secure_leaderboard, ONLINE_ENABLED

print(f"   ONLINE_ENABLED constant: {ONLINE_ENABLED}")

lb = get_secure_leaderboard()
print(f"   Leaderboard available: {lb.is_available()}")
print(f"   Leaderboard base_url: {lb.base_url}")

print("\n" + "=" * 60)
print("CONCLUSION:")
if lb.is_available():
    print("✅ Online features should work (either from .env or hardcoded defaults)")
else:
    print("❌ Online features NOT working - check configuration")
print("=" * 60)
