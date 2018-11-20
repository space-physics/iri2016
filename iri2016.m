function iri2016()
%% IRI2016 model from Matlab.
% https://www.scivision.co/matlab-python-user-module-import/
assert(~verLessThan('matlab', '9.5'), 'Matlab >= R2018b required')

% geographic WGS84 lat,lon,alt
glat = 65.1;
glon = -147.5;
alt_km = 100:10:1000;
t = '2015-12-13T10';


iono = py.iri2016.IRI(t, alt_km, glat, glon);

plotiono(iono)
end

function plotiono(iono)

NmF2 = xarray2mat(iono{'NmF2'});
hmF2 = xarray2mat(iono{'hmF2'});

disp(['NmF2 ',num2str(NmF2),' m^-3'])
disp(['hmF2 ',num2str(hmF2), ' km'])

alt_km = xarrayind2vector(iono, 'alt_km');
times = char(iono.attrs{'time'}.isoformat());
glat = iono.attrs{'glat'};
glon = iono.attrs{'glon'};

%% Density profiles
Ne = xarray2mat(iono{'ne'});
NOp = xarray2mat(iono{'nO+'});
NHp = xarray2mat(iono{'nH+'});
NHep = xarray2mat(iono{'nHe+'});
NO2p = xarray2mat(iono{'nO2+'});
NNOp = xarray2mat(iono{'nNO+'});

figure(1), clf(1)
sgtitle({[times,' deg.  (',num2str(glat),', ', num2str(glon),')']})

ax = subplot(1,2,1, 'parent', 1);
set(ax, 'nextplot','add')

semilogx(ax, Ne, alt_km, 'DisplayName', 'N_e')
semilogx(ax, NOp, alt_km, 'DisplayName', 'N_{O^+}')
semilogx(ax, NHp, alt_km, 'DisplayName', 'N_{H^+}')
semilogx(ax, NHep, alt_km, 'DisplayName', 'N_{He^+}')
semilogx(ax, NO2p, alt_km, 'DisplayName', 'N_{O_2^+}')
semilogx(ax, NNOp, alt_km, 'DisplayName', 'N_{NO^+}')

set(ax,'xscale','log')
title('Number Densities')
xlabel(ax, 'Density [m^-3]')
ylabel(ax, 'altitude [km]')
xlim(ax, [1e4,1e12])

grid(ax, 'on')
legend(ax, 'show')

%% Temperature Profiles

Tn = xarray2mat(iono{'Tn'});
Ti = xarray2mat(iono{'Ti'});
Te = xarray2mat(iono{'Te'});

ax = subplot(1,2,2, 'parent', 1);
set(ax, 'nextplot','add')

plot(ax, Tn, alt_km, 'DisplayName', 'T_n')
plot(ax, Ti, alt_km, 'DisplayName', 'T_i')
plot(ax, Te, alt_km, 'DisplayName', 'T_e')

title('Temperature')
xlabel(ax, 'Temperature [K]')
ylabel(ax, 'altitude [km]')

grid(ax, 'on')
legend(ax, 'show')
  
end

function M = xarray2mat(V)
M = double(py.numpy.asfortranarray(V));
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