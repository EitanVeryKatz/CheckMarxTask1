
import requests

def getLatestVersion(i_packageName):
    """
    recieves Package name
    returns Latest version of package 
    or None if failed to recieve
    """


    url = f"https://pypi.org/project/{i_packageName}//json"
    
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        packageData = response.json()
        return data["info"]["version"]
    
    except requests.exceptions.RequestException as exeptionMessage:
        print(f"Failed to get Version info for '{i_packageName}'.\
               Error message: ")
        return None
        
