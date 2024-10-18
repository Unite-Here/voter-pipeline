import csv
import os
import tempfile
from unittest.mock import Mock
from zipfile import ZipFile

import openpyxl
import pytest
import requests

from lib.utils.files import (FileUtilsError, csv_to_dict_list, delete_csv_headers, download_file, unzip_all_files,
                             unzip_file, xlsx_to_csv)


# Test download_file success
def test_download_file_success(requests_mock):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fake variables
        fake_url = "https://www.fake.site/fake.txt"
        fake_dest = f"{tmpdir}/fake.txt"
        fake_data = "Once upon a midnight dreary..."

        # Mock requests.get
        requests_mock.get(fake_url, text=fake_data)

        # Call download_file with fake variables
        download_file(fake_url, fake_dest)

        # Assert path exists and file contents
        assert os.path.exists(fake_dest)
        with open(fake_dest, "r") as f:
            downloaded_data = f.read()
            assert downloaded_data == fake_data


# Test download_file fail
def test_download_file_fail(requests_mock):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fake variables
        fake_url = "https://www.fake.site/fake.txt"
        fake_dest = f"{tmpdir}/fake.txt"

        # Mock requests.get to throw exception
        requests_mock.get(fake_url, exc=requests.exceptions.ConnectionError)

        # Assert exception raised
        with pytest.raises(FileUtilsError, match=r"Downloading file failed"):
            download_file(fake_url, fake_dest)


# Test unzip_file success
def test_unzip_file_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fake variables
        fake_file = f"{tmpdir}/fake.txt"
        fake_zip = f"{tmpdir}/fake.zip"

        # Make temporary file
        open(fake_file, "a").close()

        # Make temporary zip file using temporary file
        with ZipFile(fake_zip, "w") as zip:
            zip.write(fake_file, os.path.basename(fake_file))

        # Remove temporary file
        os.remove(fake_file)

        # Call unzip_file
        unzip_file(fake_zip, os.path.basename(fake_file), tmpdir)

        # Assert file extracted correctly
        assert os.path.exists(fake_file)


# Test unzip_file fail
def test_unzip_file_fail(mocker):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fake variables
        fake_file = f"{tmpdir}/fake.txt"
        fake_zip = f"{tmpdir}/fake.zip"

        # Mock extraction call to throw exception
        mocker.patch("lib.utils.files.ZipFile.extract", side_effect=Exception)

        # Assert exception raised
        with pytest.raises(FileUtilsError, match=r"Unzip file failed"):
            unzip_file(fake_zip, os.path.basename(fake_file), tmpdir)


# Test unzip_all_files success
def test_unzip_all_files_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fake variables
        fake_file_a = f"{tmpdir}/fake_a.txt"
        fake_file_b = f"{tmpdir}/fake_b.txt"
        fake_zip = f"{tmpdir}/fake.zip"

        # Make temporary files
        open(fake_file_a, "a").close()
        open(fake_file_b, "a").close()

        # Make temporary zip file using temporary files
        with ZipFile(fake_zip, "w") as zip:
            zip.write(fake_file_a, os.path.basename(fake_file_a))
            zip.write(fake_file_b, os.path.basename(fake_file_b))

        # Remove temporary files
        os.remove(fake_file_a)
        os.remove(fake_file_b)

        # Call unzip_file
        unzip_all_files(fake_zip, tmpdir)

        # Assert file extracted correctly
        assert os.path.exists(fake_file_a)
        assert os.path.exists(fake_file_b)


# Test unzip_all_files fail
def test_unzip_all_files_fail(mocker):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fake variables
        fake_zip = f"{tmpdir}/fake.zip"

        # Mock extraction call to throw eception
        mocker.patch("lib.utils.files.ZipFile.extractall", side_effect=Exception)

        # Assert exception raised
        with pytest.raises(FileUtilsError, match=r"Unzip all files failed"):
            unzip_all_files(fake_zip, tmpdir)


