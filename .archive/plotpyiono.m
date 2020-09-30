function plotiono(iono, key)

alt_km = xarrayind2vector(iono, 'alt_km');
times = char(iono.attrs{'time'}.isoformat());
glat = iono.attrs{'glat'};
glon = iono.attrs{'glon'};

if nargin>1
    figure
    v = xarray2mat(iono{key});
    semilogx(v, alt_km, 'DisplayName', key)

    switch(key(1))
        case 'n', xlabel('Density [m^-3]')
        case 'T', xlabel('Temperature [K]')
    end
    ylabel('altitude [km]')
    title(key)

    return
end

NmF2 = xarray2mat(iono{'NmF2'});
hmF2 = xarray2mat(iono{'hmF2'});

disp(['NmF2 ',num2str(NmF2),' m^-3'])
disp(['hmF2 ',num2str(hmF2), ' km'])



%% Density profiles
Ne = xarray2mat(iono{'ne'});
NOp = xarray2mat(iono{'nO+'});
NHp = xarray2mat(iono{'nH+'});
NHep = xarray2mat(iono{'nHe+'});
NO2p = xarray2mat(iono{'nO2+'});
NNOp = xarray2mat(iono{'nNO+'});
NCI = xarray2mat(iono{'nCI'});
NNp = xarray2mat(iono{'nN+'});

hp = figure;
sgtitle(hp, {[times,' deg.  (',num2str(glat),', ', num2str(glon),')']})

ax = subplot(1,2,1, 'parent', hp);
set(ax, 'nextplot','add')

semilogx(ax, Ne, alt_km, 'DisplayName', 'N_e')
semilogx(ax, NOp, alt_km, 'DisplayName', 'N_{O^+}')
semilogx(ax, NHp, alt_km, 'DisplayName', 'N_{H^+}')
semilogx(ax, NHep, alt_km, 'DisplayName', 'N_{He^+}')
semilogx(ax, NO2p, alt_km, 'DisplayName', 'N_{O_2^+}')
semilogx(ax, NNOp, alt_km, 'DisplayName', 'N_{NO^+}')
semilogx(ax, NCI, alt_km, 'DisplayName', 'N_{CI}')
semilogx(ax, NNp, alt_km, 'DisplayName', 'N_{N^+}')

title(ax, 'Number Densities')
xlabel(ax, 'Density [m^-3]')
ylabel(ax, 'altitude [km]')
xlim(ax, [1e4,1e12])

set(ax,'xscale','log')
grid(ax, 'on')
legend(ax, 'show')

%% Temperature Profiles

Tn = xarray2mat(iono{'Tn'});
Ti = xarray2mat(iono{'Ti'});
Te = xarray2mat(iono{'Te'});

ax = subplot(1,2,2, 'parent', hp);
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
