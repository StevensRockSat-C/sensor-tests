from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    chan_list_to_mask, input_mode_to_string, input_range_to_string
from time import sleep
from sys import stdout
from multiprint import MultiPrinter


class daqhatsWrapper:
    """
    Wrap the daqhat library for ease of use
    """
    #hat-id for 128 is 326, according to the library reference
    def __init__ (self, chanList, hat_id=326, sample_rate=6400): #open port/channel
        self.hat_id = hat_id
        self.sample_rate = 6400 #with 6400 samples, can do 10 kS
        self.channelList = chan_list_to_mask(chanList)
        self.address = select_hat_device(HatIDs.MCC_128)
        self.hat = mcc128(self.address)
        self.num_channels = len(chanList)

        #FOR TESTING
        self.overrun = False
        

        #read from buffer, returns csv using printwriter
        #put EVERYTHING in try catch for various errors
        #

        #close 
   

    def read_write_data(self, output_log):
        READ_ALL_AVAILABLE = -1
        samples_per_channel = 0
        read_request_size = READ_ALL_AVAILABLE
        self.hat.a_in_mode_write(AnalogInputMode.SE)
        self.hat.a_in_range_write(AnalogInputRange.BIP_10V) #change from 10v later?
        self.hat.a_in_scan_start(self.channelList, samples_per_channel, self.sample_rate, OptionFlags.CONTINUOUS)
        mprint = MultiPrinter()
        timeout = 5.0
        input_mode = AnalogInputMode
        
        
        def formatNum(n):
            return '{:.5f}'.format(n)
            
        while True:
            try:
                read_result = self.hat.a_in_scan_read(read_request_size, timeout)
                
                if (read_result.hardware_overrun | read_result.buffer_overrun):
                    self.overrun = True
                    
                mprint.p(",".join(map(lambda n: '{:.5f}'.format(n), read_result.data)), output_log) #joins all of data together with ,
                #read_result.data clears every time you read it so you are getting the new data each time
                stdout.flush()
                sleep(0.1)
            except KeyboardInterrupt:
                read_result = self.hat.a_in_scan_read(read_request_size, timeout)
                mprint.p(",".join(map(lambda n: '{:.5f}'.format(n), read_result.data)), output_log) #joins all of data together with ,
                exit()
        
            
    #        a_in_scan_cleanup()

output_log = open("accelerations.csv", 'w')

daq = daqhatsWrapper([1,2])
daq.read_write_data(output_log)
