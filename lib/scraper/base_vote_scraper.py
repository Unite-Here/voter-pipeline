

class BaseVoteImport():
    def __init__(self) -> None:
        pass

    def db_upsert(self):
        raise NotImplementedError()

    def get_all_votes(self):
        raise NotImplementedError() 

    