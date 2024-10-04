import os
import tempfile

from lib.scraper.base_vote_scraper import BaseVoterScrapper
from lib.voter.voter import Voter
from utils.files import csv_to_dict_list, download_file, unzip_file

EV_URL = "https://elections.clarkcountynv.gov/VoterRequestsTV/EVMB/ev_24P.zip"
EV_ZIP_NAME = "ev_24P.zip"
EV_FILE_NAME = "EV_24P.txt"
EV_CSV_NAME = "ev_votes.csv"
VBM_URL = "https://elections.clarkcountynv.gov/VoterRequestsTV/EVMB/mbreq24P.zip"
VBM_ZIP_NAME = "mbreq24P.zip"
VBM_FILE_NAME = "mbreq24P_20240620_23300223.txt"
VBM_CSV_NAME = "vbm_votes.csv"
RAW_HEADER_LIST = [
    "IDNUMBER", "NAME", "PRECINCT", "PARTY", "PARTY_NAME", "CONGRESS", "ASSEMBLY", "SENATE", "COMMISSION", "EDUCATION",
    "REGENT", "SCHOOL", "CITY", "WARD", "TOWNSHIP", "REG_STATUS", "VOTE_SITE", "ELECTION_CODE", "ACTIVITY_DATE"
]
CLEAN_HEADER_LIST = [
    "IDNUMBER", "COUNTY", "VOTE_TYPE", "ELECTION_CODE", "ACTIVITY_DATE", "NAME", "PRECINCT", "PARTY", "PARTY_NAME",
    "CONGRESS", "ASSEMBLY", "SENATE", "COMMISSION", "EDUCATION", "REGENT", "SCHOOL", "CITY", "WARD", "TOWNSHIP",
    "REG_STATUS", "VOTE_SITE"
]


class CCNVScraperError(RuntimeError):
    pass


class ClarkNVVoteScraper(BaseVoterScrapper):

    def __init__(self) -> None:
        super().__init__()
        self.raw_votes = []
        self.clean_votes = []

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
                unzip_file(f"{tmpdir}/{VBM_ZIP_NAME}", VBM_FILE_NAME, tmpdir)

                # Rename file from txt to csv
                os.rename(f"{tmpdir}/{VBM_FILE_NAME}", f"{tmpdir}/{VBM_CSV_NAME}")

                # Convert csv to list of dictionaries and add vote type
                file_data = csv_to_dict_list(f"{tmpdir}/{VBM_CSV_NAME}", RAW_HEADER_LIST)
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
                unzip_file(f"{tmpdir}/{EV_ZIP_NAME}", EV_FILE_NAME, tmpdir)

                # Turn txt file into csv
                os.rename(f"{tmpdir}/{EV_FILE_NAME}", f"{tmpdir}/{EV_CSV_NAME}")

                # Convert csv to list of dictionaries and add vote type
                file_data = csv_to_dict_list(f"{tmpdir}/{EV_CSV_NAME}", RAW_HEADER_LIST)
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
                # Set voter data
                voter = Voter(raw_data["IDNUMBER"], "CLARK_COUNTY", raw_data["VOTE_TYPE"], raw_data["ELECTION_CODE"],
                              raw_data["ACTIVITY_DATE"], raw_data["NAME"], raw_data["PRECINCT"], raw_data["PARTY"],
                              raw_data["PARTY_NAME"], raw_data["CONGRESS"], raw_data["ASSEMBLY"], raw_data["SENATE"],
                              raw_data["COMMISSION"], raw_data["EDUCATION"], raw_data["REGENT"], raw_data["SCHOOL"],
                              raw_data["CITY"], raw_data["WARD"], raw_data["TOWNSHIP"], raw_data["REG_STATUS"],
                              raw_data["VOTE_SITE"])

                # Append voter to list
                self.clean_votes.append(voter)
        except Exception as err:
            raise CCNVScraperError(f"Error processing votes: {err}")
