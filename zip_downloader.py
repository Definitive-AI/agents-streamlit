import os
import requests
import zipfile
from urllib.parse import urlparse

def download_and_unzip(zip_url):
    """
    Download a zip file from the given URL and unzip it in a new folder
    in the executing file's directory.
    
    :param zip_url: URL of the zip file to download
    :return: Path to the extracted folder
    """
    # Get the filename from the URL
    filename = os.path.basename(urlparse(zip_url).path)
    
    # Download the zip file
    response = requests.get(zip_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download the file. Status code: {response.status_code}")
    
    # Save the zip file
    with open(filename, 'wb') as file:
        file.write(response.content)
    
    # Create a new folder for extraction
    current_directory = os.getcwd()
    folder_name = os.path.join(os.path.dirname(current_directory), "agents")
    os.makedirs(folder_name, exist_ok=True)
    
    # Unzip the file
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(folder_name)
    
    # Remove the zip file
    os.remove(filename)
    
    return os.path.abspath(folder_name)

# Example usage
if __name__ == "__main__":
    url = "https://example.com/sample.zip"
    extracted_folder = download_and_unzip(url)
    print(f"Files extracted to: {extracted_folder}")
