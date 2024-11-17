"""Check if all required dependencies are installed."""
import importlib.util
import sys
from typing import Dict, List

def check_package(package_name: str) -> bool:
    """Check if a package is installed."""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

# List of required packages and their import names
REQUIRED_PACKAGES = {
    'torch': 'torch',
    'transformers': 'transformers',
    'moviepy': 'moviepy',
    'tenacity': 'tenacity',
    'diskcache': 'diskcache',
    'pexels-api': 'pexels_api',
    'pixabay-python': 'pixabay',
    'python-unsplash': 'unsplash',
    'python-dotenv': 'dotenv',
}

def main():
    """Main function to check dependencies."""
    missing_packages = []
    installed_packages = []
    
    print("Checking required packages...")
    print("-" * 50)
    
    for package, import_name in REQUIRED_PACKAGES.items():
        if check_package(import_name):
            installed_packages.append(package)
            print(f"✅ {package:<20} - Installed")
        else:
            missing_packages.append(package)
            print(f"❌ {package:<20} - Missing")
    
    print("\nSummary:")
    print(f"Total packages required: {len(REQUIRED_PACKAGES)}")
    print(f"Installed: {len(installed_packages)}")
    print(f"Missing: {len(missing_packages)}")
    
    if missing_packages:
        print("\nMissing packages:")
        print("pip install " + " ".join(missing_packages))
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
