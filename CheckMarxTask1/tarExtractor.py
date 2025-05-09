from msilib.schema import File
import tarfile
import os
import sys

def extractTarball(i_filepath, i_extract_to):
    try:
        print("began extraction process")
        limitedPathLengthsOS = ("win32","win64")
        if sys.platform in limitedPathLengthsOS:
            i_extract_to = os.path.abspath(i_extract_to)
            if not i_extract_to.startswith("\\\\?\\"):
                i_extract_to = f"\\\\?\\{i_extract_to}"
                

        with tarfile.open(i_filepath, "r:gz") as tar:
            tar.extractall(path=i_extract_to)
        print(f"Extracted to {i_extract_to}")
        return True
    
    except Exception as exceptionMessage:
        print(f"Failed to extract tarball: {exceptionMessage}")
        return False


def findDependencyFiles(i_extractPath):
    
    potentialFiles = ["setup.py", "pyproject.toml", "requirements.txt"]
    found = {}

    for root, dirs, files in os.walk(i_extractPath):
        for name in potentialFiles:
            if name in files:
                full_path = os.path.join(root, name)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    found[name] = f.read()
                    print(f"Found {name} in {full_path}")
                    
    for fileName in potentialFiles:
        if fileName not in found:
            print(f"{fileName} not found")

    return found