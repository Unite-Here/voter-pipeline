import pytest

from lib.voter.voter import Voter, VoterClassError


# Test making instance of Voter
def test_make_voter():
    # Fake variables
    fake_data = {
        "IDNUMBER": "123456",
        "COUNTY": "UNKNOWN_COUNTY",
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
        "VOTE_SITE": "0"
    }

    fake_voter = Voter(fake_data["IDNUMBER"], fake_data["COUNTY"], fake_data["VOTE_TYPE"], fake_data["ELECTION_CODE"],
                       fake_data["ACTIVITY_DATE"], fake_data["NAME"], fake_data["PRECINCT"], fake_data["PARTY"],
                       fake_data["PARTY_NAME"], fake_data["CONGRESS"], fake_data["ASSEMBLY"], fake_data["SENATE"],
                       fake_data["COMMISSION"], fake_data["EDUCATION"], fake_data["REGENT"], fake_data["SCHOOL"],
                       fake_data["CITY"], fake_data["WARD"], fake_data["TOWNSHIP"], fake_data["REG_STATUS"],
                       fake_data["VOTE_SITE"])

    # Assert that Voter data matches input
    assert fake_voter.get_all() == fake_data


def test_make_voter_invalid_vote_type():
    # Fake variables
    fake_data = {
        "IDNUMBER": "123456",
        "COUNTY": "UNKNOWN_COUNTY",
        "VOTE_TYPE": "NOT A VOTE OPTION",
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
        "VOTE_SITE": "0"
    }

    # Assert exception raised
    with pytest.raises(VoterClassError):
        fake_voter = Voter(fake_data["IDNUMBER"], fake_data["COUNTY"], fake_data["VOTE_TYPE"],
                           fake_data["ELECTION_CODE"], fake_data["ACTIVITY_DATE"], fake_data["NAME"],
                           fake_data["PRECINCT"], fake_data["PARTY"], fake_data["PARTY_NAME"], fake_data["CONGRESS"],
                           fake_data["ASSEMBLY"], fake_data["SENATE"], fake_data["COMMISSION"], fake_data["EDUCATION"],
                           fake_data["REGENT"], fake_data["SCHOOL"], fake_data["CITY"], fake_data["WARD"],
                           fake_data["TOWNSHIP"], fake_data["REG_STATUS"], fake_data["VOTE_SITE"])
