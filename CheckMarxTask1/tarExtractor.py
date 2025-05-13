
from VersionFetcher import getLatestVersion
from PackageDownloader import downloadPackage, extractFile
from DependancyParser import findDependencyFiles









    


def main():
    pkg = input("Enter package name: ")
    version = getLatestVersion(pkg)

    if version:
        print(f"Latest version of '{pkg}': {version}")
        file = downloadPackage(pkg, version)
        if file:
            print(f"Downloaded file: {file}")
            if extractFile(file, "extracted"):
                print(f"Extracted to 'extracted' directory.")
                return findDependencyFiles("extracted")
            else:
                print("Failed to extract the tarball.")
        else:
            print("Failed to download the package.")
    
    else:
        print("Failed to fetch version.")
        



if __name__ == "__main__":
    main()