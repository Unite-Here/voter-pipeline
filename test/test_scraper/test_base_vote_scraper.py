from unittest.mock import Mock

import pytest
from civis.futures import CivisFuture
from civis.response import Response
from civis.tests import create_client_mock

from lib.scraper.base_vote_scraper import BaseScraperError, BaseVoterScraper
from lib.voter.voter import Voter


def create_mock_future(client, response):
    mock_poller = client.queries.get_runs
    mock_poller.return_value = response
    mock_poller_args = None, None
    return CivisFuture(mock_poller, mock_poller_args, None)


# Test db_upsert success
def test_db_upsert_success(mocker):
    # Fake variables
    fake_client = create_client_mock()
    fake_table = "fake.table"
    fake_scraper = BaseVoterScraper(fake_client, fake_table)
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

    fake_voters = [
        Voter(fake_votes[0]["IDNUMBER"], fake_votes[0]["COUNTY"], fake_votes[0]["VOTE_TYPE"],
              fake_votes[0]["ELECTION_CODE"], fake_votes[0]["ACTIVITY_DATE"], fake_votes[0]["NAME"],
              fake_votes[0]["PRECINCT"], fake_votes[0]["PARTY"], fake_votes[0]["PARTY_NAME"], fake_votes[0]["CONGRESS"],
              fake_votes[0]["ASSEMBLY"], fake_votes[0]["SENATE"], fake_votes[0]["COMMISSION"],
              fake_votes[0]["EDUCATION"], fake_votes[0]["REGENT"], fake_votes[0]["SCHOOL"], fake_votes[0]["CITY"],
              fake_votes[0]["WARD"], fake_votes[0]["TOWNSHIP"], fake_votes[0]["REG_STATUS"], fake_votes[0]["VOTE_SITE"],
              fake_votes[0]["BALLOT_PARTY"], fake_votes[0]["REQUEST_SOURCE"], fake_votes[0]["REQUEST_DATE"],
              fake_votes[0]["BALLOT_MAIL_DATE"], fake_votes[0]["RETURN_CODE"]),
        Voter(fake_votes[1]["IDNUMBER"], fake_votes[1]["COUNTY"], fake_votes[1]["VOTE_TYPE"],
              fake_votes[1]["ELECTION_CODE"], fake_votes[1]["ACTIVITY_DATE"], fake_votes[1]["NAME"],
              fake_votes[1]["PRECINCT"], fake_votes[1]["PARTY"], fake_votes[1]["PARTY_NAME"], fake_votes[1]["CONGRESS"],
              fake_votes[1]["ASSEMBLY"], fake_votes[1]["SENATE"], fake_votes[1]["COMMISSION"],
              fake_votes[1]["EDUCATION"], fake_votes[1]["REGENT"], fake_votes[1]["SCHOOL"], fake_votes[1]["CITY"],
              fake_votes[1]["WARD"], fake_votes[1]["TOWNSHIP"], fake_votes[1]["REG_STATUS"], fake_votes[1]["VOTE_SITE"],
              fake_votes[1]["BALLOT_PARTY"], fake_votes[1]["REQUEST_SOURCE"], fake_votes[1]["REQUEST_DATE"],
              fake_votes[1]["BALLOT_MAIL_DATE"], fake_votes[1]["RETURN_CODE"])
    ]

    # Mock function call
    mock_csv_to_civis = mocker.patch("lib.scraper.base_vote_scraper.civis.io.csv_to_civis")

    # Set fake_scraper clean_votes list using fake_voters
    fake_scraper.clean_votes = fake_voters

    # Call db_upsert function
    fake_scraper.db_upsert()

    # Assert csv_to_civis function called successfully
    mock_csv_to_civis.assert_called()


# Test db_upsert fail
def test_db_upsert_fail(mocker):
    fake_client = create_client_mock()
    fake_table = "fake.table"
    fake_scraper = BaseVoterScraper(fake_client, fake_table)
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

    fake_voters = [
        Voter(fake_votes[0]["IDNUMBER"], fake_votes[0]["COUNTY"], fake_votes[0]["VOTE_TYPE"],
              fake_votes[0]["ELECTION_CODE"], fake_votes[0]["ACTIVITY_DATE"], fake_votes[0]["NAME"],
              fake_votes[0]["PRECINCT"], fake_votes[0]["PARTY"], fake_votes[0]["PARTY_NAME"], fake_votes[0]["CONGRESS"],
              fake_votes[0]["ASSEMBLY"], fake_votes[0]["SENATE"], fake_votes[0]["COMMISSION"],
              fake_votes[0]["EDUCATION"], fake_votes[0]["REGENT"], fake_votes[0]["SCHOOL"], fake_votes[0]["CITY"],
              fake_votes[0]["WARD"], fake_votes[0]["TOWNSHIP"], fake_votes[0]["REG_STATUS"], fake_votes[0]["VOTE_SITE"],
              fake_votes[0]["BALLOT_PARTY"], fake_votes[0]["REQUEST_SOURCE"], fake_votes[0]["REQUEST_DATE"],
              fake_votes[0]["BALLOT_MAIL_DATE"], fake_votes[0]["RETURN_CODE"]),
        Voter(fake_votes[1]["IDNUMBER"], fake_votes[1]["COUNTY"], fake_votes[1]["VOTE_TYPE"],
              fake_votes[1]["ELECTION_CODE"], fake_votes[1]["ACTIVITY_DATE"], fake_votes[1]["NAME"],
              fake_votes[1]["PRECINCT"], fake_votes[1]["PARTY"], fake_votes[1]["PARTY_NAME"], fake_votes[1]["CONGRESS"],
              fake_votes[1]["ASSEMBLY"], fake_votes[1]["SENATE"], fake_votes[1]["COMMISSION"],
              fake_votes[1]["EDUCATION"], fake_votes[1]["REGENT"], fake_votes[1]["SCHOOL"], fake_votes[1]["CITY"],
              fake_votes[1]["WARD"], fake_votes[1]["TOWNSHIP"], fake_votes[1]["REG_STATUS"], fake_votes[1]["VOTE_SITE"],
              fake_votes[1]["BALLOT_PARTY"], fake_votes[1]["REQUEST_SOURCE"], fake_votes[1]["REQUEST_DATE"],
              fake_votes[1]["BALLOT_MAIL_DATE"], fake_votes[1]["RETURN_CODE"])
    ]

    # Mock function call
    mock_csv_to_civis = mocker.patch("lib.scraper.base_vote_scraper.civis.io.csv_to_civis", side_effect=Exception)

    # Set fake_scraper clean_votes list using fake_voters
    fake_scraper.clean_votes = fake_voters

    # Assert exception raised
    with pytest.raises(BaseScraperError, match=r"Error upserting data to civis"):
        fake_scraper.db_upsert()
