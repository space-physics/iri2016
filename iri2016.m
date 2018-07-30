function iri2016()
% quick demo calling IRI2016 model from Matlab.
% https://www.scivision.co/matlab-python-user-module-import/

% geographic WGS84 lat,lon,alt
glat = 65.1;
glon = -147.5;
alt_km = 100:10:1000;
t = '2015-12-13T10';


dt = py.iri2016.IRI(t, alt_km, glat, glon);

Ne = xarray2mat(dt{'ne'});
NmF2 = xarray2mat(dt{'NmF2'});
hmF2 = xarray2mat(dt{'hmF2'});

plotiono(alt_km, Ne, t, glat, glon)
end

function plotiono(alt_km, Ne, t,glat,glon)
  figure(1), clf(1)
  ax = axes('nextplot','add');

  semilogx(ax, Ne, alt_km)
  
  set(ax,'xscale','log')
  title({[t,' deg.  (',num2str(glat),',', num2str(glon),')']})
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

C = cell(V{1}.indexes{key}.values.tolist);  % might be numeric or cell array of strings

if iscellstr(C) || any(class(C{1})=='py.str')
    I=cellfun(@char,C, 'uniformoutput',false);
else
    I = cell2mat();
end % if

end % function