import csv
import os
from zipfile import ZipFile

import openpyxl
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


def csv_to_dict_list(csv_file: str, has_header: bool, headers: list[str], file_encoding: str = "utf-8") -> list[dict]:
    """
    Read csv file into list of dictionaries
    Parameters:
        csv_file (string): Path to csv file being read
        has_header (boolean): Whether or not the csv file has a header row
        headers (list): List of header strings to use as fieldnames
        file_encoding (string): File encoding, defaults to "utf-8"
    Returns:
        data: List of dictionaries
    """
    data = []
    try:
        with open(csv_file, "r", encoding=file_encoding) as file:
            reader = csv.DictReader(file, fieldnames=headers)

            for dictionary in reader:
                data.append(dictionary)

            # If header was in file, delete first item in data
            if has_header == True:
                data.pop(0)

        return data
    except Exception as err:
        raise FileUtilsError(f"Reading csv to list failed: {err}")


def delete_csv_headers(csv_file: str, directory: str, file_encoding: str = "utf-8"):
    """
    Delete first row (presumed to be header) from csv file
    Parameters:
        csv_file (string): Path to csv file being edited
        directory (string): Path working directory, not ending in '/'
        file_encoding (string): File encoding, defaults to "utf-8"
    """
    with open(f"{directory}/temp.csv", "w", newline="", encoding=file_encoding) as temp_csv:
        # Write all except first row to temp_csv
        with open(csv_file, "r") as source:
            writer = csv.writer(temp_csv)
            reader = csv.reader(source)
            for index, row in enumerate(reader):
                if index != 0:
                    writer.writerow(row)

    with open(f"{directory}/temp.csv", "r", newline="", encoding=file_encoding) as temp_csv:
        # Overwrite csv file from temp_csv
        with open(csv_file, "w", newline="", encoding=file_encoding) as destination:
            writer = csv.writer(destination)
            reader = csv.reader(temp_csv)
            for row in reader:
                writer.writerow(row)

    # Delete temporary file
    os.remove(f"{directory}/temp.csv")


def xlsx_to_csv(xlsx_file: str, csv_file: str, file_encoding: str = "utf-8"):
    """
    Read xlsx file to csv
    Parameters:
        xlsx_file (string): Path to xlsx file being read
        csv_file (string): Path to csv file being written
        file_encoding (string): File encoding, defaults to "utf-8"
    """
    excel = openpyxl.load_workbook(xlsx_file)
    sheet = excel.active
    if sheet is not None:
        with open(csv_file, "w", newline="", encoding=file_encoding) as file:
            writer = csv.writer(file)
            for row in sheet.rows:
                writer.writerow(cell.value for cell in row)
