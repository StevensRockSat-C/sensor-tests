from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    chan_list_to_mask
from time import sleep, time
from sys import stdout
from multiprint import MultiPrinter


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
    def write_data_to_csv(self, data, numChannels, startTime):
        time_per_sample = 156.25 # 1/sampling_rate * (10^6 conversion to microseconds)
        rows=0
        data_csv = ''
        
        sample_time = startTime - (((1.0)*len(data)/numChannels) * time_per_sample) # total samples * time between samples
        while (len(data)/numChannels > rows):
            data_csv += str(sample_time)
            for i in range(numChannels):
                data_csv += ("," + str(data[rows*numChannels + i]))
            data_csv += "\n"
            rows += 1
            sample_time += time_per_sample
        if (self.debug and (sample_time != startTime)): raise Exception("NOT CALCULATING MID-SAMPLE TIMES CORRECTLY!")
        data_csv = data_csv.removesuffix("\n")
        self.mprint.p(data_csv, self.outputLog)
    
    """
    Same as write_data_to_csv, but without timestamps
    """
    def write_data_to_csv_no_times(self, data, numChannels, time=None):
        data_csv = ''
        for row in range(int(len(data)/numChannels)):
            data_csv += ("," if (row != int(len(data)/numChannels) - 1) else (str(time) + ",")) # Only write timestamp to last value
            for i in range(numChannels):
                data_csv += (str(data[row*numChannels + i]) + ",")
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
                
                #self.write_data_to_csv(sampleData.data, self.numChannels, startTime)
                self.write_data_to_csv_no_times(sampleData.data, self.numChannels)
                sleep(0.1)
            except KeyboardInterrupt:
                sampleStartTime = timeUS()
                sampleData= self.hat.a_in_scan_read(read_request_size, timeout) #get last values
                #self.write_data_to_csv(sampleData.data, self.numChannels, sampleStartTime)
                self.write_data_to_csv_no_times(sampleData.data, self.numChannels)
                
                #closing all files/scans
                outputLog.close()
                self.hat.a_in_scan_stop() #stopping continuous scan
                self.hat.a_in_scan_cleanup() #cleaning up
                exit()
 
        
#initialize multiprinter as mprint
mprint = MultiPrinter()
daq = daqhatsWrapper(mprint, debug=True)
daq.read_write_data()
