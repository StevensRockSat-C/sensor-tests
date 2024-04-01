import pytest
import daqHatWrapper

@pytest.fixture
def wrapper():
    return daqHatWrapper.daqhatsWrapper()

def test_wrapper_init(wrapper):
    assert wrapper.numChannels == 6
    assert wrapper.sampleRate == 6400
