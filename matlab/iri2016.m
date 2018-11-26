function iono = iri2016(time, glat, glon, altkmrange)

narginchk(4,4)
validateattributes(glat, {'numeric'}, {'scalar'})
validateattributes(glon, {'numeric'}, {'scalar'})
validateattributes(altkmrange, {'numeric'}, {'positive', 'vector','numel',3})
%% binary IRI2016
exe = ['..', filesep, 'bin', filesep, 'iri2016_driver'];
if ispc, exe = [exe,'.exe']; end
if ~exist(exe,'file'), error('must compile IRI2016 as per README.md'), end

t = num2str(datevec(time));

cmd = [exe, ' ', t,...
       ' ',num2str(glat), ' ', num2str(glon), ' ', num2str(altkmrange)];
[status,dat] = system(cmd);
if status ~= 0, error(dat), end

arr = sscanf(dat, '%f', [12,Inf]);

%{
C               OUTF(1,*)  ELECTRON DENSITY/M-3
C               OUTF(2,*)  NEUTRAL TEMPERATURE/K
C               OUTF(3,*)  ION TEMPERATURE/K
C               OUTF(4,*)  ELECTRON TEMPERATURE/K
C               OUTF(5,*)  O+ ION DENSITY/% or /M-3 if jf(22)=f 
C               OUTF(6,*)  H+ ION DENSITY/% or /M-3 if jf(22)=f
C               OUTF(7,*)  HE+ ION DENSITY/% or /M-3 if jf(22)=f
C               OUTF(8,*)  O2+ ION DENSITY/% or /M-3 if jf(22)=f
C               OUTF(9,*)  NO+ ION DENSITY/% or /M-3 if jf(22)=f
C                 AND, IF JF(6)=.FALSE.:
C               OUTF(10,*)  CLUSTER IONS DEN/% or /M-3 if jf(22)=f
C               OUTF(11,*)  N+ ION DENSITY/% or /M-3 if jf(22)=f
%}

iono.altkm = arr(1,:);
iono.Ne = arr(2,:);
iono.Tn = arr(3,:);
iono.Ti = arr(4,:);
iono.Te = arr(5,:);
iono.nO = arr(6,:);
iono.nH = arr(7,:);
iono.nHe = arr(8,:);
iono.nO2 = arr(9,:);
iono.nNO = arr(10,:);
iono.nCI = arr(11,:);
iono.nN = arr(12,:);

end
