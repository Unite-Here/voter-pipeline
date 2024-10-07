import csv
from zipfile import ZipFile

import requests


class FileUtilsError(ValueError):
    pass


def download_file(url: str, dest_path: str) -> None:
    """
    Download file from url to given destination
    Parameters:
        url (string): URL to download file from
        dest_path (string): Name and path to download to
    """
    try:
        r = requests.get(url)
        with open(dest_path, "wb") as f:
            f.write(r.content)
    except Exception as err:
        raise FileUtilsError(f"Downloading file failed: {err}")


def unzip_file(zip_path: str, file_name: str, unzip_path: str) -> None:
    """
    Unzip specific file to destination
    Parameters:
        zip_path (string): Path to zip file
        file_name (string): Name of file to be extracted
        unzip_path (string): Path for unzipped file destination
    """
    try:
        with ZipFile(zip_path, "r") as z_obj:
            z_obj.extract(file_name, path=unzip_path)
    except Exception as err:
        raise FileUtilsError(f"Unzip file failed: {err}")


def unzip_all_files(zip_path: str, unzip_path: str) -> None:
    """
    Unzip all contents of zip file to destination
    Parameters:
        zip_path (string): Path to zip file
        unzip_path (string): Path for unzipped file destination
    """
    try:
        with ZipFile(zip_path, "r") as z_obj:
            z_obj.extractall(path=unzip_path)
    except Exception as err:
        raise FileUtilsError(f"Unzip all files failed: {err}")


def csv_to_dict_list(csv_file: str, headers: list[str], file_encoding: str = "utf-8") -> list[dict]:
    """
    Read csv file into list of dictionaries
    Parameters:
        csv_file (string): Path to csv file being read
        headers (list): List of header strings to use as fieldnames
        file_encoding (string): File encoding, defaults to "utf-8"
    Returns:
        data: List of dictionaries
    """
    try:
        data = []
        file = open(csv_file, "r", encoding=file_encoding)
        reader = csv.DictReader(file, fieldnames=headers)
        for dictionary in reader:
            data.append(dictionary)
        return data
    except Exception as err:
        raise FileUtilsError(f"Reading csv to list failed: {err}")
