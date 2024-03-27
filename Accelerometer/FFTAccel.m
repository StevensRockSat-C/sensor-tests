%% FFT Analysis for vibration testing data
clear, clc, close all

vibData = readmatrix('2_5_24_adxl372_mounted159hz_python6400hz_test.csv');
xData = vibData(:, 2);
yData = vibData(:, 3);
zData = vibData(:, 4);

figure(1)
xAmplitudeSpectrum=abs(fft(xData));
yAmplitudeSpectrum=abs(fft(yData));
zAmplitudeSpectrum=abs(fft(zData));
f=linspace(0,65535,length(xAmplitudeSpectrum));
plot(f(5:1000),xAmplitudeSpectrum(5:1000), ...
    f(5:1000),yAmplitudeSpectrum(5:1000), ...
    f(5:1000),zAmplitudeSpectrum(5:1000));

title('Vibration Test Data by Frequency')
xlabel('Frequency (Hz)')
ylabel('Applitude')
legend('x-axis', 'y-axis', 'z-axis')