from dataclasses import dataclass

from utils.data import validate_input


class VoterClassError(RuntimeError):
    pass


VOTE_TYPE_OPTIONS = ["Mail", "Early", "E-day"]


@dataclass
class Voter:
    """
    Voter object class

    Attributes
    ----------
    IDNUMBER : str
        Voter record unique identifier
    COUNTY : str
        Voting district
    VOTE_TYPE : str
        Vote type - Mail, Early, E-day
    ELECTION_CODE : str
        Election voter voted in
    ACTIVITY_DATE : str
        Date and time voter voted
    NAME : str | None
        Voter name
    PRECINCT : str | None
        Voter precinct
    PARTY : str | None
        Ballot party code
    PARTY_NAME : str | None
        Abbreviation for party
    CONGRESS : str | None
        Voting district
    ASSEMBLY : str | None
        Voting district
    SENATE : str | None
        Voting district
    COMMISSION : str | None
        Voting district
    EDUCATION : str | None
        Voting district
    REGENT : str | None
        Voting district
    SCHOOL : str | None
        Voting district
    CITY : str | None
        Voting district
    WARD : str | None
        Voting district
    TOWNSHIP : str | None
        Voting district
    REG_STATUS : str | None
        Voter registration status
    VOTE_SITE : str | None
        Site voter voted at

    Methods
    -------
    Getters and setters for all attributes
    """

    IDNUMBER: str
    COUNTY: str
    VOTE_TYPE: str
    ELECTION_CODE: str
    ACTIVITY_DATE: str
    NAME: str | None = None
    PRECINCT: str | None = None
    PARTY: str | None = None
    PARTY_NAME: str | None = None
    CONGRESS: str | None = None
    ASSEMBLY: str | None = None
    SENATE: str | None = None
    COMMISSION: str | None = None
    EDUCATION: str | None = None
    REGENT: str | None = None
    SCHOOL: str | None = None
    CITY: str | None = None
    WARD: str | None = None
    TOWNSHIP: str | None = None
    REG_STATUS: str | None = None
    VOTE_SITE: str | None = None

    def set_all(self, voter_data: list):
        """
        Set multiple values at once

        Parameters
        ----------
        voter_data : list
            List must contain the following values in this order:
                - IDNUMBER
                - COUNTY
                - VOTE_TYPE
                - ELECTION_CODE
                - ACTIVITY_DATE
            
            Additional optional values in order are:
                - NAME
                - PRECINCT
                - PARTY
                - PARTY_NAME
                - CONGRESS
                - ASSEMBLY
                - SENATE
                - COMMISSION
                - EDUCATION
                - REGENT
                - SCHOOL
                - CITY
                - WARD
                - TOWNSHIP
                - REG_STATUS
                - VOTE_SITE
        """

        if len(voter_data) < 5:
            raise VoterClassError("Voter data list missing required values")
        else:
            self.set_idnumber(voter_data[0])
            self.set_county(voter_data[1])
            self.set_vote_type(voter_data[2])
            self.set_election_code(voter_data[3])
            self.set_activity_date(voter_data[4])

            try:
                self.set_name(voter_data[5])
            except:
                pass
            try:
                self.set_precinct(voter_data[6])
            except:
                pass
            try:
                self.set_party(voter_data[7])
            except:
                pass
            try:
                self.set_party_name(voter_data[8])
            except:
                pass
            try:
                self.set_congress(voter_data[9])
            except:
                pass
            try:
                self.set_assembly(voter_data[10])
            except:
                pass
            try:
                self.set_senate(voter_data[11])
            except:
                pass
            try:
                self.set_commission(voter_data[12])
            except:
                pass
            try:
                self.set_education(voter_data[13])
            except:
                pass
            try:
                self.set_regent(voter_data[14])
            except:
                pass
            try:
                self.set_school(voter_data[15])
            except:
                pass
            try:
                self.set_city(voter_data[16])
            except:
                pass
            try:
                self.set_ward(voter_data[17])
            except:
                pass
            try:
                self.set_township(voter_data[18])
            except:
                pass
            try:
                self.set_reg_status(voter_data[19])
            except:
                pass
            try:
                self.set_vote_site(voter_data[20])
            except:
                pass

    def get_idnumber(self) -> str:
        return self.IDNUMBER

    def set_idnumber(self, val: str):
        self.IDNUMBER = val

    def get_county(self) -> str:
        return self.COUNTY

    def set_county(self, val: str) -> None:
        self.COUNTY = val

    def get_vote_type(self) -> str:
        return self.VOTE_TYPE

    def set_vote_type(self, val: str) -> None:
        valid = validate_input(VOTE_TYPE_OPTIONS, val)
        if valid:
            self.VOTE_TYPE = val
        else:
            raise VoterClassError(f"Invalid input {val}, valid inputs are: Mail, Early, E-day")

    def get_election_code(self) -> str:
        return self.ELECTION_CODE

    def set_election_code(self, val: str) -> None:
        self.ELECTION_CODE = val

    def get_activity_date(self) -> str:
        return self.ACTIVITY_DATE

    def set_activity_date(self, val: str) -> None:
        self.ACTIVITY_DATE = val

    def get_name(self) -> str | None:
        return self.NAME

    def set_name(self, val: str) -> None:
        self.NAME = val

    def get_precinct(self) -> str | None:
        return self.PRECINCT

    def set_precinct(self, val: str) -> None:
        self.PRECINCT = val

    def get_party(self) -> str | None:
        return self.PARTY

    def set_party(self, val: str) -> None:
        self.PARTY = val

    def get_party_name(self) -> str | None:
        return self.PARTY_NAME

    def set_party_name(self, val: str) -> None:
        self.PARTY_NAME = val

    def get_congress(self) -> str | None:
        return self.CONGRESS

    def set_congress(self, val: str) -> None:
        self.CONGRESS = val

    def get_assembly(self) -> str | None:
        return self.ASSEMBLY

    def set_assembly(self, val: str) -> None:
        self.ASSEMBLY = val

    def get_senate(self) -> str | None:
        return self.SENATE

    def set_senate(self, val: str) -> None:
        self.SENATE = val

    def get_commission(self) -> str | None:
        return self.COMMISSION

    def set_commission(self, val: str) -> None:
        self.COMMISSION = val

    def get_education(self) -> str | None:
        return self.EDUCATION

    def set_education(self, val: str) -> None:
        self.EDUCATION = val

    def get_regent(self) -> str | None:
        return self.REGENT

    def set_regent(self, val: str) -> None:
        self.REGENT = val

    def get_school(self) -> str | None:
        return self.SCHOOL

    def set_school(self, val: str) -> None:
        self.SCHOOL = val

    def get_city(self) -> str | None:
        return self.CITY

    def set_city(self, val: str) -> None:
        self.CITY = val

    def get_ward(self) -> str | None:
        return self.WARD

    def set_ward(self, val: str) -> None:
        self.WARD = val

    def get_township(self) -> str | None:
        return self.TOWNSHIP

    def set_township(self, val: str) -> None:
        self.TOWNSHIP = val

    def get_reg_status(self) -> str | None:
        return self.REG_STATUS

    def set_reg_status(self, val: str) -> None:
        self.REG_STATUS = val

    def get_vote_site(self) -> str | None:
        return self.VOTE_SITE

    def set_vote_site(self, val: str) -> None:
        self.VOTE_SITE = val
