 
from __init__ import DownloadExtractAndFindDependanciesOfLastVersion  


def main():  
    """  
    Main function to prompt the user for a package name and display its dependencies.  

    This function takes user input for a package name, calls the  
    `DownloadExtractAndFindDependanciesOfLastVersion` function to process the package,  
    and prints the list of dependencies found.  
    """  
    package = input("Enter package name: ")  
    print(DownloadExtractAndFindDependanciesOfLastVersion(package))  


if __name__ == "__main__":  
    main()  