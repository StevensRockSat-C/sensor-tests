%% FFT Analysis for vibration testing data
clear, clc, close all

SAMPLE_RATE = 6400;

%% Get data from CSV
vibData = readmatrix('2024-02-14_12-35-51-ADXL1001-6400Hz-NotHeld-ACpower.csv');
    % 2024-02-15_17-34-21-ADXL1001-6400Hz-NotHeld-ACpower-DampenerMount.csv
    % 2024-02-14_12-35-51-ADXL1001-6400Hz-NotHeld-ACpower.csv
xData = vibData(:, 1);
N = length(xData);

%% Plot Voltage over Time
% figure(1)
% tData = linspace(0,N/SAMPLE_RATE, N);
% plot(tData,xData)

%% Plot FFT
figure(2)
xAmplitudeSpectrum=abs(fft(xData));
frequencies = (0:N-1) * (SAMPLE_RATE / N);
lowerHz = round(N / SAMPLE_RATE) * 5;
plot(frequencies(lowerHz:N/2), xAmplitudeSpectrum(lowerHz:N/2)); % Plotting half of the spectrum

title('Vibration Test Data by Frequency')
xlabel('Frequency (Hz)')
ylabel('Applitude')
legend('x-axis')

% figure(3)
% pspectrum(xData,SAMPLE_RATE,"spectrogram", ...
%     "FrequencyResolution", 0.5, ...
%     'FrequencyLimits', [100, 300], ... % Set frequency limits to exclude frequencies below 10 Hz
%     'OverlapPercent', 0, ... % Increase overlap for better frequency resolution
%     'Leakage', 0.1);            

figure(4)
pspectrum(xData,SAMPLE_RATE,"persistence", ...
    "FrequencyResolution", 3, ...
    'FrequencyLimits', [100, 3200], ... % Set frequency limits to exclude frequencies below 10 Hz
    'OverlapPercent', 90, ... % Increase overlap for better frequency resolution
    'Leakage', 0.5);

figure(5)

[p,f,t] = pspectrum(xData,SAMPLE_RATE,"spectrogram", ...
    "FrequencyResolution", 1, ...
    'FrequencyLimits', [100, 300], ... % Set frequency limits to exclude frequencies below 10 Hz
    'OverlapPercent', 40, ... % Increase overlap for better frequency resolution
    'Leakage', 0.2);      

waterfall(f,t,p')
xlabel('Frequency (Hz)')
ylabel('Time (seconds)')
wtf = gca;
wtf.XDir = 'reverse';
view([30 45])