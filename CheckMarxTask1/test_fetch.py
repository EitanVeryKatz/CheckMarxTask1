
from version_fetcher import getLatestVersion

pkg = input("Enter package name: ")
version = get_latest_version(pkg)

if version:
    print(f"Latest version of '{pkg}': {version}")
else:
    print("Failed to fetch version.")
