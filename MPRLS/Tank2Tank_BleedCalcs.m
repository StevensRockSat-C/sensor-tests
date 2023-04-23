%% RockSatC
% Tank-to-Tank Emergency Bleed Time Calculations

clear, clc

%% Problem Setup
% Defininf theremodynamic properties
R = 287;            %[J/(kg*K)]
M = 0.02896;        %[kg/mol]
mu = 1.474e-5;      %[kg/(m*s)], Dynamic viscosity of air at -50 deg C
                    %   Not normally constant, but collection periods will
                    %    take place at roughly same temp
                    
% Defining payload terms
Dint = 0.125*0.0254;                %[m], 1/8" dia internal tubing, in -> m
Pdiff = 30;                         %[kPa], difference in pressure btwn sample tanks
Ldiff = 300/1000;                   %[m], line length btwn sample tanks 

% Bleed time calculations
Vol_bleed = Ldiff.*(pi/4)*Dint^2;                   %[m^3]
Q = (Pdiff./Ldiff).*(pi/128)*((Dint^4)/(mu/100));   %[m^3/s], Volumetric flow rate of gas for given deltaP
BleedTime = Vol_bleed./Q;                           %[s], Time to bleed