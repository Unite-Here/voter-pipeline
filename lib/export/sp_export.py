from operator import itemgetter

from lib.export.base_export import BaseExport, BaseExportError
from lib.voter.voter import Voter

from uhlibs.sepuede.api import SePuedeApiSession, getActivityParticipation


STEP_ID = 107

class CCNVExportError(BaseExportError):
    pass


class SPExport(BaseExport):

    def __init__(self, sp_base_url, sp_api_key, step_id) -> None:
        super().__init__()
        self.sp_base_url = sp_base_url
        self.sp_api_key = sp_api_key
        self.step_id = step_id

    def get_external_state(self):
        """
        downloads from SePuede the list of current participants in the voted step
        updates external_state list with the list of spids returned.
        [{'spid': <worker-voter SePuede ID>}]
        """
        session = SePuedeApiSession(self.sp_base_url, self.sp_api_key)
        
        sp_voters = getActivityParticipation(session, 'step', self.step_id)

        self.external_state = list(map(self._extract_rename, sp_voters))


    def _extract_rename(dict):
        return {'spid': dict['workerId']}
    
