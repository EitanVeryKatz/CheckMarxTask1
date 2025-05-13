import requests

def getLatestVersion(i_packageName):
    """  
    Retrieves the latest version of a package from the PyPI repository.  

    Args:  
        i_packageName (str): The name of the package to query.  

    Returns:  
        str: The latest version of the package as a string if successful.  
        None: If the request fails or the package information cannot be retrieved.  

    Raises:  
        requests.exceptions.RequestException: If there is an issue with the HTTP request.  
    """  
  
    url = f"https://pypi.org/pypi/{i_packageName}/json"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        packageData = response.json()
        return packageData["info"]["version"]  # Fixed variable name
    except requests.exceptions.RequestException as exeptionMessage:
        print(f"Failed to get version info for '{i_packageName}'. Error message: {exeptionMessage}")
        return None
