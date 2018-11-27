%% Altitude profile with IRI2016
glat = -11.95;
glon = -76.77;
altkmrange = [100, 200, 20];
t0 = datenum(2004,11,21,0,0,0);
t1 = datenum(2004,11,22,0,0,0);
ts = 3600;

times = datetimerange(t0, t1, ts);

for i = 1:length(times)
    iri(i) = iri2016(times(i), glat, glon, altkmrange);
end

plottime(iri, times, glat, glon)
