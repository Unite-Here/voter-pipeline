import csv
import tempfile

import civis
from uhlibs.civis.api import query_civis

from lib.scraper.queries import UPSERT_VOTERS_QUERY
from lib.voter.voter import Voter

HEADER_LIST = [
    "IDNUMBER", "COUNTY", "VOTE_TYPE", "ELECTION_CODE", "ACTIVITY_DATE", "NAME", "PRECINCT", "PARTY", "PARTY_NAME",
    "CONGRESS", "ASSEMBLY", "SENATE", "COMMISSION", "EDUCATION", "REGENT", "SCHOOL", "CITY", "WARD", "TOWNSHIP",
    "REG_STATUS", "VOTE_SITE"
]
DATABASE = ""
TABLE = ""


class BaseScraperError(RuntimeError):
    pass


class BaseVoterScraper():

    def __init__(self) -> None:
        self.clean_votes: list[Voter] = []
        pass

    def db_upsert(self):
        """
        Add data to civis database from csv file
        """

        # Temporary directory for csv file
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Create csv file and write clean_votes data into file
                with open(f"{tmpdir}/voters_data.csv", "w", newline="") as v_data_file:
                    writer = csv.DictWriter(v_data_file, fieldnames=HEADER_LIST)
                    writer.writeheader()

                    # Loop through all Voter objects in list and add data as csv row
                    for voter in self.clean_votes:
                        data = voter.get_all()
                        writer.writerow(data)

                    # Send populated csv to database
                    fut = civis.io.csv_to_civis(v_data_file,
                                                database=DATABASE,
                                                table=TABLE,
                                                primary_keys=["IDNUMBER", "COUNTY"],
                                                last_modified_keys=["IDNUMBER", "COUNTY"],
                                                existing_table_rows="upsert")
                    fut.result()
            except Exception as err:
                raise BaseScraperError(f"Error upserting data to civis: {err}")

    def get_all_votes(self):
        raise NotImplementedError()
