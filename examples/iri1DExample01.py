if __name__ == '__main__':

    from matplotlib.pyplot import figure, legend, show
    from pyiri2016.iri2016prof import IRI2016Profile
    from scipy import arange
    import seaborn

    def example01():

        """ Height Profile Example """

        altlim = [100., 1000.]
        altstp = 5.
        lat, lon = -11.95, -76.77
        year, month, dom = 2003, 11, 21

        iri2016Obj = IRI2016Profile(altlim=altlim, altstp=altstp, lat=lat, \
            lon=lon, year=year, month=month, dom=dom, option=1, verbose=False)

        altbins = arange(altlim[0], altlim[1] + altstp, altstp)

        nalt = len(altbins)
        index = range(nalt)

        fig = figure(figsize=(16,6))

        pn = fig.add_subplot(121)
        ne = iri2016Obj.a[0, index]
        pn.plot(ne, altbins, label='N$_e$')
        pn.set_title(iri2016Obj.title1)
        pn.set_xlabel('Density (m$^{-3}$)')
        pn.set_ylabel('Altitude (km)')
        pn.set_xscale('log')
        legend(loc='best')

        pn = fig.add_subplot(122)
        ti = iri2016Obj.a[2, index]
        te = iri2016Obj.a[3, index]
        pn.plot(ti, altbins, label='T$_i$')
        pn.plot(te, altbins, label='T$_e$')
        pn.set_title(iri2016Obj.title2)
        pn.set_xlabel('Temperature ($^\circ$)')
        pn.set_ylabel('Altitude (km)')        
        legend(loc='best')

        show()


    example01()