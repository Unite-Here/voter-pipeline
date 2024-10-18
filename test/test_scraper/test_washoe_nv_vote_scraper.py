from unittest.mock import Mock

import pytest
from civis.tests import create_client_mock

from lib.scraper.washoe_nv_vote_scraper import WashoeNVVoteScraper, WCNVScraperError


# Test get_all_votes success
def test_get_all_votes_success(mocker):
    # Fake variable
    fake_client = create_client_mock()
    fake_scraper = WashoeNVVoteScraper(fake_client)

    # Mock function calls
    mock_get_raw_votes_from_link = mocker.patch(
        "lib.scraper.washoe_nv_vote_scraper.WashoeNVVoteScraper.get_raw_votes_from_link")
    mock_process_votes = mocker.patch("lib.scraper.washoe_nv_vote_scraper.WashoeNVVoteScraper.process_votes")

    # Call get_all_votes
    fake_scraper.get_all_votes()

    # Assert functions called
    mock_get_raw_votes_from_link.assert_called()
    mock_process_votes.assert_called()


# Test get_all_votes fail
def test_get_all_votes_fail(mocker):
    # Fake variable
    fake_client = create_client_mock()
    fake_scraper = WashoeNVVoteScraper(fake_client)

    # Mock function calls
    mocker.patch("lib.scraper.washoe_nv_vote_scraper.WashoeNVVoteScraper.get_raw_votes_from_link",
                 side_effect=Exception)

    # Assert exception raised
    with pytest.raises(WCNVScraperError, match=r"Error getting all votes"):
        fake_scraper.get_all_votes()


# Test get_raw_votes_from_link success
def test_get_raw_votes_from_link_success(mocker):
    # Fake variables
    fake_client = create_client_mock()
    fake_scraper = WashoeNVVoteScraper(fake_client)
    fake_dict_list = [{
        "voter_id": "000",
        "date_returned": "2000-01-01"
    }, {
        "voter_id": "111",
        "date_returned": "2000-01-01"
    }, {
        "voter_id": "",
        "date_returned": ""
    }]
    expected_dict_list = [{
        "voter_id": "000",
        "date_returned": "2000-01-01"
    }, {
        "voter_id": "111",
        "date_returned": "2000-01-01"
    }]

    # Mock function calls
    mock_get_latest_link = mocker.patch("lib.scraper.washoe_nv_vote_scraper.WashoeNVVoteScraper.get_latest_link",
                                        return_value="fake.site")
    mock_download_file = mocker.patch("lib.scraper.washoe_nv_vote_scraper.download_file")
    mock_xlsx_to_csv = mocker.patch("lib.scraper.washoe_nv_vote_scraper.xlsx_to_csv")
    mock_delete_csv_headers = mocker.patch("lib.scraper.washoe_nv_vote_scraper.delete_csv_headers")
    mock_csv_to_dict_list = mocker.patch("lib.scraper.washoe_nv_vote_scraper.csv_to_dict_list",
                                         return_value=fake_dict_list)

    # Call get_raw_votes_from_link function
    fake_scraper.get_raw_votes_from_link()

    # Assert all functions called and data set correctly
    mock_get_latest_link.assert_called()
    mock_download_file.assert_called()
    mock_xlsx_to_csv.assert_called()
    mock_delete_csv_headers.assert_called()
    mock_csv_to_dict_list.assert_called()
    assert fake_scraper.raw_votes == expected_dict_list


# Test get_raw_votes_from_link fail
def test_get_raw_votes_from_link_fail(mocker):
    # Fake variables
    fake_client = create_client_mock()
    fake_scraper = WashoeNVVoteScraper(fake_client)

    # Mock function calls
    mocker.patch("lib.scraper.washoe_nv_vote_scraper.WashoeNVVoteScraper.get_latest_link", return_value="fake.site")
    mocker.patch("lib.scraper.washoe_nv_vote_scraper.download_file", side_effect=Exception)

    # Assert exception raised correctly
    with pytest.raises(WCNVScraperError, match=r"Error getting votes from link"):
        fake_scraper.get_raw_votes_from_link()


# Test process_votes success
def test_process_votes_success():
    # Fake variables
    fake_client = create_client_mock()
    fake_scraper = WashoeNVVoteScraper(fake_client)
    fake_votes = [{
        "voter_id": "123456",
        "county": "WASHOE_COUNTY",
        "category": "EV",
        "party": "NP",
        "precinct": "0000",
        "city": "big city",
        "election_code": "0000",
        "date_returned": "2000-01-01",
    }, {
        "voter_id": "654321",
        "county": "WASHOE_COUNTY",
        "category": "EV",
        "party": "NP",
        "precinct": "0000",
        "city": "big city",
        "party": "NP",
        "election_code": "0000",
        "date_returned": "2000-01-01",
    }]

    # Set raw_votes to fake values
    fake_scraper.raw_votes = fake_votes

    # Call process votes
    fake_scraper.process_votes()

    # Assert clean votes contains corret data
    assert len(fake_scraper.clean_votes) == 2
    assert fake_scraper.clean_votes[0].get_idnumber() == fake_votes[0]["voter_id"]
    assert fake_scraper.clean_votes[1].get_idnumber() == fake_votes[1]["voter_id"]


# Test process_votes fail
def test_process_votes_fail():
    # Fake variables
    fake_client = create_client_mock()
    fake_scraper = WashoeNVVoteScraper(fake_client)
    fake_votes = [{"Bad": "Value"}]

    # Set raw_votes to fake values
    fake_scraper.raw_votes = fake_votes

    # Assert exception is raised
    with pytest.raises(WCNVScraperError, match=r"Error processing votes"):
        fake_scraper.process_votes()
