%files = dir('*.csv');
files = ["cropped_12-10-2019-11-08-56-current-0p5A-voltage-0p15V.csv",...
"cropped_12-10-2019-11-11-35-current-1p0A-voltage-0p29V.csv",...
"cropped_12-10-2019-11-14-36-current-1p5A-voltage-0p44V.csv",...
"cropped_12-10-2019-11-17-45-current-2p0A-voltage-0p58V.csv",...
"cropped_12-10-2019-11-20-37-current-2p5A-voltage-0p72V.csv",...
"cropped_12-10-2019-11-23-35-current-3p0A-voltage-0p86V.csv",...
"cropped_12-10-2019-11-26-35-current-3p5A-voltage-0p99V.csv",...
"cropped_12-10-2019-11-29-37-current-4p0A-voltage-1p15V.csv",...
"cropped_12-10-2019-11-32-36-current-4p5A-voltage-1p32V.csv",...
"cropped_12-10-2019-11-35-36-current-5p0A-voltage-1p51V.csv"];
power = zeros(length(files),1);
tube = zeros(4,length(files));
sLDOs = zeros(4,length(files));
sLDO_upper = zeros(4,length(files));
sLDO_lower = zeros(4,length(files));
module = zeros(4,length(files));
for i = 1:length(files)
    k = sprintf("reading %s",files(i));
    disp(k);
    data = csvread(files(i),1,1);
    d_tube = data(1,:);
    d_sLDOs = data(2,:);
    %d_sLDO_upper = data(3,:);
    %d_sLDO_lower = data(4,:);
    %d_module = data(5,:);
    
    power(i) = d_tube(7);
    
    tube(1,i) = d_tube(1);
    tube(2,i) = d_tube(2);
    tube(3,i) = d_tube(3);
    tube(4,i) = d_tube(4);
    
    sLDOs(1,i) = d_sLDOs(1);
    sLDOs(2,i) = d_sLDOs(2);
    sLDOs(3,i) = d_sLDOs(3);
    sLDOs(4,i) = d_sLDOs(4);
    
    %{
    sLDO_upper(1,i) = d_sLDO_upper(1);
    sLDO_upper(2,i) = d_sLDO_upper(2);
    sLDO_upper(3,i) = d_sLDO_upper(3);
    
    sLDO_lower(1,i) = d_sLDO_lower(1);
    sLDO_lower(2,i) = d_sLDO_lower(2);
    sLDO_lower(3,i) = d_sLDO_lower(3);
    
    module(1,i) = d_module(1);
    module(2,i) = d_module(2);
    module(3,i) = d_module(3);
    %}
    
end

tube_avg_T = tube(4,:);

figure(1);
f1 = polyfit(power,transpose(sLDOs(2,:)-tube_avg_T),1);
plot(power,sLDOs(2,:)-tube_avg_T,'k.','MarkerSize',12);
%ylim([0 35]);
hold on
plot(power,polyval(f1,power),'k--','LineWidth',0.8);
legend('Shunt LDOs','sLDOs (Fit)','Location','northwest');
title('\Delta T_{max} vs. Power');
xlabel('Power (W)');
ylabel('\Delta T_{max}');
txt1 = sprintf("y_1 = %.4fx1 + %.4f",f1(1),f1(2));
set(gca,'FontSize',16);
text(0.2,100,txt1,'FontSize',14,'Color','k');

%{
figure(2);
f1 = polyfit(power(5:end),transpose(sLDOs(2,5:end)-tube_avg_T(5:end)),1);
f2 = polyfit(power(5:end),transpose(module(2,5:end)-tube_avg_T(5:end)),1);
plot(power,sLDOs(2,:)-tube_avg_T,'k.',power,module(2,:)-tube_avg_T,'ro',power,sLDO_upper(2,:)-tube_avg_T,'b*',power,sLDO_lower(2,:)-tube_avg_T,'gx','MarkerSize',12);
ylim([0 35]);
hold on
plot(power(5:end),polyval(f1,power(5:end)),'k--',power(5:end),polyval(f2,power(5:end)),'r-.','LineWidth',0.8);
legend('Shunt LDOs','Entire Module','Upper sLDOs','Lower sLDOs','sLDOs (Fit)','Module (Fit)','Location','northwest');
title('\Delta T_{min} vs. Power');
xlabel('Power (W)');
ylabel('\Delta T_{min}');
txt1 = sprintf("y_1 = %.4fx1 + %.4f",f1(1),f1(2));
txt2 = sprintf("y_2 = %.4fx1 + %.4f",f2(1),f2(2));
set(gca,'FontSize',16);
text(0.2,20,txt1,'FontSize',14,'Color','k');
text(0.2,18,txt2,'FontSize',14,'Color','r');

figure(3);
f1 = polyfit(power(5:end),transpose(sLDOs(3,5:end)-tube_avg_T(5:end)),1);
f2 = polyfit(power(5:end),transpose(module(3,5:end)-tube_avg_T(5:end)),1);
plot(power,sLDOs(3,:)-tube_avg_T,'k.',power,module(3,:)-tube_avg_T,'ro',power,sLDO_upper(3,:)-tube_avg_T,'b*',power,sLDO_lower(3,:)-tube_avg_T,'gx','MarkerSize',12);
ylim([0 35]);
hold on
plot(power(5:end),polyval(f1,power(5:end)),'k--',power(5:end),polyval(f2,power(5:end)),'r-.','LineWidth',0.8);
legend('Shunt LDOs','Entire Module','Upper sLDOs','Lower sLDOs','sLDOs (Fit)','Module (Fit)','Location','northwest');
title('\Delta T_{avg} vs. Power');
xlabel('Power (W)');
ylabel('\Delta T_{avg}');
txt1 = sprintf("y_1 = %.4fx1 + %.4f",f1(1),f1(2));
txt2 = sprintf("y_2 = %.4fx1 + %.4f",f2(1),f2(2));
set(gca,'FontSize',16);
text(0.2,20,txt1,'FontSize',14,'Color','k');
text(0.2,18,txt2,'FontSize',14,'Color','r');
%}
