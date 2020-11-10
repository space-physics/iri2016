function plotiono(iono, times, glat, glon)
arguments
  iono struct
  times datetime
  glat (1,1) {mustBeNumeric,mustBeFinite}
  glon (1,1) {mustBeNumeric,mustBeFinite}
end
%% Density profiles
hp = figure;
sgtitle(hp, {datestr(times) + " deg.  (" + num2str(glat) + ", " + num2str(glon) + ")"})
t = tiledlayout(hp, 1,2);
ax = nexttile(t);
set(ax, 'nextplot','add')

semilogx(ax, iono.Ne, iono.altkm, 'DisplayName', 'N_e')
semilogx(ax, iono.nO, iono.altkm, 'DisplayName', 'N_{O^+}')
semilogx(ax, iono.nH, iono.altkm, 'DisplayName', 'N_{H^+}')
semilogx(ax, iono.nHe, iono.altkm, 'DisplayName', 'N_{He^+}')
semilogx(ax, iono.nO2, iono.altkm, 'DisplayName', 'N_{O_2^+}')
semilogx(ax, iono.nNO, iono.altkm, 'DisplayName', 'N_{NO^+}')
semilogx(ax, iono.nCI, iono.altkm, 'DisplayName', 'N_{CI}')
semilogx(ax, iono.nN, iono.altkm, 'DisplayName', 'N_{N^+}')

title(ax, 'Number Densities')
xlabel(ax, 'Density [m^-3]')
ylabel(ax, 'altitude [km]')
xlim(ax, [1e4,1e12])

set(ax,'xscale','log')
grid(ax, 'on')
legend(ax, 'show','location','northwest')

%% Temperature Profiles

ax = nexttile(t);
set(ax, 'nextplot','add')

plot(ax, iono.Tn, iono.altkm, 'DisplayName', 'T_n')
plot(ax, iono.Ti, iono.altkm, 'DisplayName', 'T_i')
plot(ax, iono.Te, iono.altkm, 'DisplayName', 'T_e')

title('Temperature')
xlabel(ax, 'Temperature [K]')
ylabel(ax, 'altitude [km]')

grid(ax, 'on')
legend(ax, 'show','location','northwest')

end
