 
import imp  
import requests  
import tarfile  
import os  
import zipfile  
import sys  

def downloadPackage(i_package_name, i_version, i_download_dir="Downloads"):  
    """  
    Downloads a specific version of a package from PyPI and saves it to a specified directory.  

    Args:  
        i_package_name (str): The name of the package to download.  
        i_version (str): The version of the package to download.  
        i_download_dir (str, optional): The directory where the package will be saved. Defaults to "Downloads".  

    Returns:  
        str: The file path of the downloaded package if successful.  
        None: If the download fails or the package version is not found.  
    """  
    url = f"https://pypi.org/pypi/{i_package_name}/json"  

    try:  
        response = requests.get(url, timeout=10)  
        response.raise_for_status()  
        data = response.json()  
        print("got Json data")  

        # Check if the version exists  
        release_files = data["releases"][i_version]  
        tarball = next((f for f in release_files if f["packagetype"] == "sdist"), None)  

        # If no tarball found,  
        if tarball is None:  
            print("No source distribution (.tar.gz) found.")  
            return None  
        else:  
            print("got tarball")  

        download_url = tarball["url"]  
        filename = tarball["filename"]  

        # Create the download directory if it doesn't exist  
        os.makedirs(i_download_dir, exist_ok=True)  
        print("got download dir")  
        filepath = os.path.join(i_download_dir, filename)  
        print("got filepath")  

        # Download the file  
        print(f"Downloading {filename}...")  
        file_response = requests.get(download_url, stream=True)  
        print(f"got file response{file_response.status_code}")  
        file_response.raise_for_status()  

        # Save the file to the specified directory  
        with open(filepath, "wb") as f:  
            for chunk in file_response.iter_content(chunk_size=8192):  
                f.write(chunk)  

        print(f"Downloaded to: {filepath}")  
        return filepath  

    except Exception as e:  
        print(f"Error downloading package: {e}")  
        return None  


def extractFile(i_filePath, i_extract_to="extracted"):  
    """  
    Extracts a compressed package file (e.g., .tar.gz or .whl) to a specified directory.  

    Args:  
        i_filePath (str): The file path of the compressed package to extract.  
        i_extract_to (str, optional): The directory where the package will be extracted. Defaults to "extracted".  

    Returns:  
        str: The path to the top-level extracted folder if successful.  
        list: An empty list if the extraction fails.  
    """  
    try:  
        print("began extraction process")  
        limited_path_lengths_OS = ("win32", "win64")  
        if sys.platform in limited_path_lengths_OS:  
            i_extract_to = os.path.abspath(i_extract_to)  
            if not i_extract_to.startswith("\\\\?\\"):  
                i_extract_to = f"\\\\?\\{i_extract_to}"  

        # Ensure the extraction directory exists  
        os.makedirs(i_extract_to, exist_ok=True)  

        # Get a snapshot of existing files in the directory before extraction  
        existing_files = set(os.listdir(i_extract_to))  
        extracted_files = []  # List to store paths of newly extracted files  

        if i_filePath.endswith(".tar.gz") or i_filePath.endswith(".tar"):  
            # Tarball extraction  
            with tarfile.open(i_filePath, "r:gz") as tar:  
                tar.extractall(path=i_extract_to)  

                extracted_file = tar.getmembers()[0].name.split("/")[0]  

        elif i_filePath.endswith(".whl"):  
            # Zip extraction  
            with zipfile.ZipFile(i_filePath, 'r') as whl_file:  
                whl_file.extractall(i_extract_to)  

        print(f"Extracted to {i_extract_to}")  
        return f"{i_extract_to}\\{extracted_file}"  

    except Exception as exceptionMessage:  
        print(f"Failed to extract tarball: {exceptionMessage}")  
        return []  