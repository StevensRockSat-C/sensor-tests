import pytest
from daqHatWrapper import daqhatsWrapper

@pytest.fixture
def wrapper():
    return daqhatsWrapper()

def test_wrapper_init(wrapper):
    assert wrapper.numChannels == 6
    assert wrapper.sampleRate == 6400
