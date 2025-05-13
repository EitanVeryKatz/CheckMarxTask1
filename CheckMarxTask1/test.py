from _init_ import DownloadExtractAndFindDependanciesOfLastVersion


def main():
    package = input("Enter package name: ")
    print(DownloadExtractAndFindDependanciesOfLastVersion(package))



if __name__ == "__main__":
    main()