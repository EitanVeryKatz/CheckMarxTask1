
from re import I
from version_fetcher import getLatestVersion
from downloadPackage import download_package
from tarExtractor import extractTarball



def main():
    pkg = input("Enter package name: ")
    version = getLatestVersion(pkg)

    if version:
        print(f"Latest version of '{pkg}': {version}")
        file = download_package(pkg, version)
        if file:
            print(f"Downloaded file: {file}")
            if extractTarball(file, "extracted"):
                print(f"Extracted to 'extracted' directory.")
            else:
                print("Failed to extract the tarball.")
        else:
            print("Failed to download the package.")
    
    else:
        print("Failed to fetch version.")


if __name__ == "__main__":
    main()