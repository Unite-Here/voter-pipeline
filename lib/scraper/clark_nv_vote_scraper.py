import os
import tempfile

from lib.scraper.base_vote_scraper import BaseVoterScraper
from lib.utils.data import format_date_mdy_to_ymd
from lib.utils.files import csv_to_dict_list, download_file, unzip_file
from lib.voter.voter import Voter

EV_URL = "https://elections.clarkcountynv.gov/VoterRequestsTV/EVMB/ev_24G.zip"
EV_ZIP_NAME = "ev_24G.zip"
EV_CSV_NAME = "ev_votes.csv"
VBM_URL = "https://elections.clarkcountynv.gov/VoterRequestsTV/EVMB/mbreq24G.zip"
VBM_ZIP_NAME = "mbreq24G.zip"
VBM_CSV_NAME = "vbm_votes.csv"
RAW_EV_HEADERS = [
    "IDNUMBER", "NAME", "PRECINCT", "PARTY", "PARTY_NAME", "CONGRESS", "ASSEMBLY", "SENATE", "COMMISSION", "EDUCATION",
    "REGENT", "SCHOOL", "CITY", "WARD", "TOWNSHIP", "REG_STATUS", "VOTE_SITE", "ELECTION_CODE", "ACTIVITY_DATE"
]
RAW_VBM_HEADERS = [
    "IDNUMBER", "NAME", "STREET_NUMBER", "STREET_PREDIRECTION", "STREET_NAME", "STREET_TYPE", "UNIT", "CITY", "STATE",
    "ZIP", "PRECINCT", "VOTER_REG_PARTY", "BALLOT_PARTY", "ELECTION_CODE", "REQUEST_SOURCE", "REQUEST_DATE",
    "BALLOT_MAIL_DATE", "ACTIVITY_DATE", "RETURN_CODE"
]
COUNTY_NAME = "CLARK_COUNTY"
FILE_ENCODING = "cp1252"


class CCNVScraperError(RuntimeError):
    pass


class ClarkNVVoteScraper(BaseVoterScraper):

    def __init__(self, cli) -> None:
        super().__init__(cli)
        self.raw_votes = []

    def get_all_votes(self):
        """
        Get all votes

        Returns
        -------
        list
            clean_votes list of voter objects
        """
        try:
            self.get_vbm_votes()
            self.get_ev_votes()
            self.process_votes()
            return self.clean_votes
        except Exception as err:
            raise CCNVScraperError(f"Error getting all votes: {err}")

    def get_vbm_votes(self) -> None:
        """
        Get vote by mail
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Download file to tmpdir
                download_file(VBM_URL, f"{tmpdir}/{VBM_ZIP_NAME}")

                # Extract single file from downloaded zip
                file_name = unzip_file(f"{tmpdir}/{VBM_ZIP_NAME}", tmpdir)

                # Rename file from txt to csv
                os.rename(f"{tmpdir}/{file_name}", f"{tmpdir}/{VBM_CSV_NAME}")

                # Convert csv to list of dictionaries and add vote type
                file_data = csv_to_dict_list(f"{tmpdir}/{VBM_CSV_NAME}", True, RAW_VBM_HEADERS, FILE_ENCODING)
                
                # Remove items that do not have a value for voter_id or date_returned
                file_data = [val for val in file_data if val["IDNUMBER"]]
                
                for dictionary in file_data:
                    dictionary["VOTE_TYPE"] = "Mail"

                # Add file contents to the raw_votes list
                self.raw_votes.extend(file_data)
            except Exception as err:
                raise CCNVScraperError(f"Error getting votes by mail: {err}")

    def get_ev_votes(self) -> None:
        """
        Get early votes
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Download file to tmpdir
                download_file(EV_URL, f"{tmpdir}/{EV_ZIP_NAME}")

                # Extract single file from downloaded zip
                file_name = unzip_file(f"{tmpdir}/{EV_ZIP_NAME}", tmpdir)

                # Turn txt file into csv
                os.rename(f"{tmpdir}/{file_name}", f"{tmpdir}/{EV_CSV_NAME}")

                # Convert csv to list of dictionaries and add vote type
                file_data = csv_to_dict_list(f"{tmpdir}/{EV_CSV_NAME}", False, RAW_EV_HEADERS, FILE_ENCODING)
                for dictionary in file_data:
                    dictionary["VOTE_TYPE"] = "Early"

                # Add file contents to the raw_votes list
                self.raw_votes.extend(file_data)
            except Exception as err:
                raise CCNVScraperError(f"Error getting early votes: {err}")

    def process_votes(self) -> None:
        """
        Process raw data into voter objects
        """
        try:
            for raw_data in self.raw_votes:
                # Create voter object with required parameters
                voter = Voter(raw_data["IDNUMBER"], COUNTY_NAME, raw_data["VOTE_TYPE"], raw_data["ELECTION_CODE"],
                              raw_data["ACTIVITY_DATE"])

                # Set optional parameter values
                voter.set_optional(raw_data)

                # Format dates to yyyy-mm-dd
                activity_date = voter.get_activity_date()
                formatted_activity_date = format_date_mdy_to_ymd(activity_date)
                voter.set_activity_date(formatted_activity_date)
                
                if voter.get_request_date() is not None:
                    request_date = voter.get_request_date()
                    formatted_request_date = format_date_mdy_to_ymd(str(request_date))
                    voter.set_request_date(formatted_request_date)
                
                if voter.get_ballot_mail_date() is not None:
                    ballot_mail_date = voter.get_ballot_mail_date()
                    formatted_ballot_mail_date = format_date_mdy_to_ymd(str(ballot_mail_date))
                    voter.set_ballot_mail_date(formatted_ballot_mail_date)

                # Append voter to list
                self.clean_votes.append(voter)
        except Exception as err:
            raise CCNVScraperError(f"Error processing votes: {err}")
