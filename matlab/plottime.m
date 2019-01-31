function plottime(iri, t, glat, glon)
  
  validateattributes(iri, {'struct'}, {'vector'})
  validateattributes(t, {'numeric'}, {'vector'})
  validateattributes(glat, {'numeric'}, {'scalar'})
  validateattributes(glon, {'numeric'}, {'scalar'})
  
ttxt = [datestr(t(1), 29), ' (',num2str(glat),',',num2str(glon),')'];

figure
%% max density
ax1 = subplot(2,1,1);
set(ax1,'nextplot','add')

semilogy(ax1,t, [iri.NmF2], 'DisplayName','N_mF_2')
semilogy(ax1,t, [iri.NmF1], 'DisplayName','N_mF_1')
semilogy(ax1,t, [iri.NmE], 'DisplayName','N_mE')

datetick(ax1,'x',13)
title(ax1,ttxt)
ylabel(ax1,'m^{-3}')

legend(ax1,'show','location','southwest')
%% height of max density
ax2 = subplot(2,1,2);
set(ax2,'nextplot','add')

semilogy(ax2,t, [iri.hmF2], 'DisplayName','h_mF_2')
semilogy(ax2,t, [iri.hmF1], 'DisplayName','h_mF_1')
semilogy(ax2,t, [iri.hmE], 'DisplayName','h_mE')

datetick(ax2,'x',13)
ylabel(ax2,'km')
xlabel(ax2,'time [UTC]')

legend(ax2,'show','location','southwest')

%% TEC
hf = figure;
ax = axes('nextplot','add');
semilogy(ax, t, [iri.TECtotal], 'DisplayName', 'total')
datetick(ax, 'x', 13)
ylabel(ax, 'TEC [TECu / m^{-2}]')
xlabel(ax, 'time [UTC]')
title(ax,ttxt)
end