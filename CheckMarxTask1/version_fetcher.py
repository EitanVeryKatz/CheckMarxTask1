import requests

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