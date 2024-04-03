%% FFT Analysis for vibration testing data
clear, clc, close all

SAMPLE_RATE = 6400;

%% Get data from CSV
vibData = readmatrix('../Test Data/2024-02-14_6accelerometersHandShaken.csv');
    % 2024-02-15_17-34-21-ADXL1001-6400Hz-NotHeld-ACpower-DampenerMount.csv
    % 2024-02-14_12-35-51-ADXL1001-6400Hz-NotHeld-ACpower.csv
xData = vibData(:, 2:7); % Select columns 1 through 6 for vibration data
N = size(xData, 1);

%% Plot Voltage over Time
figure(1)
tData = linspace(0, N/SAMPLE_RATE, N);
plot(tData, xData)
legend('Accelerometer 1', 'Accelerometer 2', 'Accelerometer 3', 'Accelerometer 4', 'Accelerometer 5', 'Accelerometer 6')
xlabel('Time (seconds)')
ylabel('Voltage')
title('Voltage vs Time for Accelerometers')

%% Plot FFT for each accelerometer
figure(2)
frequencies = (0:N-1) * (SAMPLE_RATE / N);
lowerHz = round(N / SAMPLE_RATE) * 5;

for i = 1:6
    subplot(2, 3, i);
    xAmplitudeSpectrum = abs(fft(xData(:, i)));
    plot(frequencies(lowerHz:N/2), xAmplitudeSpectrum(lowerHz:N/2));
    title(['Accelerometer ', num2str(i), ' - Vibration Test Data by Frequency'])
    xlabel('Frequency (Hz)')
    ylabel('Amplitude')
end

legend('x-axis')

% figure(3)
% pspectrum(xData,SAMPLE_RATE,"spectrogram", ...
%     "FrequencyResolution", 0.5, ...
%     'FrequencyLimits', [100, 300], ... % Set frequency limits to exclude frequencies below 10 Hz
%     'OverlapPercent', 0, ... % Increase overlap for better frequency resolution
%     'Leakage', 0.1);            

figure(4)
for i = 1:6
    subplot(2, 3, i);
    pspectrum(xData(:, i), SAMPLE_RATE, "persistence", ...
        "FrequencyResolution", 3, ...
        'FrequencyLimits', [100, 3200], ...
        'OverlapPercent', 90, ...
        'Leakage', 0.5);
    title(['Accelerometer ', num2str(i)]);
end

figure(5)
for i = 1:6
    subplot(2, 3, i);
    [p, f, t] = pspectrum(xData(:, i), SAMPLE_RATE, "spectrogram", ...
        "FrequencyResolution", 5, ...
        'FrequencyLimits', [100, 300], ...
        'OverlapPercent', 40, ...
        'Leakage', 0.2);
    waterfall(f, t, p');
    xlabel('Frequency (Hz)')
    ylabel('Time (seconds)')
    wtf = gca;
    wtf.XDir = 'reverse';
    view([30 45])
    title(['Accelerometer ', num2str(i)]);
end