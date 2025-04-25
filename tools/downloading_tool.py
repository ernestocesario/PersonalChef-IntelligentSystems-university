from exceptions.DownloadErrorException import DownloadErrorException
import requests

'''
def downloader_tool(link: str) -> dict:
    """
    Retrieves the flyer of a specific supermarket

    Returns:
        dict: 
    """
    download_from_link(link, "./volantino.pdf")
    return {"result": None}
'''


def download_from_link(url, outputPath) -> None:
    try:
        response = requests.get(url, stream=True)

        response.raise_for_status()

        with open(outputPath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    except requests.exceptions.RequestException as e:
        raise DownloadErrorException