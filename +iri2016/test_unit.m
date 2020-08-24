%% simple
time = datetime(2015,12,13,10,0,0);
glat = 65.1;
glon = -147.5;
altkmrange = [100,1000,10];

iono = iri2016.iri2016(time, glat, glon,  altkmrange);

assert(abs(iono.Ne(11) - 3.986688e9) < 1e5, 'Ne error excessive')
%% build
srcdir = fullfile(cwd, '/../src/iri2016');
iri2016.cmake(srcdir)
name = 'iri2016_driver';
if ispc
  name = [name, '.exe'];
end
assert(isfile(fullfile(srcdir, name)))
