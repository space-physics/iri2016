function plottime(iri, times, glat, glon)

figure(1); clf(1)
ax1 = subplot(2,1,1);
set(ax1,'nextplot','add')

semilogy(ax1,times, [iri.NmF2], 'DisplayName','N_mF_2')
semilogy(ax1,times, [iri.NmF1], 'DisplayName','N_mF_1')
semilogy(ax1,times, [iri.NmE], 'DisplayName','N_mE')

datetick(ax1,'x',13)
title(ax1,[datestr(times(1), 29), ' (',num2str(glat),',',num2str(glon),')'])
ylabel(ax1,'m^{-3}')

legend(ax1,'show','location','southwest')
%%
ax2 = subplot(2,1,2);
set(ax2,'nextplot','add')

semilogy(ax2,times, [iri.hmF2], 'DisplayName','h_mF_2')
semilogy(ax2,times, [iri.hmF1], 'DisplayName','h_mF_1')
semilogy(ax2,times, [iri.hmE], 'DisplayName','h_mE')

datetick(ax2,'x',13)
ylabel(ax2,'km')
xlabel(ax2,'time [UTC]')

legend(ax2,'show','location','southwest')

end