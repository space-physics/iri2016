%% simple
time = datetime(2015,12,13,10,0,0);
glat = 65.1;
glon = -147.5;
altkmrange = [100,1000,10];

cwd = fileparts(mfilename('fullpath'));
addpath([cwd,'/../matlab'])

iono = iri2016(time, glat, glon,  altkmrange);


assert(abs(iono.Ne(1) - 2.197662e9) < 1e5, 'Ne error excessive')
