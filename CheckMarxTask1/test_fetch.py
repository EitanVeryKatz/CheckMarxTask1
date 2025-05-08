
from version_fetcher import getLatestVersion

pkg = input("Enter package name: ")
version = getLatestVersion(pkg)

if version:
    print(f"Latest version of '{pkg}': {version}")
else:
    print("Failed to fetch version.")
