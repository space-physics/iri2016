function iono = iri2016(time, glat, glon, altkmrange)

validateattributes(glat, {'numeric'}, {'scalar'})
validateattributes(glon, {'numeric'}, {'scalar'})
validateattributes(altkmrange, {'numeric'}, {'positive', 'vector','numel',3})
%% binary IRI2016
cwd = fileparts(mfilename('fullpath'));
exe = [cwd,filesep,'..', filesep, 'build', filesep, 'iri2016_driver'];
if ispc, exe = [exe,'.exe']; end
if ~exist(exe,'file'), error('compile IRI2016 via setup_iri2016.m'), end

t = num2str(datevec(time));

cmd = [exe, ' ', t,...
       ' ',num2str(glat), ' ', num2str(glon), ' ', num2str(altkmrange)];
[status,dat] = system(cmd);
if status ~= 0, error(dat), end

Nalt =  fix((altkmrange(2) - altkmrange(1)) / altkmrange(3)) + 1;

arr = cell2mat(textscan(dat, '%f %f %f %f %f %f %f %f %f %f %f %f', Nalt, 'ReturnOnError', false));

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

arr(arr<=0) = nan;

iono.NmF2=arr(1);
iono.hmF2=arr(2);
iono.NmF1=arr(3);
iono.hmF1=arr(4);
iono.NmE=arr(5);
iono.hmE=arr(6);
iono.TECtotal=arr(37);

end
