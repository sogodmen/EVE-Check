import subprocess
import sys
import json
from pathlib import Path

def is_package_installed(package_name):
    try:
        if sys.version_info >= (3, 8):
            from importlib.metadata import distribution
            distribution(package_name)
        else:
            import pkg_resources
            pkg_resources.get_distribution(package_name)
        return True
    except:
        return False

def load_packages_from_json(json_path="install_packages.json"):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("packages", [])
    except FileNotFoundError:
        print(f"⚠ File {json_path} not found! Empty package list used.")
        return []
    except json.JSONDecodeError:
        print(f"⚠ JSON format error in file {json_path}! An empty list is used.")
        return []

def install_packages():
    packages = load_packages_from_json()
    if not packages:
        print("❌ The package list is empty or not loaded. Check install_packages.json.")
        return

    print("🔍 Checking and installing packages...")
    for package in packages:
        if is_package_installed(package):
            print(f"✅ Already installed: {package}")
            continue
        
        try:
            print(f"⬇ Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Successfully: {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation error {package}: {e}")

if __name__ == "__main__":
    print("🚀 Start installing dependencies...")
    install_packages()

    print("🎉 Done! All packages have been checked.")
