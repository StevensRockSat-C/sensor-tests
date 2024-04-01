from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    chan_list_to_mask, input_mode_to_string, input_range_to_string
from sys import stdout
from time import sleep

class daqhatsWrapper:
    """
    Wrap the daqhat library for ease of use
    """
    #hat-id for 128 is 326, according to the library reference
    def __init__ (self, channelList, fileName='out.txt', hat_id=326, sample_rate=6400): #open port/channel
        self.hat_id = hat_id
        self.sample_rate = 6400 #with 6400 samples, can do 10 kS
        self.channelList = chan_list_to_mask(channelList)
        self.hat = select_hat_device(HatIDs.MCC_128)
        self.address = mcc128(self.hat)
        self.num_channels = len(channelList)

        #open file to write to
        f = open(fileName, 'w', encoding="utf-8")

        samples_per_channel = 0
        try:
            self.hat.a_in_scan_start(self.channelList, 0, self.sample_rate, OptionFlags.CONTINUOUS)
        except(HatError, ValueError): 
            # WHAT THEN
            pass

        #FOR TESTING
        self.overrun = False

        #read from buffer, returns csv using printwriter
        #put EVERYTHING in try catch for various errors
        #

        #close 
    def _read_and_display_data(self, num_channels):
    
        total_samples_read = 0
        read_request_size = -1

    # When doing a continuous scan, the timeout value will be ignored in the
    # call to a_in_scan_read because we will be requesting that all available
    # samples (up to the default buffer size) be returned.
        timeout = 5.0

    # Read all of the available samples (up to the size of the read_buffer which
    # is specified by the user_buffer_size).  Since the read_request_size is set
    # to -1 (READ_ALL_AVAILABLE), this function returns immediately with
    # whatever samples are available (up to user_buffer_size) and the timeout
    # parameter is ignored.
        while True:
            read_result = self.hat.a_in_scan_read(read_request_size, timeout)

            # Check for an overrun error
            if read_result.hardware_overrun:
                print('\n\nHardware overrun\n')
                break
            elif read_result.buffer_overrun:
                print('\n\nBuffer overrun\n')
                break

            samples_read_per_channel = int(len(read_result.data) / self.num_channels)
            total_samples_read += samples_read_per_channel

            # Display the last sample for each channel.
            print('\r{:12}'.format(samples_read_per_channel),
                ' {:12} '.format(total_samples_read), end='')

            if samples_read_per_channel > 0:
                index = samples_read_per_channel * self.num_channels - self.num_channels

                for i in range(num_channels):
                    print('{:10.5f}'.format(read_result.data[index+i]), 'V ',
                        end='')
                stdout.flush()

                sleep(0.1)

        print('\n')
   

    def _read_buffer(self):
        total_samples_read = 0
        read_request_size = -1 #-1 means read all avilable samples

        timeout = 5.0

        while True:
            read_result = self.hat.a_in_scan_read(read_request_size, timeout)
            if (read_result.hardware_overrun | read_result.buffer_overrun):
                self.overrun = True     #say that it's overrun, but don't stop reading

            samples_read_per_channel = int(len(read_result.data) / self.num_channels)
            total_samples_read += samples_read_per_channel
            #how is that data returned?


    def _close_file(self,f):
        f.close()

daq = daqhatsWrapper([1,2,3])