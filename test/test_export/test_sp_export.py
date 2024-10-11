from unittest.mock import Mock

import pytest

from lib.export.sp_export import SPExport, CCNVExportError


def test_update_worker_success(mocker):
    # Fake variables
    fake_worker = {"spid": "12358", "activity_date": "2000-01-01", "vote_type": "Mail"}
    fake_url = "www.fakeurl.com"
    fake_api_key = "Fake API key 1234"
    fake_step_id = 12345
    fake_vote_date_detail_id = "0101"
    fake_vote_type_detail_id = "1010"
    fake_sp_session = "session"
    fake_export = SPExport(fake_sp_session, fake_url, fake_api_key, fake_step_id, fake_vote_date_detail_id, fake_vote_type_detail_id)

    # Mock function calls
    mock_add_step = mocker.patch("lib.export.sp_export.addStep")
    mock_add_detail = mocker.patch("lib.export.sp_export.addDetail")

    # Call update_worker
    fake_export.update_worker(fake_worker)

    # Assert functions called
    mock_add_step.assert_called()
    mock_add_detail.assert_called()


def test_update_worker_fail(mocker):
    # Fake variables
    fake_worker = {"spid": "12358", "activity_date": "2000-01-01", "vote_type": "Mail"}
    fake_url = "www.fakeurl.com"
    fake_api_key = "Fake API key 1234"
    fake_step_id = 12345
    fake_vote_date_detail_id = "0101"
    fake_vote_type_detail_id = "1010"
    fake_sp_session = "session"
    fake_export = SPExport(fake_sp_session, fake_url, fake_api_key, fake_step_id, fake_vote_date_detail_id, fake_vote_type_detail_id)

    # Mock function call
    mock_add_step = mocker.patch("lib.export.sp_export.addStep", side_effect=Exception)

    # Assert exception raised
    with pytest.raises(CCNVExportError, match=r"Failed to add step for worker 12358"):
        fake_export.update_worker(fake_worker)


def test_get_worker_voters(mocker):
    # Fake variables
    fake_client = "fake_client"
    fake_url = "www.fakeurl.com"
    fake_api_key = "Fake API key 1234"
    fake_step_id = 12345
    fake_vote_date_detail_id = "0101"
    fake_vote_type_detail_id = "1010"
    fake_sp_session = "session"
    fake_export = SPExport(fake_sp_session, fake_url, fake_api_key, fake_step_id, fake_vote_date_detail_id, fake_vote_type_detail_id)
    fake_local_num = "00000000"
    fake_state = "NJ"
    fake_county = "Hudson"
    fake_vp_schema = "political"
    fake_database = "Big Data"
    fake_data = [{"greeting": "hello"}, {"greeting": "hola"}]

    # Mock function call
    mock_query_civis = mocker.patch("lib.export.sp_export.select", return_value=fake_data)

    # Call get_worker_voters
    fake_export.get_worker_voters(fake_client, fake_local_num, fake_state, fake_county, fake_vp_schema, fake_database)

    # Assert query civis called and returned data
    mock_query_civis.assert_called()
    assert fake_export.worker_voters == fake_data


def test_sp_export_initial_state():
    fake_url = "www.fakeurl.com"
    fake_api_key = "Fake API key 1234"
    fake_step_id = 12345
    fake_vote_date_detail_id = "0101"
    fake_vote_type_detail_id = "1010"
    fake_sp_session = "session"
    fake_export = SPExport(fake_sp_session, fake_url, fake_api_key, fake_step_id, fake_vote_date_detail_id, fake_vote_type_detail_id)

    assert fake_export.external_state == []
    assert fake_export.sp_base_url == fake_url
    assert fake_export.sp_api_key == fake_api_key
    assert fake_export.step_id == fake_step_id


def test_get_external_state(mocker):
    fake_url = "www.fakeurl.com"
    fake_api_key = "Fake API key 1234"
    fake_step_id = 12345
    fake_vote_date_detail_id = "0101"
    fake_vote_type_detail_id = "1010"
    fake_sp_session = "session"
    fake_export = SPExport(fake_sp_session, fake_url, fake_api_key, fake_step_id, fake_vote_date_detail_id, fake_vote_type_detail_id)
    mock_sp_result = [{
        'type': 'Step',
        'stepDetailId': fake_step_id,
        'workerId': '545',
        'responseString': None,
        'responseBoolean': None,
        'responseDate': None,
        'responseNumber': None,
        'responseDecimal': None,
        'responseOption': None,
        'responseOptions': None
    }, {
        'type': 'Step',
        'stepDetailId': fake_step_id,
        'workerId': '546',
        'responseString': None,
        'responseBoolean': None,
        'responseDate': None,
        'responseNumber': None,
        'responseDecimal': None,
        'responseOption': None,
        'responseOptions': None
    }, {
        'type': 'Step',
        'stepDetailId': fake_step_id,
        'workerId': '547',
        'responseString': None,
        'responseBoolean': None,
        'responseDate': None,
        'responseNumber': None,
        'responseDecimal': None,
        'responseOption': None,
        'responseOptions': None
    }]

    mock_get_activity_participation = mocker.patch("lib.export.sp_export.getActivityParticipation",
                                                   return_value=mock_sp_result)

    fake_export.get_external_state()

    mock_get_activity_participation.assert_called_with(mocker.ANY, 'step', fake_step_id)
    assert fake_export.external_state == [{'spid': '545'}, {'spid': '546'}, {'spid': '547'}]
