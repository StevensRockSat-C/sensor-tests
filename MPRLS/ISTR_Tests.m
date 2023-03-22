%% Stevens RockSatC - ISTR - Spring 2023
% Leak rates
clear, clc, close all

format long

%% Reading in Files
% Reading in CSV files
Test1_SampCol_dat = readmatrix('3-20-23_sample_collection.csv');
Test2_Bleed_dat = readmatrix('3-20-23_bleed_test.csv');


%% Data Cleanup
% Converting microseconds to minutes and aligning time axes
SampleCol_t = ((Test1_SampCol_dat(:,1)-Test1_SampCol_dat(1,1))/1e6);
Bleed_t = ((Test2_Bleed_dat(:,1)-Test2_Bleed_dat(1,1))/1e3)/60;

%Pulling Pressure Data
SampleCol_p = Test1_SampCol_dat(:,2)./10;
Bleed1_p = Test2_Bleed_dat(:,2)./10;
Bleed2_p = Test2_Bleed_dat(:,3)./10;

%% Plotting
SampleCol_t0 = SampleCol_t(591:end) - SampleCol_t(591);

figure(1)
plot(SampleCol_t0, SampleCol_p(591:end), 'Linewidth', 3)
title('Sample Collection Test')
xlabel('Time, [s]')
ylabel('Tank Pressure, [kPa]')

figure(2)
plot(Bleed_t(4923:end), [Bleed1_p(4923:end), Bleed2_p(4923:end)], 'Linewidth', 3)
title('Bleed Validation')
xlabel('Time, [s]')
ylabel('Tank Pressure, [kPa]')
legend('Bleed Tank Pressure', 'Sample Tank Pressure')

