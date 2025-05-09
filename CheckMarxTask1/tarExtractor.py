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
