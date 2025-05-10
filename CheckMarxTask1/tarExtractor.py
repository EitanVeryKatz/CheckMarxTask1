import ast
from tkinter import N
import requests
from doctest import debug_script
from msilib.schema import File
import ast
import tarfile
import os
import sys
import toml




def extractFile(i_filepath, i_extract_to):
    try:
        print("began extraction process")
        limitedPathLengthsOS = ("win32","win64")
        if sys.platform in limitedPathLengthsOS:
            i_extract_to = os.path.abspath(i_extract_to)
            if not i_extract_to.startswith("\\\\?\\"):
                i_extract_to = f"\\\\?\\{i_extract_to}"
                

        if i_filepath.endswith(".tar.gz") or i_filepath.endswith(".tar"):
            #tarball extraction 
             with tarfile.open(i_filepath, "r:gz") as tar:
                tar.extractall(path=i_extract_to)
        elif i_filepath.endswith(".tar"):
            #zip extraction
            with tarfile.open(i_filepath, "r") as tar:
                tar.extractall(path=i_extract_to)
                
        print(f"Extracted to {i_extract_to}")
        return True
    
    except Exception as exceptionMessage:
        print(f"Failed to extract tarball: {exceptionMessage}")
        return False






# def findDependencyFiles(i_extractPath):
    
#     potentialFiles = ["setup.py", "pyproject.toml", "requirements.txt"]
#     found = {}

#     for root, dirs, files in os.walk(i_extractPath):
#         for name in potentialFiles:
#             if name in files:
#                 full_path = os.path.join(root, name)
#                 with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
#                     found[name] = f.read()
#                     print(f"Found item {name} in {full_path}")
                    
#     for fileName in potentialFiles:
#         if fileName not in found:
#             print(f"{fileName} not found")
            
#     return parseRequirements(found)



def findDependencyFiles(i_extractPath):
    potentialFiles = {"setup.py", "pyproject.toml", "requirements.txt"}
    found = {}
    metadata_path = None

    for root, dirs, files in os.walk(i_extractPath):
        for name in potentialFiles:
            if name in files:
                full_path = os.path.join(root, name)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    found[name] = f.read()
                    print(f"Found item {name} in {full_path}")
                    
        for dirname in dirs:
            if dirname.endswith(".dist-info"):
                candidate = os.path.join(root, dirname, "METADATA")
                if os.path.isfile(candidate):
                    metadata_path = candidate
                    break 
                
    if metadata_path:
        try:
            with open(metadata_path, "r", encoding="utf-8", errors="ignore") as f:
                found["METADATA"] = f.read()
                print(f"Found item METADATA in {metadata_path}")
        except Exception as e:
            print(f"Failed to read METADATA in {metadata_path}: {e}")
    

  
    for fileName in potentialFiles:
        if fileName not in found:
            print(f"{fileName} not found")

    return parseRequirements(found)
























#get list of all dependancies   
def parseRequirements(i_requirements):
    dependencies = []
    
    # Check if any of the files are present
    for fileName, fileContent in i_requirements.items():
        if fileName == "setup.py":
            ParseSetupPy(fileContent,dependencies)
        elif fileName == "pyproject.toml":
            # Parse pyproject.toml for dependencies
            parse_pyproject_toml(fileContent,dependencies)  
        elif fileName == "requirements.txt":
            # Parse requirements.txt for dependencies
            parse_requirements_txt(fileContent,dependencies)
            
    # Remove duplicates
    dependencies = list(set(dependencies))
    print(f"Dependencies found: {dependencies}")
    
    return dependencies



def parse_requirements_txt(fileContent, dependancies):
    lines = fileContent.splitlines()
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            dependancies.append(line)
            print(f"added dependancy {line} from requirements.txt")
    return None


def ParseSetupPy(i_setupPy,dependancies):
    
    class SetupVisitor(ast.NodeVisitor):
        
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id == "setup":
                for keyword in node.keywords:
                    if "require" in keyword.arg:
                        if isinstance(keyword.value, ast.Dict):
                            for item in keyword.value.values:
                                searchDependenciesInAstObject(item, dependancies)
                        elif isinstance(keyword.value, ast.List):
                            for item in keyword.value.elts:
                                searchDependenciesInAstObject(item, dependancies)


                                
            self.generic_visit(node)

    tree = ast.parse(i_setupPy)
    try:
         visitor = SetupVisitor()
         visitor.visit(tree)
    except Exception as e:
        print(f"Error parsing setup.py: {e}")
        
    return None

def searchDependenciesInAstObject(item, dependancies):
    string_value = None
    if isinstance(item, ast.Str):  # For Python <3.8
        string_value = item.s
    elif isinstance(item, ast.Constant) and isinstance(item.value, str):
        string_value = item.value
    if string_value:
        dependancies.append(string_value)
        print(f"added dependancy {string_value} from setup.py")
    return None


def parse_pyproject_toml(path,dependancies):
    try:
        data = toml.loads(path)
        if "build-system" in data and "requires" in data["build-system"]:
            for item in data["build-system"]["requires"]:
                if isinstance(item, str):
                    dependancies.append(item)
                    print(f"added dependancy {item} from toml")
    except Exception as e:
        print(f"Error parsing pyproject.toml: {e}")
    return None
        



def download_package(i_package_name, i_version, i_download_dir="Downloads"):
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
    

def getLatestVersion(i_packageName):
    """
    Receives package name
    Returns the latest version of the package
    or None if failed to retrieve
    """
    # Corrected the URL
    url = f"https://pypi.org/pypi/{i_packageName}/json"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        packageData = response.json()
        return packageData["info"]["version"]  # Fixed variable name
    except requests.exceptions.RequestException as exeptionMessage:
        print(f"Failed to get version info for '{i_packageName}'. Error message: {exeptionMessage}")
        return None
    


def main():
    pkg = input("Enter package name: ")
    version = getLatestVersion(pkg)

    if version:
        print(f"Latest version of '{pkg}': {version}")
        file = download_package(pkg, version)
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
        

def extract_whl(i_filepath, i_extract_to):
    try:
        print("began extraction process")
        limitedPathLengthsOS = ("win32","win64")
        if sys.platform in limitedPathLengthsOS:
            i_extract_to = os.path.abspath(i_extract_to)
            if not i_extract_to.startswith("\\\\?\\"):
                i_extract_to = f"\\\\?\\{i_extract_to}"
                

       
    
    except Exception as exceptionMessage:

        print(f"Failed to extract tarball: {exceptionMessage}")
        return False


if __name__ == "__main__":
    main()