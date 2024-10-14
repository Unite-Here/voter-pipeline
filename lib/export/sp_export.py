from operator import itemgetter

import civis
from uhlibs.civis.api import map_columns_to_values, select
from uhlibs.sepuede.api import SePuedeApiSession, addDetail, addStep, getActivityParticipation

from lib.export.base_export import BaseExport, BaseExportError
from lib.export.queries import GET_VOTERS_AFLCIO_MATCHED
from lib.utils.data import filter_dict_lists
from lib.voter.voter import Voter

CIVIS_PARAMETER_KEYS = [
    'name',
    'type',
    'value',
]


class CCNVExportError(BaseExportError):
    pass


class SPExport(BaseExport):

    def __init__(self, sp_session, step_id, vote_date_detail_id, vote_type_detail_id) -> None:
        super().__init__()
        self.step_id = step_id
        self.vote_date_detail_id = vote_date_detail_id
        self.vote_type_detail_id = vote_type_detail_id
        self.sp_session = sp_session

    def get_external_state(self):
        """
        Downloads from SePuede the list of current participants in the voted step
        updates external_state list with the list of spids returned.
        [{'spid': <worker-voter SePuede ID>}]
        """

        sp_voters = getActivityParticipation(self.sp_session, 'step', self.step_id)

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

    def find_differences(self) -> list[dict]:
        """
        Find worker_voters sepuede IDs not in external_state sepuede IDs
        """
        known = self.external_state
        unknown = self.worker_voters
        key = "spid"
        diff = filter_dict_lists(known, unknown, key)

        return diff

    def send_updates(self):
        """
        Update workers on sepuede
        """
        missing_workers = self.find_differences()
        for worker in missing_workers:
            self.update_worker(worker)

    def update_worker(self, worker: dict):
        """
        Update single worker
        """
        try:
            addStep(self.sp_session, worker["spid"], self.step_id)
        except Exception as err:
            raise CCNVExportError(f"Failed to add step for worker {worker['spid']}: {err}")
        try:
            addDetail(self.sp_session, worker["spid"], self.vote_date_detail_id, "responseDate", worker["activity_date"])
        except Exception as err:
            raise CCNVExportError(f"Failed to add vote date detail for worker {worker['spid']}: {err}")
        try:
            addDetail(self.sp_session, worker["spid"], self.vote_type_detail_id, "responseString", worker["vote_type"])
        except Exception as err:
            raise CCNVExportError(f"Failed to add vote type detail for worker {worker['spid']}: {err}")
