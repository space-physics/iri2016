%% simple
time = datenum(2015,12,13,10,0,0);
glat = 65.1;
glon = -147.5;
altkmrange = [100,1000,10];

cwd = fileparts(mfilename('fullpath'));
addpath(fullfile(cwd, '/../matlab'))

iono = iri2016(time, glat, glon,  altkmrange);

assert(abs(iono.Ne(11) - 3.986688e9) < 1e5, 'Ne error excessive')

if isoctave
  disp('OK: IRI2016 GNU Octave')
else
  disp('OK: IRI2016 Matlab')
end
