%% Stevens RockSatC - ISTR - Spring 2023
% Leak rates
clear, clc, close all

format long

%% Reading in Files
% Reading in CSV files
Valve_Xvalve_dat = readmatrix('3-6-23_Parker_MINI.csv');
Control_dat = readmatrix('3-7-23_MPRLS_Empty.csv');
Control2_dat = readmatrix('3-19-23_MINI_failed_Baseline2.csv');
Valve_AscoS_dat = readmatrix('3-20-23_MINI_TAKE2.csv');

%% Data Cleanup
% % Converting epoch time to uint64 
% %     (kept for formatting, this is harder to deal with than what I'm actually using below)
% Xvalve_time = uint64(Xvalve_dat(:,1));
% Control_time = uint64(Control_dat(:,1));
% Xvalve_time = datetime(Xvalve_dat(:,1), 'ConvertFrom', 'epochtime', 'TicksPerSecond', 1e6, 'Format', 'hh:mm:ss:SSSS');
% Control_time = datetime(Control_dat(:,1), 'ConvertFrom', 'epochtime', 'TicksPerSecond', 1e6, 'Format','hh:mm:ss:SSSS');

% Converting microseconds to minutes and aligning time axes
Xvalve_t = ((Valve_Xvalve_dat(:,1)-Valve_Xvalve_dat(1,1))/1e6)/60;
Control_t = ((Control_dat(:,1)-Control_dat(1,1))/1e6)/60;
Control2_t = ((Control2_dat(:,1)-Control2_dat(1,1))/1e6)/60;
AscoS_t = ((Valve_AscoS_dat(:,1)-Valve_AscoS_dat(1,1))/1e3)/60;   %This test was run in milliseconds, so we divide by 1e3 instead of 1e6

% Zeroing out time and pressure terms
%   Sets first term to (t, P) = (0, 0)

Control_t0 = Control_t([10:end]) - Control_t(10);
Control2_t0 = Control2_t([9:end]) - Control2_t(9);
Xvalve_t0 = Xvalve_t([48:end]) - Xvalve_t(48);
AscoS_t0 = AscoS_t([10:end]) - AscoS_t(10);

Control_p0 = Control_dat([10:end],2) - Control_dat(10,2);
Control2_p0 = Control2_dat([9:end],2) - Control2_dat(9,2);
Xvalve_p0 = Valve_Xvalve_dat([48:end],2) - Valve_Xvalve_dat(48,2);
AscoS_p0 = Valve_AscoS_dat([10:end],2) - Valve_AscoS_dat(10,2);

ControlAvg_p0 = (Control_p0(1:460) + Control2_p0)./2;

%Calulating Pressure change rates
for i = 2:size(Control_p0, 1)
    Control_Rate(i-1) = (Control_p0(i) - Control_p0(i-1))/(Control_t0(i) - Control_t0(i-1));
end

for i = 2:size(Control2_p0, 1)
    Control2_Rate(i-1) = (Control2_p0(i) - Control2_p0(i-1))/(Control2_t0(i) - Control2_t0(i-1));
end

for i = 2:size(ControlAvg_p0, 1)
    ControlAvg_Rate(i-1) = (ControlAvg_p0(i) - ControlAvg_p0(i-1))/(Control2_t0(i) - Control2_t0(i-1));
end

for i = 2:size(Xvalve_p0, 1)
    Xvalve_Rate(i-1) = (Xvalve_p0(i) - Xvalve_p0(i-1))/(Xvalve_t0(i) - Xvalve_t0(i-1));
end

for i = 2:size(AscoS_p0, 1)
    AscoS_Rate(i-1) = (AscoS_p0(i) - AscoS_p0(i-1))/(AscoS_t0(i) - AscoS_t0(i-1));
end

%Finding Valve leak rates
Xvalve_LeakRate = ControlAvg_Rate(1:302) - Xvalve_Rate;
AscoS_LeakRate = AscoS_Rate(1:459) - ControlAvg_Rate;

%% Plotting
% figure(1)
% hold on
% plot(Control_t, Control_dat(:,2))
% plot(Control2_t, Control2_dat(:,2))
% plot(Xvalve_t, Valve_Xvalve_dat(:,2))
% plot(AscoS_t, Valve_AscoS_dat(:,2))
% xlabel('Time, [min]')
% ylabel('Pressure, [hPa]')
% title('Pressure Change Over Time, Raw Data')
% legend('Control', 'Control2', 'XValve', 'Asco411')
% hold off
% 
% figure(2)
% hold on
% plot(Control_t([10:end]), Control_dat([10:end],2))
% plot(Control2_t([9:end]), Control2_dat([9:end],2))
% plot(Xvalve_t([48:end]), Valve_Xvalve_dat([48:end],2))
% plot(AscoS_t([10:end]), Valve_AscoS_dat([10:end],2))
% xlabel('Time, [min]')
% ylabel('Pressure, [hPa]')
% title('Pressure Change Over Time, Trimmed Data')
% legend('Control', 'Control2', 'XValve', 'Asco411')
% hold off
% 
% figure(3)
% hold on
% plot(Control_t0, Control_p0)
% plot(Control2_t0, Control2_p0)
% plot(Xvalve_t0, Xvalve_p0)
% plot(AscoS_t0, AscoS_p0)
% xlabel('Time, [min]')
% ylabel('Pressure delta from Min, [hPa]')
% title('Pressure Change Over Time, Zeroed Data')
% legend('Control', 'Control2', 'XValve', 'Asco411')
% hold off

% figure(4)
% hold on
% plot(Control2_t0, ControlAvg_p0, 'Linewidth', 3)
% plot(Xvalve_t0, Xvalve_p0, 'Linewidth', 3)
% plot(AscoS_t0, AscoS_p0, 'Linewidth', 3)
% xlabel('Time, [min]')
% ylabel('Pressure delta from Min, [hPa]')
% title('Pressure Change Over Time, Zeroed Data, Averaged Control')
% legend('Control Average', 'XValve', 'Asco Series S')
% hold off
% 
windowSize = 20; 
b = (1/windowSize)*ones(1,windowSize);
a = 1;
Xvalve_filter = filter(b, a, Xvalve_Rate);
AscoS_filter = filter(b, a, AscoS_Rate(30:end));

% figure(5)
% hold on
% plot(Xvalve_t0(1:302), smoothdata(Xvalve_Rate))
% plot(AscoS_t0(30:1016), smoothdata(AscoS_Rate(30:end)))
% hold off
% alpha(0.9)
% hold on
% plot(Xvalve_t0(1:302), Xvalve_filter, 'k', 'Linewidth', 3)
% plot(AscoS_t0(30:1016), AscoS_filter, 'Linewidth', 3)
% hold off
% xlabel('Time, [min]')
% ylabel('Leak Rate, [hPa/min]')
% title('Valve Leak Rates over Time')
% legend('Xvalve Raw', 'Asco Series S Raw', 'Xvalve Moving Avg', 'Asco S Moving Avg')

Xvalve_LR_filter = filter(b, a, Xvalve_LeakRate);
AscoS_LR_filter = filter(b, a, AscoS_LeakRate(30:end));

% figure(6)
% hold on
% plot(Xvalve_t0(1:302), smoothdata(Xvalve_LeakRate))
% plot(AscoS_t0(30:302), smoothdata(AscoS_LeakRate(30:302)))
% hold off
% alpha(0.9)
% hold on
% plot(Xvalve_t0(1:302), Xvalve_LR_filter, 'k', 'Linewidth', 3)
% plot(AscoS_t0(30:302), AscoS_LR_filter(30:302), 'Linewidth', 3)
% hold off
% xlabel('Time, [min]')
% ylabel('Leak Rate, [hPa/min]')
% title('Valve Leak Rates over Time')
% legend('Xvalve Raw', 'Asco Series S Raw', 'Xvalve Moving Avg', 'Asco S Moving Avg')

