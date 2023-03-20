%% Stevens RockSatC - ISTR - Spring 2023
clear, clc, close all

format long

%% Setup
%Reading in CSV files
Xvalve_dat = readmatrix('3-6-23_Parker_MINI.csv');
Control_dat = readmatrix('3-7-23_MPRLS_Empty.csv');

%Converting epoch time to human time
% Xvalve_time = uint64(Xvalve_dat(:,1));
% Control_time = uint64(Control_dat(:,1));

% a1 = Xvalve_time(1,1);
% a2 = Control_time(1,1);

%Converting microseconds to minutes
Xvalve_time(:,1) = ((Xvalve_dat(:,1)-Xvalve_dat(1,1))/1e6)/60;
Control_time(:,1) = ((Control_dat(:,1)-Control_dat(1,1))/1e6)/60;

% Xvalve_time = datetime(Xvalve_dat(:,1), 'ConvertFrom', 'epochtime', 'TicksPerSecond', 1e6, 'Format', 'hh:mm:ss:SSSS');
% Control_time = datetime(Control_dat(:,1), 'ConvertFrom', 'epochtime', 'TicksPerSecond', 1e6, 'Format','hh:mm:ss:SSSS');

%Calulating differences
XValve_LeakRate = Xvalve_dat([48:350],2) - Control_dat([48:350],2);



%% Plotting
figure(1)
hold on
% plot(Control_time([10, end],1), Control_dat([10, end],2))
% plot(Xvalve_time([48, end],1), Xvalve_dat([48, end],2))
hold off

figure(2)
hold on
plot(Control_time(:,1), Control_dat(:,2))
plot(Xvalve_time(:,1), Xvalve_dat(:,2))
hold off

figure(3)
plot(Xvalve_time([48:350],1), XValve_LeakRate)
xlabel('Time, [min]')
ylabel('Pressure Loss Rate, [hPa/min]')
title('Xvalve Leak Rate')

