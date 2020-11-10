function plottime(iri, times, glat, glon)
arguments
  iri struct
  times datetime
  glat (1,1) {mustBeNumeric,mustBeFinite}
  glon (1,1) {mustBeNumeric,mustBeFinite}
end

ttxt = datestr(times(1), 29) + " (" + num2str(glat) + "," + num2str(glon) + ")";

fig = figure;
sgtitle(fig, ttxt)
%% max density
t = tiledlayout(fig, 2, 1);
ax1 = nexttile(t);
set(ax1,'nextplot','add')

semilogy(ax1,times, [iri.NmF2], 'DisplayName','N_mF_2')
semilogy(ax1,times, [iri.NmF1], 'DisplayName','N_mF_1')
semilogy(ax1,times, [iri.NmE], 'DisplayName','N_mE')

datetick(ax1,'x',13)

title(ax1, 'Density')
ylabel(ax1,'m^{-3}')

legend(ax1,'show','location','southwest')
%% height of max density
ax2 = nexttile(t);
set(ax2,'nextplot','add')

semilogy(ax2,times, [iri.hmF2], 'DisplayName','h_mF_2')
semilogy(ax2,times, [iri.hmF1], 'DisplayName','h_mF_1')
semilogy(ax2,times, [iri.hmE], 'DisplayName','h_mE')

ylabel(ax2,'km')
xlabel(ax2,'time [UTC]')
title(ax2, 'feature altitude')
legend(ax2,'show','location','southwest')

%% TEC
fig2 = figure;
ax = axes('nextplot','add', 'parent', fig2);

semilogy(ax, times, [iri.TECtotal], 'DisplayName', 'total')

ylabel(ax, 'TEC [TECu / m^{-2}]')
xlabel(ax, 'time [UTC]')
title(ax,ttxt)
end
