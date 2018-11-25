time = datenum(2015,12,13,10,0,0);
glat = 65.1;
glon = -147.5;
altkmrange = [100,1000,10];

iono = iri2016(time, glat, glon,altkmrange);

plotiono(iono, time, glat, glon)