from dataclasses import dataclass


@dataclass
class Voter:
    """
    Voter object class

    Attributes
    ----------
    IDNUMBER : int
        Voter record unique identifier
    NAME : str
        Voter name
    PRECINCT : int
        Voter precinct
    PARTY : int
        Ballot party code
    PARTY_ABBR : str
        Abbreviation for party
    CONGRESS : int
        Voting district
    ASSEMBLY : int
        Voting district
    SENATE : int
        Voting district
    COMMISSION : str
        Voting district
    EDUCATION : int
        Voting district
    REGENT : int
        Voting district
    SCHOOL : str
        Voting district
    CITY : str
        Voting district
    WARD : str
        Voting district
    TOWNSHIP : str
        Voting district
    STATUS : int
        Voter registration status
    EV_SITE : str
        Early vote site voter voted at
    ELECTION_CODE : str
        Election voter voted in
    ACTIVITY_DATE : str
        Date and time voter voted

    Methods
    -------
    Getters and setters for all attributes
    """
    
    IDNUMBER: int
    NAME: str
    PRECINCT: int
    PARTY: int
    PARTY_ABBR: str
    CONGRESS: int
    ASSEMBLY: int
    SENATE: int
    COMMISSION: str
    EDUCATION: int
    REGENT: int
    SCHOOL: str
    CITY: str
    WARD: str
    TOWNSHIP: str
    STATUS: int
    EV_SITE: str
    ELECTION_CODE: str
    ACTIVITY_DATE: str

    def __init__(self, voter_data: list):
        self.IDNUMBER = voter_data[0]
        self.NAME = voter_data[0]
        self.PRECINCT = voter_data[0]
        self.PARTY = voter_data[0]
        self.PARTY_ABBR = voter_data[0]
        self.CONGRESS = voter_data[0]
        self.ASSEMBLY = voter_data[0]
        self.SENATE = voter_data[0]
        self.COMMISSION = voter_data[0]
        self.EDUCATION = voter_data[0]
        self.REGENT = voter_data[0]
        self.SCHOOL = voter_data[0]
        self.CITY = voter_data[0]
        self.WARD = voter_data[0]
        self.TOWNSHIP = voter_data[0]
        self.STATUS = voter_data[0]
        self.EV_SITE = voter_data[0]
        self.ELECTION_CODE = voter_data[0]
        self.ACTIVITY_DATE = voter_data[0]

    def get_idnumber(self):
        return self.IDNUMBER

    def set_idnumber(self, val):
        self.IDNUMBER = val

    def get_name(self):
        return self.NAME

    def set_name(self, val):
        self.NAME = val

    def get_precinct(self):
        return self.PRECINCT

    def set_precinct(self, val):
        self.PRECINCT = val

    def get_party(self):
        return self.PARTY

    def set_party(self, val):
        self.PARTY = val

    def get_party_abbr(self):
        return self.PARTY_ABBR

    def set_party_abbr(self, val):
        self.PARTY_ABBR = val

    def get_congress(self):
        return self.CONGRESS

    def set_congress(self, val):
        self.CONGRESS = val

    def get_assembly(self):
        return self.ASSEMBLY

    def set_assembly(self, val):
        self.ASSEMBLY = val

    def get_senate(self):
        return self.SENATE

    def set_senate(self, val):
        self.SENATE = val

    def get_commission(self):
        return self.COMMISSION

    def set_commission(self, val):
        self.COMMISSION = val

    def get_education(self):
        return self.EDUCATION

    def set_education(self, val):
        self.EDUCATION = val

    def get_regent(self):
        return self.REGENT

    def set_regent(self, val):
        self.REGENT = val

    def get_school(self):
        return self.SCHOOL

    def set_school(self, val):
        self.SCHOOL = val

    def get_city(self):
        return self.CITY

    def set_city(self, val):
        self.CITY = val

    def get_ward(self):
        return self.WARD

    def set_ward(self, val):
        self.WARD = val

    def get_township(self):
        return self.TOWNSHIP

    def set_township(self, val):
        self.TOWNSHIP = val

    def get_status(self):
        return self.STATUS

    def set_status(self, val):
        self.STATUS = val

    def get_ev_site(self):
        return self.EV_SITE

    def set_ev_site(self, val):
        self.EV_SITE = val

    def get_election_code(self):
        return self.ELECTION_CODE

    def set_election_code(self, val):
        self.ELECTION_CODE = val

    def get_activity_date(self):
        return self.ACTIVITY_DATE

    def set_activity_date(self, val):
        self.ACTIVITY_DATE = val