# Test csv_to_list success
def test_csv_to_dict_list_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fake variables
        fake_headers = ["FRUIT", "COLOR", "TASTE"]
        fake_data = [["Apricot", "Orange", "Tart"], ["Blackberry", "Black", "Tart"], ["Cantaloupe", "Orange", "Sweet"]]
        fake_csv = f"{tmpdir}/fake.csv"
        expected_response = [{
            "FRUIT": "Apricot",
            "COLOR": "Orange",
            "TASTE": "Tart"
        }, {
            "FRUIT": "Blackberry",
            "COLOR": "Black",
            "TASTE": "Tart"
        }, {
            "FRUIT": "Cantaloupe",
            "COLOR": "Orange",
            "TASTE": "Sweet"
        }]

        # Put fake data in temporary csv file
        with open(fake_csv, "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(fake_data)

        # Call csv_to_dict_list
        response = csv_to_dict_list(fake_csv, False, fake_headers)

        # Assert response is as expected
        assert response == expected_response


# Test csv_to_list fail
def test_csv_to_dict_list_fail(mocker):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fake variables
        fake_headers = ["FRUIT", "COLOR", "TASTE"]
        fake_csv = f"{tmpdir}/fake.csv"

        # Mock DictReader to throw exception
        mocker.patch("lib.utils.files.csv.DictReader", side_effect=Exception)

        # Assert exception thrown
        with pytest.raises(FileUtilsError, match=r"Reading csv to list failed"):
            csv_to_dict_list(fake_csv, False, fake_headers)


# test delete_csv_headers
def test_delete_csv_headers():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fake variables
        fake_data = [{
            "FRUIT": "Apricot",
            "COLOR": "Orange",
            "TASTE": "Tart"
        }, {
            "FRUIT": "Blackberry",
            "COLOR": "Black",
            "TASTE": "Tart"
        }, {
            "FRUIT": "Cantaloupe",
            "COLOR": "Orange",
            "TASTE": "Sweet"
        }]
        fake_keys = ["FRUIT", "COLOR", "TASTE"]

        with open(f"{tmpdir}/fake.csv", "w", newline="") as outfile:
            dict_writer = csv.DictWriter(outfile, fake_keys)
            dict_writer.writeheader()
            dict_writer.writerows(fake_data)

        # Assert first row is headers
        fake_contents = []
        with open(f"{tmpdir}/fake.csv", "r") as infile:
            reader = csv.reader(infile)
            for d in reader:
                fake_contents.append(d)

        assert fake_contents[0] == fake_keys

        # Call delete_csv_headers
        delete_csv_headers(f"{tmpdir}/fake.csv", tmpdir)

        # Assert file no longer contains headers
        expected = [['Apricot', 'Orange', 'Tart'], ['Blackberry', 'Black', 'Tart'], ['Cantaloupe', 'Orange', 'Sweet']]
        result = []
        with open(f"{tmpdir}/fake.csv", "r") as infile:
            reader = csv.reader(infile)
            for d in reader:
                result.append(d)

        assert result == expected


# test delete_csv_headers
def test_xlsx_to_csv():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fake variables
        fake_data = [[
            "Apricot",
            "Orange",
            "Tart"
        ], [
            "Blackberry",
            "Black",
            "Tart"
        ], [
            "Cantaloupe",
            "Orange",
            "Sweet"
        ]]
        fake_keys = ["FRUIT", "COLOR", "TASTE"]

        fake_wb = openpyxl.Workbook()
        fake_ws = fake_wb.active
        if fake_ws is not None:
            fake_ws.append(fake_keys)
            for data in fake_data:
                fake_ws.append(data)

        fake_wb.save(f"{tmpdir}/fake.xlsx")

        # Call xlsx_to_csv
        xlsx_to_csv(f"{tmpdir}/fake.xlsx", f"{tmpdir}/fake.csv")

        # Assert csv data is as expected
        expected = [{
            "FRUIT": "FRUIT",
            "COLOR": "COLOR",
            "TASTE": "TASTE"
        }, {
            "FRUIT": "Apricot",
            "COLOR": "Orange",
            "TASTE": "Tart"
        }, {
            "FRUIT": "Blackberry",
            "COLOR": "Black",
            "TASTE": "Tart"
        }, {
            "FRUIT": "Cantaloupe",
            "COLOR": "Orange",
            "TASTE": "Sweet"
        }]

        result = []
        with open(f"{tmpdir}/fake.csv", "r") as file:
            reader = csv.DictReader(file, fieldnames=fake_keys)
            for d in reader:
                result.append(d)

        assert result == expected
