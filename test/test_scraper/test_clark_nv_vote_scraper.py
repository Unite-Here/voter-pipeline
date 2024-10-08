from unittest.mock import Mock

import pytest

from lib.scraper.clark_nv_vote_scraper import CCNVScraperError, ClarkNVVoteScraper
from civis.tests import create_client_mock


# Test get_all_votes success
def test_get_all_votes_success(mocker):
    # Fake variable
    fake_client = create_client_mock()
    fake_scraper = ClarkNVVoteScraper(fake_client)

    # Mock function calls
    mock_get_vbm_votes = mocker.patch("lib.scraper.clark_nv_vote_scraper.ClarkNVVoteScraper.get_vbm_votes")
    mock_get_ev_votes = mocker.patch("lib.scraper.clark_nv_vote_scraper.ClarkNVVoteScraper.get_ev_votes")
    mock_process_votes = mocker.patch("lib.scraper.clark_nv_vote_scraper.ClarkNVVoteScraper.process_votes")

    # Call get_all_votes
    fake_scraper.get_all_votes()

    # Assert functions called
    mock_get_vbm_votes.assert_called()
    mock_get_ev_votes.assert_called()
    mock_process_votes.assert_called()


# Test get_all_votes fail
def test_get_all_votes_fail(mocker):
    # Fake variable
    fake_client = create_client_mock()
    fake_scraper = ClarkNVVoteScraper(fake_client)

    # Mock function calls
    mocker.patch("lib.scraper.clark_nv_vote_scraper.ClarkNVVoteScraper.get_vbm_votes", side_effect=Exception)

    # Assert exception raised
    with pytest.raises(CCNVScraperError, match=r"Error getting all votes"):
        fake_scraper.get_all_votes()


# Test get_vbm_votes success
def test_get_vbm_votes_success(mocker):
    # Fake variables
    fake_client = create_client_mock()
    fake_scraper = ClarkNVVoteScraper(fake_client)
    fake_dict_list = [{}, {}]
    expected_dict_list = [{"VOTE_TYPE": "Mail"}, {"VOTE_TYPE": "Mail"}]

    # Mock function calls
    mock_download_file = mocker.patch("lib.scraper.clark_nv_vote_scraper.download_file")
    mock_unzip_file = mocker.patch("lib.scraper.clark_nv_vote_scraper.unzip_file")
    mock_os_rename = mocker.patch("lib.scraper.clark_nv_vote_scraper.os.rename")
    mock_csv_to_dict_list = mocker.patch("lib.scraper.clark_nv_vote_scraper.csv_to_dict_list",
                                         return_value=fake_dict_list)

    # Call get_vbm_votes function
    fake_scraper.get_vbm_votes()

    # Assert all functions called and data set correctly
    mock_download_file.assert_called()
    mock_unzip_file.assert_called()
    mock_os_rename.assert_called()
    mock_csv_to_dict_list.assert_called()
    assert fake_scraper.raw_votes == expected_dict_list


# Test get_vbm_votes fail
def test_get_vbm_votes_fail(mocker):
    # Fake variables
    fake_client = create_client_mock()
    fake_scraper = ClarkNVVoteScraper(fake_client)

    # Mock function call to cause error
    mock_download_file = mocker.patch("lib.scraper.clark_nv_vote_scraper.download_file", side_effect=Exception)

    # Assert exception raised correctly
    with pytest.raises(CCNVScraperError, match=r"Error getting votes by mail"):
        fake_scraper.get_vbm_votes()


# Test get_ev_votes success
def test_get_ev_votes_success(mocker):
    # Fake variables
    fake_client = create_client_mock()
    fake_scraper = ClarkNVVoteScraper(fake_client)
    fake_dict_list = [{}, {}]
    expected_dict_list = [{"VOTE_TYPE": "Early"}, {"VOTE_TYPE": "Early"}]

    # Mock function calls
    mock_download_file = mocker.patch("lib.scraper.clark_nv_vote_scraper.download_file")
    mock_unzip_file = mocker.patch("lib.scraper.clark_nv_vote_scraper.unzip_file")
    mock_os_rename = mocker.patch("lib.scraper.clark_nv_vote_scraper.os.rename")
    mock_csv_to_dict_list = mocker.patch("lib.scraper.clark_nv_vote_scraper.csv_to_dict_list",
                                         return_value=fake_dict_list)

    # Call get_ev_votes function
    fake_scraper.get_ev_votes()

    # Assert all functions called and data set correctly
    mock_download_file.assert_called()
    mock_unzip_file.assert_called()
    mock_os_rename.assert_called()
    mock_csv_to_dict_list.assert_called()
    assert fake_scraper.raw_votes == expected_dict_list


