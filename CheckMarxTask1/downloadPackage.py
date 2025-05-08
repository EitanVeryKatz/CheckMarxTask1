import os
import requests

def download_package(i_package_name, i_version, i_download_dir="downloads"):
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
        os.makedirs(download_dir, exist_ok=True)
        filepath = os.path.join(download_dir, filename)

        # Download the file
        print(f"Downloading {filename}...")
        file_response = requests.get(download_url, stream=True)
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