from operator import itemgetter

import civis
from uhlibs.civis.api import map_columns_to_values, select
from uhlibs.sepuede.api import SePuedeApiSession, getActivityParticipation

from lib.export.base_export import BaseExport, BaseExportError
from lib.export.queries import GET_VOTERS_AFLCIO_MATCHED
from lib.voter.voter import Voter
from lib.utils.data import filter_lists

CIVIS_PARAMETER_KEYS = [
    'name',
    'type',
    'value',
]


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
        Downloads from SePuede the list of current participants in the voted step
        updates external_state list with the list of spids returned.
        [{'spid': <worker-voter SePuede ID>}]
        """
        session = SePuedeApiSession(self.sp_base_url, self.sp_api_key)

        sp_voters = getActivityParticipation(session, 'step', self.step_id)

        self.external_state = list(map(self._extract_rename, sp_voters))

    def _extract_rename(self, dict):
        return {'spid': dict['workerId']}

    def get_worker_voters(self, client, local_num, state, county, vp_schema, database):
        """
        Query civis for list of voters joined with aflcio_matchfiles_merged

        Parameters
        ----------
        client : civis client
        local_num : string
        state : string
        county : string
        vp_schema : string
        database : string

        Returns
        -------
        list[dict]
            Query results as list of dictionaries
        """

        vp_params_list = [["local_number", "string", local_num], ["state", "string", state],
                          ["county", "string", county], ["vp_schema", "string", vp_schema]]

        vp_params = map_columns_to_values(CIVIS_PARAMETER_KEYS, vp_params_list)

        self.worker_voters = select(client, GET_VOTERS_AFLCIO_MATCHED, vp_params, database)

    def get_worker_voters_spids(self):
        """
        Get dict list of spid in worker_voters
        """
        spids = []
        for item in self.worker_voters:
            val = {"spid": item["spid"]}
            spids.append(val)

        return spids

    def find_differences(self):
        """
        Find worker_voters sepuede IDs not in external_state sepuede IDs
        """
        diff = filter_lists(self.external_state, self.get_worker_voters_spids())

        return diff
