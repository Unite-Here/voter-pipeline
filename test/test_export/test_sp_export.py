import pytest

from lib.export.sp_export import SPExport

def test_sp_export_initial_state():
    fake_url = "www.fakeurl.com"
    fake_api_key = "Fake API key 1234"
    fake_step_id = 12345
    test_export = SPExport(fake_url, fake_api_key, fake_step_id)

    assert test_export.external_state == []
    assert test_export.sp_base_url == fake_url
    assert test_export.sp_api_key == fake_api_key
    assert test_export.step_id == fake_step_id

def test_get_external_state(mocker):
    fake_url = "www.fakeurl.com"
    fake_api_key = "Fake API key 1234"
    fake_step_id = 12345
    test_export = SPExport(fake_url, fake_api_key, fake_step_id)
    mock_sp_result = [
        {
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
        },
        {
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
        },
        {
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
        }
    ]

    mock_get_activity_participation = mocker.patch("lib.export.sp_export.getActivityParticipation", return_value=mock_sp_result)
    mock_sepuede_session = mocker.patch("lib.export.sp_export.SePuedeApiSession")

    test_export.get_external_state()

    mock_sepuede_session.assert_called_with(fake_url, fake_api_key)
    mock_get_activity_participation.assert_called_with(mocker.ANY, 'step', fake_step_id)
    assert test_export.external_state == [{'spid': '545'}, {'spid': '546'}, {'spid': '547'}]
