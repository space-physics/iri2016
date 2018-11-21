time = datetime(2015,12,13,10,0,0);
glat = 65.1;
glon = -147.5;
altKm = 100:10:1000;
%altKm = 100;

iono = iri2016(time, altKm, glat, glon);

%iono = iri_2016(time, altKm, glat, glon);

%% plot
plotiono(iono, 'nCI')
plotiono(iono, 'nN+')
plotiono(iono, 'nH+')

plotiono(iono)