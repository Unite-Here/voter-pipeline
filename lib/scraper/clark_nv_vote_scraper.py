import csv
import os
import tempfile

from lib.scraper.base_vote_scraper import BaseVoterScrapper
from lib.voter.voter import Voter
from utils.files import csv_to_list, download_file, unzip_file

EV_URL = "https://elections.clarkcountynv.gov/VoterRequestsTV/EVMB/ev_24P.zip"
EV_ZIP_NAME = "ev_24P.zip"
EV_FILE_NAME = "EV_24P.txt"
EV_CSV_NAME = "ev_votes.csv"
VBM_URL = ""
VBM_ZIP_NAME = ""
VBM_CSV_NAME = ""
VBM_FILE_NAME = ""


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
        self.get_vbm_votes()
        self.get_ev_votes()
        self.process_votes()
        return self.clean_votes

    def get_vbm_votes(self) -> None:
        """
        Get vote by mail
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Download file to tmpdir
            download_file(VBM_URL, f"{tmpdir}/{VBM_ZIP_NAME}")

            # Extract single file from downloaded zip
            unzip_file(f"{tmpdir}/{VBM_ZIP_NAME}", VBM_FILE_NAME, tmpdir)

            # Rename file from txt to csv
            os.rename(f"{tmpdir}/{VBM_FILE_NAME}", f"{tmpdir}/{VBM_CSV_NAME}")

            # Add file contents to the raw_votes list
            file_data = csv_to_list(f"{tmpdir}/{VBM_CSV_NAME}")
            self.raw_votes.extend(file_data)

            # Add vote type to lists
            for row in file_data:
                row.extend("Mail")

    def get_ev_votes(self) -> None:
        """
        Get early votes
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Download file to tmpdir
            download_file(EV_URL, f"{tmpdir}/{EV_ZIP_NAME}")

            # Extract single file from downloaded zip
            unzip_file(f"{tmpdir}/{EV_ZIP_NAME}", EV_FILE_NAME, tmpdir)

            # Rename file from txt to csv
            os.rename(f"{tmpdir}/{EV_FILE_NAME}", f"{tmpdir}/{EV_CSV_NAME}")

            # Add file contents to the raw_votes list
            file_data = csv_to_list(f"{tmpdir}/{EV_CSV_NAME}")
            self.raw_votes.extend(file_data)

            # Add vote type to lists
            for row in file_data:
                row.extend("Early")

    def process_votes(self) -> None:
        """
        Process raw data into voter objects
        """
        for raw_data in self.raw_votes:
            # Empty voter object
            voter = Voter("", "", "", "", "")

            # Set data to be used for voter
            clean_data = [
                raw_data[0],        # idnumber
                "CLARK_COUNTY",     # county
                raw_data[19],       # vote_type
                raw_data[17],       # election_code
                raw_data[18],       # activity_date
                raw_data[1],        # name
                raw_data[2],        # precinct
                raw_data[3],        # party
                raw_data[4],        # party_name
                raw_data[5],        # congress
                raw_data[6],        # assembly
                raw_data[7],        # senate
                raw_data[8],        # commission
                raw_data[9],        # education
                raw_data[10],       # regent
                raw_data[11],       # school
                raw_data[12],       # city
                raw_data[13],       # ward
                raw_data[14],       # township
                raw_data[15],       # reg_status
                raw_data[16]        # vote_site
            ]

            # Set voter data
            voter.set_all(clean_data) 

            # Append voter to list
            self.clean_votes.append(voter)
