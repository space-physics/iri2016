function iono = iri2016(time,altKm,glat,glon,setSamplePlot)
%% IRI2016 model from Matlab.
% https://www.scivision.dev/matlab-python-user-module-import/
% geographic WGS84 lat,lon,alt
%
% Example:
% iri2016('2015-12-13T10:00', 100:10:1000, 65.1, -147.5)
%
assert(~verLessThan('matlab', '9.5'), 'Matlab >= R2018b required')

narginchk(4,5)
validateattributes(altKm, {'numeric'}, {'positive', 'vector'})
validateattributes(glat, {'numeric'}, {'scalar'})
validateattributes(glon, {'numeric'}, {'scalar'})
if nargin<5
    setSamplePlot = false;
end
validateattributes(setSamplePlot, {'logical'}, {'scalar'})

switch class(time)
    case {'datetime', 'double'}, time = datestr(time, 30);
end

iono = py.iri2016.IRI(time, altKm, glat, glon);
end