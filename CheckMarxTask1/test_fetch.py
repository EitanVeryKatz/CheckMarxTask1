
from version_fetcher import getLatestVersion
from downloadPackage import download_package

pkg = input("Enter package name: ")
version = getLatestVersion(pkg)

if version:
    print(f"Latest version of '{pkg}': {version}")
    file = download_package(pkg, version)
    if file:
        print(f"Downloaded file: {file}")
    else:
        print("Failed to download the package.")
    
else:
    print("Failed to fetch version.")
