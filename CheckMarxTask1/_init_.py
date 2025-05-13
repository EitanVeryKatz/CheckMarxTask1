from typing import List
from VersionFetcher import getLatestVersion
from PackageDownloader import downloadPackage, extractFile
from DependancyParser import findDependencyFiles

def DownloadExtractAndFindDependanciesOfLastVersion(i_package):
    """  
    Downloads the latest version of a package, extracts it, and finds its dependencies.  

    Args:  
        i_package (str): The name of the package to process.  

    Returns:  
        List[str]: A list of dependencies found in the package.  
                   Returns an empty list if an error occurs during the process.  
    """  
    try:
        version = getLatestVersion(i_package)
        downloadFilePath = downloadPackage(i_package, version)
        extractedFile = extractFile(downloadFilePath,)
        dependanciesList = findDependencyFiles(extractedFile)
        return dependanciesList
        
    except:
        return []
    
