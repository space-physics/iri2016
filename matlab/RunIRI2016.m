%time = datetime(2015,12,13,10,0,0);
time = datetime(2008,03,26,13,3,0);
glat = 65.1;
glon = -147.5;
altkmrange = [100,1000,10];
%altKm = 100;

iono = iri2016(time, altkmrange, glat, glon);
%% plot
plotiono(iono, 'nN+')
plotiono(iono, 'ne')

plotiono(iono)