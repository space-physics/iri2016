if __name__ == '__main__':

    from matplotlib.pyplot import figure, legend, show
    from pyiri2016.iri2016prof import IRI2016Profile
    from pyiri2016.iri2016 import IRI2016
    from scipy import arange
    import seaborn

    def example08():

        """ Geog. Latitude Profile Example """

        hrlim = [0, 24]
        hrstp = 0.25
        iri2016Obj = IRI2016Profile(hrlim=hrlim, hrstp=hrstp, lat=-11.95, \
        lon=-76.77, option=8, verbose=False, year=2004)

        hrbins = arange(hrlim[0], hrlim[1] + hrstp, hrstp)

        nhr = len(hrbins)
        index = range(nhr)

        fig = figure(figsize=(8,12))

        pn = fig.add_subplot(211)
        NmF2 = iri2016Obj.b[0, index]
        NmF1 = IRI2016()._RmNeg(iri2016Obj.b[2, index])
        NmE = iri2016Obj.b[4, index]
        pn.plot(hrbins, NmF2, label='N$_m$F$_2$')
        pn.plot(hrbins, NmF1, label='N$_m$F$_1$')
        pn.plot(hrbins, NmE, label='N$_m$E')
        pn.set_title(iri2016Obj.title1)
        pn.set_xlim(hrbins[[0, -1]])
        pn.set_xlabel('Hour (UT)')
        pn.set_ylabel('(m$^{-3}$)')        
        pn.set_yscale('log')
        legend(loc='best')

        pn = fig.add_subplot(212)
        hmF2 = iri2016Obj.b[1, index]
        hmF1 = IRI2016()._RmNeg(iri2016Obj.b[3, index])
        hmE = iri2016Obj.b[5, index]
        pn.plot(hrbins, hmF2, label='h$_m$F$_2$')
        pn.plot(hrbins, hmF1, label='h$_m$F$_1$')
        pn.plot(hrbins, hmE, label='h$_m$E')
        pn.set_xlim(hrbins[[0, -1]])
        pn.set_title(iri2016Obj.title2)
        pn.set_xlabel('Hour (UT)')
        pn.set_ylabel('(km)')
        legend(loc='best')                

        show()


    example08()