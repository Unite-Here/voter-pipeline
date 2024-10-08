import pytest

from lib.export.base_export import BaseExport

def test_export_initial_state():
    base_export = BaseExport()

    assert base_export.external_state == []

def test_export_not_implemented():
    base_export = BaseExport()
    with pytest.raises(NotImplementedError):
        base_export.export()