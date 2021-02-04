%files = dir('*.csv');
files = ["cropped_12-09-2019-21-29-35-current-0p0A-voltage-0p0V.csv",...
"cropped_12-09-2019-21-34-33-current-0p5A-voltage-0p13V.csv",...
"cropped_12-09-2019-21-37-39-current-1p0A-voltage-0p27V.csv",...
"cropped_12-09-2019-21-40-36-current-1p5A-voltage-0p41V.csv",...
"cropped_12-09-2019-21-43-36-current-2p0A-voltage-0p54V.csv",...
"cropped_12-09-2019-21-46-36-current-2p5A-voltage-0p71V.csv",...
"cropped_12-09-2019-21-49-36-current-3p0A-voltage-0p83V.csv",...
"cropped_12-09-2019-21-52-38-current-3p5A-voltage-0p90V.csv",...
"cropped_12-09-2019-21-55-37-current-4p0A-voltage-0p99V.csv",...
"cropped_12-09-2019-21-58-36-current-4p5A-voltage-1p09V.csv",...
"cropped_12-09-2019-22-02-01-current-5p0A-voltage-1p14V.csv"];
power = zeros(length(files),1);
tube = zeros(4,length(files));
sLDOs = zeros(4,length(files));
for i = 1:length(files)
    k = sprintf("reading %s",files(i));
    disp(k);
    data = csvread(files(i),1,1);
    d_tube = data(1,:);
    d_sLDOs = data(2,:);
    
    power(i) = d_tube(7);
    
    tube(1,i) = d_tube(1);
    tube(2,i) = d_tube(2);
    tube(3,i) = d_tube(3);
    tube(4,i) = d_tube(4);
    
    sLDOs(1,i) = d_sLDOs(1);
    sLDOs(2,i) = d_sLDOs(2);
    sLDOs(3,i) = d_sLDOs(3);
    sLDOs(4,i) = d_sLDOs(4);
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
ylabel('\Delta T');
txt1 = sprintf("y = %.4fx + %.4f",f1(1),f1(2));
set(gca,'FontSize',16);
text(0.2,15,txt1,'FontSize',14,'Color','k');
