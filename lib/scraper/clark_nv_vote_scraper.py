from lib.scraper import BaseVoterScrapper

EV_URL = "https://elections.clarkcountynv.gov/VoterRequestsTV/EVMB/ev_24P.zip"
VBM_URL = ""

class ClarkNVVoteScraper(BaseVoterScrapper):
    def __init__(self) -> None:
        super().__init__()
        raw_votes = []
        clean_votes = []
        pass

    def get_all_votes(self):
        self.get_vbm_votes()
        self.get_ev_votes()
        self.process_votes()
        return self.clean_votes
        # Add all votes to a list of Voters
    
    def get_vbm_votes():
        raise NotImplementedError() 
        # download all votes from VBM_URL parameter
        # add to the raw_votes list

    def get_ev_votes():
        raise NotImplementedError() 
        # download all ovtes from EV_URL parameter
        # add to the raw_votes list
    
    def process_votes():
        raise NotADirectoryError()
        #take raw_votes list, clean and create a list of voter objects