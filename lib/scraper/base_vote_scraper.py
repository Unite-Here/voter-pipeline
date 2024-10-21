import csv
import tempfile

import civis

from lib.voter.voter import Voter

HEADER_LIST = [
    "IDNUMBER", "COUNTY", "VOTE_TYPE", "ELECTION_CODE", "ACTIVITY_DATE", "NAME", "PRECINCT", "PARTY", "PARTY_NAME",
    "CONGRESS", "ASSEMBLY", "SENATE", "COMMISSION", "EDUCATION", "REGENT", "SCHOOL", "CITY", "WARD", "TOWNSHIP",
    "REG_STATUS", "VOTE_SITE", "BALLOT_PARTY", "REQUEST_SOURCE", "REQUEST_DATE", "BALLOT_MAIL_DATE", "RETURN_CODE"
]
SQL_HEADERS = [{
    "name": "IDNUMBER",
    # "sql_type": "VARCHAR"
}, {
    "name": "COUNTY",
    # "sql_type": "VARCHAR"
}, {
    "name": "VOTE_TYPE",
    # "sql_type": "VARCHAR"
}, {
    "name": "ELECTION_CODE",
    # "sql_type": "VARCHAR"
}, {
    "name": "ACTIVITY_DATE",
    # "sql_type": "DATE"
}, {
    "name": "NAME",
    # "sql_type": "VARCHAR"
}, {
    "name": "PRECINCT",
    # "sql_type": "VARCHAR"
}, {
    "name": "PARTY",
    # "sql_type": "VARCHAR"
}, {
    "name": "PARTY_NAME",
    # "sql_type": "VARCHAR"
}, {
    "name": "CONGRESS",
    # "sql_type": "VARCHAR"
}, {
    "name": "ASSEMBLY",
    # "sql_type": "VARCHAR"
}, {
    "name": "SENATE",
    # "sql_type": "VARCHAR"
}, {
    "name": "COMMISSION",
    # "sql_type": "VARCHAR"
}, {
    "name": "EDUCATION",
    # "sql_type": "VARCHAR"
}, {
    "name": "REGENT",
    # "sql_type": "VARCHAR"
}, {
    "name": "SCHOOL",
    # "sql_type": "VARCHAR"
}, {
    "name": "CITY",
    # "sql_type": "VARCHAR"
}, {
    "name": "WARD",
    # "sql_type": "VARCHAR"
}, {
    "name": "TOWNSHIP",
    # "sql_type": "VARCHAR"
}, {
    "name": "REG_STATUS",
    # "sql_type": "VARCHAR"
}, {
    "name": "VOTE_SITE",
    # "sql_type": "VARCHAR"
}, {
    "name": "BALLOT_PARTY",
    # "sql_type": "VARCHAR"
}, {
    "name": "REQUEST_SOURCE",
    # "sql_type": "VARCHAR"
}, {
    "name": "REQUEST_DATE",
    # "sql_type": "DATE"
}, {
    "name": "BALLOT_MAIL_DATE",
    # "sql_type": "DATE"
}, {
    "name": "RETURN_CODE",
    # "sql_type": "VARCHAR"
}]
DATABASE = "Unite Here"
TABLE = "political_dev.voter_pipeline"


class BaseScraperError(RuntimeError):
    pass


class BaseVoterScraper():

    def __init__(self, cli) -> None:
        self.client = cli
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
                fut = civis.io.csv_to_civis(f"{tmpdir}/voters_data.csv",
                                            client=self.client,
                                            database=DATABASE,
                                            table=TABLE,
                                            headers=True,
                                            table_columns=SQL_HEADERS,
                                            primary_keys=["idnumber", "county"],
                                            last_modified_keys=["idnumber", "county"],
                                            existing_table_rows="upsert")
                fut.result()
            except Exception as err:
                raise BaseScraperError(f"Error upserting data to civis: {err}")

    def get_all_votes(self):
        raise NotImplementedError()
