import csv
import re
import tempfile

import requests
from bs4 import BeautifulSoup

from lib.scraper.base_vote_scraper import BaseVoterScraper
from lib.utils.data import format_date_mdy_to_ymd
from lib.utils.files import csv_to_dict_list, delete_csv_headers, download_file, xlsx_to_csv, delete_csv_headers
from lib.voter.voter import Voter

VOTE_URL = "https://www.washoecounty.gov/voters/2024-election/electionreports/ev_turnout.php"
BASE_URL = "https://www.washoecounty.gov/voters/2024-election"
XLSX_FILE_NAME = "PPP-EV.xlsx"
CSV_FILE_NAME = "PPP-EV.csv"
RAW_VOTE_HEADERS = [
    "voter_id", "affidavit", "name_prefix", "name_last", "name_first", "name_middle", "name_suffix", "house_number",
    "house_fraction", "pre_direction", "street", "street_type", "post_direction", "building_number", "apartment_number",
    "city", "zip", "precinct", "portion", "party", "reg_date", "image_id", "phone_1", "phone_2", "military", "gender",
    "perm_av", "birth_place", "birth_date", "mailing_address", "mail_street", "mail_city", "mail_state", "mail_zip",
    "mail_country", "language", "drivers_license", "consolidation", "ballot_type", "av_election_id", "category",
    "source", "date_entered", "date_returned", "cassette", "frame", "sequence", "election_id", "label", "ballot_status",
    "original_party", "id_required", "citizen", "underage", "challenged", "batch", "leg_dist", "consolidation_name",
    "precinct_name", "house_district", "school_district", "verified", "consolidation_serial_number"
]
COUNTY_NAME = "WASHOE_COUNTY"
ELECTION_CODE = "24PP"
FILE_ENCODING = "utf-8"


class WCNVScraperError(RuntimeError):
    pass


class WashoeNVVoteScraper(BaseVoterScraper):

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
            self.get_raw_votes_from_link()
            self.process_votes()
            return self.clean_votes
        except Exception as err:
            raise WCNVScraperError(f"Error getting all votes: {err}")

    def get_raw_votes_from_link(self) -> None:
        """
        Get votes from latest link
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            file_url = self.get_latest_link()
            try:
                # Download file to tmpdir
                download_file(file_url, f"{tmpdir}/{XLSX_FILE_NAME}")

                # Transform file to csv
                xlsx_to_csv(f"{tmpdir}/{XLSX_FILE_NAME}", f"{tmpdir}/{CSV_FILE_NAME}", FILE_ENCODING)

                # Delete headers from csv file
                delete_csv_headers(f"{tmpdir}/{CSV_FILE_NAME}", tmpdir, FILE_ENCODING)

                # Convert csv to list of dicts
                file_data = csv_to_dict_list(f"{tmpdir}/{CSV_FILE_NAME}", False, RAW_VOTE_HEADERS, FILE_ENCODING)

                # Remove items that do not have a value for voter_id or date_returned
                file_data = [val for val in file_data if val["voter_id"] and val["date_returned"]]
                
                # Add file contents to the raw_votes list
                self.raw_votes.extend(file_data)
            except Exception as err:
                raise WCNVScraperError(f"Error getting votes from link: {err}")

    def get_latest_link(self) -> str:
        """
        Get most recent file link for election
        """
        try:
            # Get html
            result = requests.get(VOTE_URL)
            soup = BeautifulSoup(result.content, "html5lib")
            html_list = soup.findAll("a", {"href": re.compile(r"2024-election-files\/PPP-EV-.*\.xlsx")})

            # Extract links from html_list
            links = []
            for link in html_list:
                links.append(link.get("href"))
            
            # Sort links from newest to oldest
            links.sort(reverse=True)
            
            # Format link
            newest = links[0]
            formatted = BASE_URL + newest[2:]

            return formatted
        except Exception as err:
            raise WCNVScraperError(f"Error getting latest link: {err}")

    def process_votes(self) -> None:
        """
        Process raw data into voter objects
        """
        try:
            for raw_data in self.raw_votes:
                # Translate vote type from raw
                v_type = self.translate_vote_type(raw_data["category"])
                
                # Create voter object with required parameters
                voter = Voter(raw_data["voter_id"], COUNTY_NAME, v_type, ELECTION_CODE,
                              raw_data["date_returned"])

                # Set optional values
                voter.set_party_name(raw_data["party"])
                voter.set_precinct(raw_data["precinct"])
                voter.set_city(raw_data["city"])
                
                # Format dates to yyyy-mm-dd
                activity_date = voter.get_activity_date()
                formatted_activity_date = format_date_mdy_to_ymd(activity_date)
                voter.set_activity_date(formatted_activity_date)
                
                # Append voter to list
                self.clean_votes.append(voter)
        except Exception as err:
            raise WCNVScraperError(f"Error processing votes: {err}")

    def translate_vote_type(self, vote: str) -> str:
        if vote == "EV":
            return "Early"
        else:
            return "Mail"
