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
   

    def _read_write_data(self):
        total_samples_read = 0
        read_request_size = READ_ALL_AVAILABLE

        timeout = 5.0

        input_mode = AnalogInputMode
        while True:
            try:
                read_result = self.hat.a_in_scan_read(read_request_size, timeout)
                if (read_result.hardware_overrun | read_result.buffer_overrun):
                    self.overrun = True
                samples_read_per_channel = int(len(read_result.data)/self.num_channels)

                if samples_read_per_channel >0:
                    index = samples_read_per_channel * self.num_channels - self.num_channels

                    for i in range(self.num_channels):
                        csv_string += '{:.5f},'.format(read_result.data[index+i])
                        print('{:1-.5f}'.format(read_result.data[index+i]),end='')
                    stdout.flush()
                sleep(0.1)
            except KeyboardInterrupt:
                print(csv_string)
                exit()
        
            
    #        a_in_scan_cleanup()


daq = daqhatsWrapper([1,2,3])
daq.read_write_data()
