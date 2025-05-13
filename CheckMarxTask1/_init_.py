from typing import List
from VersionFetcher import getLatestVersion
from PackageDownloader import downloadPackage, extractFile
from DependancyParser import findDependencyFiles

def DownloadExtractAndFindDependanciesOfLastVersion(i_package):
    try:
        version = getLatestVersion(i_package)
        downloadFilePath = downloadPackage(i_package, version)
        extractedFile = extractFile(downloadFilePath,)
        dependanciesList = findDependencyFiles(extractedFile)
        return dependanciesList
        
    except:
        return []
    
