function data = iri_2016(time,altKm,glat,glon,setSamplePlot)
%IRI_2016 Matlab-Python wrapper of IRI2016 by MHirsch
%   time,glat,glon are one value each, while altKm can be a 1D array.

% https://www.scivision.dev/matlab-python-user-module-import/
assert(~verLessThan('matlab', '9.5'), 'Matlab >= R2018b required')

if nargin<5
    setSamplePlot = false;
end

isoDateFormat = 'yyyy-mm-ddTHH:MM:SS';

t = datestr(time,isoDateFormat);
iono = py.iri2016.IRI(t, altKm, glat, glon);

data.Ne = pyarray2mat(iono{'ne'});
data.Tn = pyarray2mat(iono{'Tn'});
data.Ti = pyarray2mat(iono{'Ti'});
data.Te = pyarray2mat(iono{'Te'});

data.nOI = pyarray2mat(iono{'nO+'});
data.nO2I = pyarray2mat(iono{'nO2+'});
data.nHI = pyarray2mat(iono{'nH+'});
data.nHeI = pyarray2mat(iono{'nHe+'});
data.nNOI = pyarray2mat(iono{'nNO+'});

data.NmF2 = pyarray2mat(iono{'NmF2'});
data.hmF2 = pyarray2mat(iono{'hmF2'});
data.NmF1 = pyarray2mat(iono{'NmF1'});
data.hmF1 = pyarray2mat(iono{'hmF1'});
data.NmE = pyarray2mat(iono{'NmE'});
data.hmE = pyarray2mat(iono{'hmE'});

data.B0 = pyarray2mat(iono{'B0'});

data.coordinates.altKm = xarrayind2vector(iono, 'alt_km');
data.coordinates.lat = xarrayind2vector(iono, 'lat');
data.coordinates.lon = xarrayind2vector(iono, 'lon');

data.attribute.f107 = str2double(char(iono.attrs{'f107'}));
data.attribute.ap = str2double(char(iono.attrs{'ap'}));
data.attribute.time = datenum(char(iono.attrs{'time'}.isoformat()),isoDateFormat);

if setSamplePlot
    plot_iono(data);
end

end

function plot_iono(data)

p = create_panels(figure,'totalPanelNo',2,'panelHeight',60,...
    'panelBreadth',60,'demargin',10,'marginleft',15,'marginright',15);
q = p(1);

q(1).select();
semilogx(data.Ne, data.coordinates.altKm)
set(gca,'xscale','log')
title({[datestr(data.attribute.time),' deg.  (',num2str(data.coordinates.lat),', ', num2str(data.coordinates.lon),')']})
xlabel('Density [m^-3]')
ylabel('altitude [km]')
grid('on')


q(2).select();
semilogx(data.nOI, data.coordinates.altKm)
hold on;
semilogx(data.nO2I, data.coordinates.altKm)
hold on;
semilogx(data.nNOI, data.coordinates.altKm)
hold on;
semilogx(data.nHI, data.coordinates.altKm)
hold on;
semilogx(data.nHeI, data.coordinates.altKm)
set(gca,'xscale','log')
% title({[datestr(data.attribute.time),' deg.  (',num2str(data.coordinates.lat),', ', num2str(data.coordinates.lon),')']})
legend('nO+','nO2+','nNO+','nH+','nHe+');
xlabel('Density [m^-3]')
ylabel('altitude [km]')
grid('on')

end


function M = pyarray2mat(V)
M = double(py.array.array('d',py.numpy.nditer(py.numpy.asfortranarray(V))));
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

end