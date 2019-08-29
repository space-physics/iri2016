function iri2016()
% quick demo calling IRI2016 model from Matlab.
% https://www.scivision.dev/matlab-python-user-module-import/

assert(~verLessThan('matlab', '8.4'), 'Matlab >= R2014b required')

% geographic WGS84 lat,lon,alt
glat = 65.1;
glon = -147.5;
alt_km = 100:10:1000;
t = '2015-12-13T10';


iono = py.iri2016.IRI(t, alt_km, glat, glon);

plotiono(iono)
end

function plotiono(iono)

Ne = xarray2mat(iono{'ne'});
NmF2 = xarray2mat(iono{'NmF2'});
hmF2 = xarray2mat(iono{'hmF2'});

alt_km = xarrayind2vector(iono, 'alt_km');
times = char(iono.attrs{'time'}.isoformat());
glat = iono.attrs{'glat'};
glon = iono.attrs{'glon'};

figure(1), clf(1)
ax = axes('nextplot','add');

semilogx(ax, Ne, alt_km)

set(ax,'xscale','log')
title({[times,' deg.  (',num2str(glat),', ', num2str(glon),')']})
xlabel('Density [m^-3]')
ylabel('altitude [km]')

grid('on')

end

function V = xarray2mat(V)
  % convert xarray 2-D array to Matlab matrix


V= V.values;
S = V.shape;
V = cell2mat(cell(V.ravel('F').tolist()));
V = reshape(V,[int64(S{1}), int64(S{2})]);

end

function I = xarrayind2vector(V,key)

C = cell(V.indexes{key}.values.tolist);  % might be numeric or cell array of strings

if iscellstr(C) || isa(C{1}, 'py.str')
    I = cellfun(@char, C, 'uniformoutput', false);
elseif isa(C{1}, 'py.datetime.datetime')
    I = char(C{1}.isoformat());
else
    I = cell2mat(C);
end % if

end % function