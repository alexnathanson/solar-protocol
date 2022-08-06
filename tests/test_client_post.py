import backend.core.clientPostIP as clientPostIP
from pytest import approx

def test_get_local_config():
    result = clientPostIP.getLocalConfig("whatever")
    assert result == None

    result = clientPostIP.getLocalConfig("name")
    assert result == 'pi'

def test_globals():
    assert clientPostIP.deviceList == "./tests/devicelist.json"