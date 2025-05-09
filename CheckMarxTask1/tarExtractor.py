import tarfile

def extractTarball(i_filepath, i_extract_to):
    try:
        with tarfile.open(i_filepath, "r:gz") as tar:
            tar.extractall(path=i_extract_to)
        print(f"Extracted to {i_extract_to}")
        return True
    
    except Exception as exceptionMessage:
        print(f"Failed to extract tarball: {exceptionMessage}")
        return False
