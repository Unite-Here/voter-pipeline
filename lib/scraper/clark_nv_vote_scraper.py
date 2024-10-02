import os
import tempfile

from lib.scraper.base_vote_scraper import BaseVoterScrapper
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
        pass

    def get_all_votes(self):
        self.get_vbm_votes()
        self.get_ev_votes()
        self.process_votes()
        return self.clean_votes
        # Add all votes to a list of Voters

    def get_vbm_votes(self):
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

            # TODO: append Mail vote type to csv

            # Add file contents to the raw_votes list
            file_data = csv_to_list(f"{tmpdir}/{VBM_CSV_NAME}")
            self.raw_votes.extend(file_data)

    def get_ev_votes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Download file to tmpdir
            download_file(EV_URL, f"{tmpdir}/{EV_ZIP_NAME}")

            # Extract single file from downloaded zip
            unzip_file(f"{tmpdir}/{EV_ZIP_NAME}", EV_FILE_NAME, tmpdir)

            # Rename file from txt to csv
            os.rename(f"{tmpdir}/{EV_FILE_NAME}", f"{tmpdir}/{EV_CSV_NAME}")

            # TODO: append Mail vote type to csv
            
            # Add file contents to the raw_votes list
            file_data = csv_to_list(f"{tmpdir}/{EV_CSV_NAME}")
            self.raw_votes.extend(file_data)

    def process_votes(self):
        for item in self.raw_votes:
            
        #take raw_votes list, clean and create a list of voter objects
        pass