# Test get_ev_votes fail
def test_get_ev_votes_fail(mocker):
    # Fake variables
    fake_client = create_client_mock()
    fake_scraper = ClarkNVVoteScraper(fake_client)

    # Mock function call to cause error
    mock_download_file = mocker.patch("lib.scraper.clark_nv_vote_scraper.download_file", side_effect=Exception)

    # Assert exception raised correctly
    with pytest.raises(CCNVScraperError, match=r"Error getting early votes"):
        fake_scraper.get_ev_votes()


# Test process_votes success
def test_process_votes_success():
    # Fake variables
    fake_client = create_client_mock()
    fake_scraper = ClarkNVVoteScraper(fake_client)
    fake_votes = [{
        "IDNUMBER": "123456",
        "COUNTY": "CLARK_COUNTY",
        "VOTE_TYPE": "Mail",
        "ELECTION_CODE": "0000",
        "ACTIVITY_DATE": "2000-01-01",
        "NAME": "Un Known",
        "PRECINCT": "0",
        "PARTY": "0",
        "PARTY_NAME": "Null Party",
        "CONGRESS": "0",
        "ASSEMBLY": "0",
        "SENATE": "0",
        "COMMISSION": "0",
        "EDUCATION": "0",
        "REGENT": "0",
        "SCHOOL": "0",
        "CITY": "0",
        "WARD": "0",
        "TOWNSHIP": "0",
        "REG_STATUS": "A",
        "VOTE_SITE": "0",
        "BALLOT_PARTY": "NP",
        "REQUEST_SOURCE": "0",
        "REQUEST_DATE": "2000-01-01",
        "BALLOT_MAIL_DATE": "2000-01-01",
        "RETURN_CODE": "0",
    }, {
        "IDNUMBER": "654321",
        "COUNTY": "CLARK_COUNTY",
        "VOTE_TYPE": "Early",
        "ELECTION_CODE": "0000",
        "ACTIVITY_DATE": "2000-01-01",
        "NAME": "No One",
        "PRECINCT": "0",
        "PARTY": "0",
        "PARTY_NAME": "Null Party",
        "CONGRESS": "0",
        "ASSEMBLY": "0",
        "SENATE": "0",
        "COMMISSION": "0",
        "EDUCATION": "0",
        "REGENT": "0",
        "SCHOOL": "0",
        "CITY": "0",
        "WARD": "0",
        "TOWNSHIP": "0",
        "REG_STATUS": "A",
        "VOTE_SITE": "0",
        "BALLOT_PARTY": "NP",
        "REQUEST_SOURCE": "0",
        "REQUEST_DATE": "2000-01-01",
        "BALLOT_MAIL_DATE": "2000-01-01",
        "RETURN_CODE": "0",
    }]

    # Set raw_votes to fake values
    fake_scraper.raw_votes = fake_votes

    # Call process votes
    fake_scraper.process_votes()

    # Assert clean votes contains corret data
    assert len(fake_scraper.clean_votes) == 2
    assert fake_scraper.clean_votes[0].get_all() == fake_votes[0]
    assert fake_scraper.clean_votes[1].get_all() == fake_votes[1]


# Test process_votes fail
def test_process_votes_fail():
    # Fake variables
    fake_client = create_client_mock()
    fake_scraper = ClarkNVVoteScraper(fake_client)
    fake_votes = [{"Bad": "Value"}]

    # Set raw_votes to fake values
    fake_scraper.raw_votes = fake_votes

    # Assert exception is raised
    with pytest.raises(CCNVScraperError, match=r"Error processing votes"):
        fake_scraper.process_votes()
