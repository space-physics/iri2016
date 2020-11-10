function iono = iri2016(time, glat, glon, altkm_range)
arguments
  time (1,1) datetime
  glat (1,1) {mustBeNumeric,mustBeFinite}
  glon (1,1) {mustBeNumeric,mustBeFinite}
  altkm_range (1,3) {mustBeNumeric,mustBeFinite,mustBePositive}
end
%% binary IRI2016
cwd = fileparts(mfilename('fullpath'));
srcdir = fullfile(cwd, "../src/iri2016");
exe = fullfile(srcdir, "iri2016_driver");
if ispc
  exe = exe + ".exe";
end
if ~isfile(exe)
  cmake(srcdir)
end
assert(isfile(exe), 'could not build or find iri2016 executable: %s', exe)

datadir = fullfile(cwd, "../src/iri2016/data");

t_str = datestr(time, 'yyyy mm dd HH MM SS');

cmd = sprintf("%s %s %f %f ", exe, t_str, glat, glon) + ...
       num2str(altkm_range) + " " + datadir;
[status, dat] = system(cmd);
assert(status == 0, dat)

Nalt = fix((altkm_range(2) - altkm_range(1)) / altkm_range(3)) + 1;

arr = cell2mat(textscan(dat, '%f %f %f %f %f %f %f %f %f %f %f %f', Nalt, ...
  'CollectOutput', true, 'ReturnOnError', false));

iono.altkm = arr(:,1);
iono.Ne = arr(:,2);
iono.Tn = arr(:,3);
iono.Ti = arr(:,4);
iono.Te = arr(:,5);
iono.nO = arr(:,6);
iono.nH = arr(:,7);
iono.nHe = arr(:,8);
iono.nO2 = arr(:,9);
iono.nNO = arr(:,10);
iono.nCI = arr(:,11);
iono.nN = arr(:,12);

arr = cell2mat(textscan(dat, '%f', 'HeaderLines',Nalt));

% by convention of msis
arr(arr <= 0) = nan;

iono.NmF2=arr(1);
iono.hmF2=arr(2);
iono.NmF1=arr(3);
iono.hmF1=arr(4);
iono.NmE=arr(5);
iono.hmE=arr(6);
iono.TECtotal=arr(37);

end
