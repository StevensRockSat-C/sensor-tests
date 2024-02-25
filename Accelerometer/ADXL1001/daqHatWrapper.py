from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    chan_list_to_mask, input_mode_to_string, input_range_to_string

class daqhatsWrapper:
    """
    Wrap the daqhat library for ease of use
    """
    #hat-id for 128 is 326, according to the library reference
    def __init__ (self, channelList, hat_id=326, sample_rate=6400): #open port/channel
        self.hat_id = hat_id
        self.sample_rate = 6400 #with 6400 samples, can do 10 kS
        self.channelList = chan_list_to_mask(channelList)
        self.address = mcc128(select_hat_device(HatIDs.MCC_128))

        #FOR TESTING
        self.overrun = False

        #read from buffer, returns csv using printwriter
        #put EVERYTHING in try catch for various errors
        #

        #close 
   

    def _read_buffer(self):
        total_samples_read = 0
        read_request_size = READ_ALL_AVAILABLE

        timeout = 5.0

        while True:
            read_result = self.hat.a_in_scan_read(read_request_size, timeout)
            if (read_result.hardware_overrun | read_result.buffer_overrun):
                self.overrun = True
            
    #        a_in_scan_cleanup()


daq = daqhatsWrapper([1,2,3])