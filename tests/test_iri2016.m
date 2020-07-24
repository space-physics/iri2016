% setup
cwd = fileparts(mfilename('fullpath'));
addpath(fullfile(cwd, '/../matlab'))

%% simple
time = datenum(2015,12,13,10,0,0);
glat = 65.1;
glon = -147.5;
altkmrange = [100,1000,10];

iono = iri2016(time, glat, glon,  altkmrange);

assert(abs(iono.Ne(11) - 3.986688e9) < 1e5, 'Ne error excessive')

if isoctave
  disp('OK: IRI2016 GNU Octave')
else
  disp('OK: IRI2016 Matlab')
end

%% build
srcdir = fullfile(cwd, '/../src/iri2016');
build(srcdir)
name = 'iri2016_driver';
if ispc
  name = [name, '.exe'];
end
assert(is_file(fullfile(srcdir, name)))
