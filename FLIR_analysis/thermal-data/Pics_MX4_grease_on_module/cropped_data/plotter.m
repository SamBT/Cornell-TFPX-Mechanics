files = dir('*.csv');
power = zeros(length(files),1);
tube = zeros(3,length(files));
sLDOs = zeros(3,length(files));
sLDO_upper = zeros(3,length(files));
sLDO_lower = zeros(3,length(files));
module = zeros(3,length(files));
for i = 1:length(files)
    data = csvread(files(i).name,1,1);
    d_tube = data(1,:);
    d_sLDOs = data(2,:);
    d_sLDO_upper = data(3,:);
    d_sLDO_lower = data(4,:);
    d_module = data(5,:);
    
    power(i) = d_tube(6);
    
    tube(1,i) = d_tube(1);
    tube(2,i) = d_tube(2);
    tube(3,i) = d_tube(3);
    
    sLDOs(1,i) = d_sLDOs(1);
    sLDOs(2,i) = d_sLDOs(2);
    sLDOs(3,i) = d_sLDOs(3);
    
    sLDO_upper(1,i) = d_sLDO_upper(1);
    sLDO_upper(2,i) = d_sLDO_upper(2);
    sLDO_upper(3,i) = d_sLDO_upper(3);
    
    sLDO_lower(1,i) = d_sLDO_lower(1);
    sLDO_lower(2,i) = d_sLDO_lower(2);
    sLDO_lower(3,i) = d_sLDO_lower(3);
    
    module(1,i) = d_module(1);
    module(2,i) = d_module(2);
    module(3,i) = d_module(3);
    
end

tube_avg_T = tube(3,:);

figure(1);
f1 = polyfit(power(5:end),transpose(sLDOs(1,5:end)-tube_avg_T(5:end)),1);
f2 = polyfit(power(5:end),transpose(module(1,5:end)-tube_avg_T(5:end)),1);
plot(power,sLDOs(1,:)-tube_avg_T,'k.',power,module(1,:)-tube_avg_T,'ro',power,sLDO_upper(1,:)-tube_avg_T,'b*',power,sLDO_lower(1,:)-tube_avg_T,'gx','MarkerSize',12);
ylim([0 35]);
hold on
plot(power(5:end),polyval(f1,power(5:end)),'k--',power(5:end),polyval(f2,power(5:end)),'r-.','LineWidth',0.8);
legend('Shunt LDOs','Entire Module','Upper sLDOs','Lower sLDOs','sLDOs (Fit)','Module (Fit)','Location','northwest');
title('\Delta T_{max} vs. Power');
xlabel('Power (W)');
ylabel('\Delta T_{max}');
txt1 = sprintf("y_1 = %.4fx1 + %.4f",f1(1),f1(2));
txt2 = sprintf("y_2 = %.4fx1 + %.4f",f2(1),f2(2));
set(gca,'FontSize',16);
text(0.2,20,txt1,'FontSize',14,'Color','k');
text(0.2,18,txt2,'FontSize',14,'Color','r');


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
