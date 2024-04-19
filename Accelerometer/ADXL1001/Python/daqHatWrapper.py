from daqhats import mcc128, OptionFlags, HatIDs, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, chan_list_to_mask
from time import sleep, time


def timeUS():
    """
    Returns system time to microseconds
    """
    return time() * 1000000
       
class daqhatsWrapper:
    """
    Wrap the daqhat library for ease of use
    """
    #hat-id for 128 is 326, according to the library reference
    def __init__(self, mprint, chanList=[1,2,3,4,5,6], debug=False, hat_id=326, sampleRate=6400): #open port/channel
        self.hat_id = hat_id
        self.sampleRate = sampleRate #with 6400 samples, can do 10 kS
        self.channelList = chan_list_to_mask(chanList)
        self.address = select_hat_device(HatIDs.MCC_128)
        self.hat = mcc128(self.address)
        self.numChannels = len(chanList)
        self.fileName = 'AccelerationData.csv'
        self.debug = debug
        self.mprint = mprint
        self.outputLog = open(self.fileName, 'w') #open file to write to, name it outputLog


    """
    Writes buffer data to the csv file
    
    Inputs:
        data: data in 1D list 
        numChannels: number of channels daqHat reading from
        startTime: time started reading data (in microseconds)
    
    Output: 
        saves data to file given with timestamps in leftmost column 
        using multiprint
    """
    def write_data_to_csv(self, data, startTime):
        data_csv = ''
        for row in range(len(data)/self.numChannels):
            data_csv += ("," if (row != int(len(data)/self.numChannels) - 1) else (str(time) + ",")) # Only write timestamp to last value
            for i in range(self.numChannels):
                data_csv += ("," + str(data[row*self.numChannels + i]))
            data_csv += "\n"
        data_csv = data_csv.removesuffix("\n")
        self.mprint.p(data_csv, self.outputLog)

    """
    Continuously records data from accelerometers to buffer, then calls write_data_to_csv to save data to csv
    
    Inputs:
        self: daqHat class
    
    Output:
        data saved to file
    """
    def read_write_data(self):
        samples_per_channel = 0
        read_request_size = -1 #read all available in buffer
        
        self.hat.a_in_mode_write(AnalogInputMode.SE)
        self.hat.a_in_range_write(AnalogInputRange.BIP_10V) #change from 10v later?
        self.hat.a_in_scan_start(self.channelList, samples_per_channel, self.sampleRate, OptionFlags.CONTINUOUS)
        timeout = 0     # Use 0 timeout to immediately read the buffer's contents, instead of waiting for it to fill.
        
        #check if pi can handle desired sampling rate
        if (self.debug): 
            actual_sampling_rate = self.hat.a_in_scan_actual_rate(self.numChannels, self.sampleRate)
            print("Actual sampling rate:", actual_sampling_rate)

        while True:
            try:                
                startTime = timeUS()
                #assign buffer values to sampleData then clear buffer
                sampleData = self.hat.a_in_scan_read(read_request_size, timeout)
                self.write_data_to_csv(sampleData.data, startTime)

                sleep(0.1)
            except KeyboardInterrupt:
                sampleStartTime = timeUS()
                sampleData= self.hat.a_in_scan_read(read_request_size, timeout) #get last values
                self.write_data_to_csv(sampleData.data, sampleStartTime)
                
                #closing all files/scans
                self.outputLog.close()
                self.hat.a_in_scan_stop() #stopping continuous scan
                self.hat.a_in_scan_cleanup() #cleaning up
                exit()
 
        
#initialize multiprinter as mprint
#mprint = MultiPrinter()
#daq = daqhatsWrapper(mprint, debug=True)
#daq.read_write_data()
