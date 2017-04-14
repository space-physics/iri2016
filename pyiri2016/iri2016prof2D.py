
from pyigrf.pyigrf import GetIGRF
from pyiri2016 import IRI2016
from pyiri2016 import IRI2016Profile
from pyiri2016.iriweb import irisubgl, firisubl
from numpy import arange, array, ceil, empty, floor, isnan, linspace, \
    log10, meshgrid, nan, tile, transpose, where
from numpy.ma import masked_where
from matplotlib.pyplot import clf, close, cm, colorbar, figure, savefig, show
from mpl_toolkits.basemap import Basemap
from os.path import dirname, isdir, join, realpath
from os import mkdir
import pyapex, seaborn
from scipy.interpolate import interp2d, RectBivariateSpline
from timeutil.timeutil import TimeUtilities


CurrFolder = dirname(realpath(__file__))
DataFolder = join(CurrFolder, 'data')


class IRI2016_2DProf(IRI2016Profile):

    #def __init__(self):

    #    pass

    #def _GetTitle(self):

    #    IRI2016Profile()._GetTitle(__self__)


    def HeightVsTime(self, FIRI=False, hrlim=[0., 24.], hrstp=1.):

        self.option = 1
        nhrstp = int((hrlim[1] + hrstp - hrlim[0]) / hrstp) + 1
        hrbins = list(map(lambda x: hrlim[0] + float(x) * hrstp, range(nhrstp)))

        Ne = empty((nhrstp, self.numstp))
        if FIRI: NeFIRI = empty((nhrstp, self.numstp))
        Te = empty((nhrstp, self.numstp))
        Ti = empty((nhrstp, self.numstp))

        for i in range(nhrstp):
            self.hour = hrbins[i]
            self.HeiProfile()

            Ne[i, :] = self.a[0, range(self.numstp)]
            if FIRI: NeFIRI[i, :] = self.a[12, range(self.numstp)]
            Te[i, :] = self.a[3, range(self.numstp)]
            Ti[i, :] = self.a[2, range(self.numstp)]

     #   self._GetTitle()

        altbins = arange(self.vbeg, self.vend + self.vstp, self.vstp)
        self.data2D = {'alt' : altbins, 'hour' : hrbins, \
                    'Ne' : Ne, 'Te' : Te, 'Ti' : Ti, \
                    'title1' : self.title1, 'title2' : self.title2}
        if FIRI:
            self.FIRI2D = {'alt' : altbins, 'hour' : hrbins, \
                'Ne' : NeFIRI, \
                'title1' : self.title1, 'title2' : self.title2}

    #
    # End of 'HeightVsTime'
    #####


    def LatVsLon(self, lonlim=[-180., 180.], lonstp=20.):

        self.option = 2
        nlonstp = int((lonlim[1] + lonstp - lonlim[0]) / lonstp) + 1
        lonbins = list(map(lambda x: lonlim[0] + float(x) * lonstp, range(nlonstp)))

        NmF2 = empty((nlonstp, self.numstp))
        hmF2 = empty((nlonstp, self.numstp))
        B0 = empty((nlonstp, self.numstp))
        dip = empty((nlonstp, self.numstp))

        for i in range(nlonstp):
            self.lon = lonbins[i]
            self.HeiProfile()
            NmF2[i, :] = self.b[0, range(self.numstp)]
            hmF2[i, :] = self.b[1, range(self.numstp)]
            B0[i, :] = self.b[9, range(self.numstp)]
            dip[i, :] = self.b[24, range(self.numstp)]


        latbins = arange(self.vbeg, self.vend + self.vstp, self.vstp)
        self.data2D = {'lat' : latbins, 'lon' : lonbins, \
                    'NmF2' : NmF2, 'hmF2' : hmF2, 'B0' : B0, 'dip' : dip, \
                    'title' : self.title3}
            

    #
    # End of 'LatVsLon'
    #####


    def LatVsFL(self, date=[2003, 11, 21], FIRI=False, IGRF=False, time=[23, 15, 0], \
        gc=[-77.76, -11.95], \
        hlim=[80., 200.], hstp=1., mlatlim=[-10., 10.], mlatstp=.1):

        #
        # INPUTS
        #

        # Date
        year, month, day = date

        # Time
        hour, minute, second = time

        # Geog. Coord.
        dlon, dlat = gc

        # hlim -> Height range at equator, in km
        # hstp -> height resolution at equator, in km
        # mlatlim -> Geom. latitude range, in degrees
        # mlatstp -> Geom. latitude resolution, in degrees

        #
        ###

        doy = TimeUtilities().CalcDOY(year, month, day)
        date2 = year + doy / (365 + 1 if TimeUtilities().IsLeapYear else 0)


        # f = figure(figsize=(16,6))

        # pn = f.add_subplot(111)

        self.coordl, self.qdcoordl = [], []

        for h in arange(hlim[0], hlim[1] + hstp, hstp):

            gc, qc = pyapex.ApexFL().getFL(date=date2, dlon=dlon, dlat=dlat, \
                hateq=h, mlatRange=mlatlim, mlatSTP=mlatstp)

            # x, y, z = gc['lat'], gc['alt'], gc['lon']

            # ind = where(y < hlim[0])
            # if len(ind) > 0: x[ind], y[ind], z[ind] = nan, nan, nan
            # pn.plot(x, y)

            self.coordl.append([gc['lon'], gc['alt'], gc['lat']])
            self.qdcoordl.append([qc['lon'], gc['alt'], qc['lat']])

        # pn.invert_xaxis()
        # show()

        jf = IRI2016().Switches()
        jmag = 0
        mmdd = int(month * 100) + day
        hour2 = hour + minute / 60 + second / 3600

        self.coordl = array(self.coordl)
        self.qdcoordl = array(self.qdcoordl)

        # nfl -> No. of field-line (or height)
        # nc -> No. of coord. (0 -> lon, 1 -> alt, 2 -> lat)
        # np -> No. of points per field-line
        nfl, nc, np = self.coordl.shape

        self.ne, self.te = tile(nan, (np, nfl)), tile(nan, (np, nfl))
        self.ti, self.tn = tile(nan, (np, nfl)), tile(nan, (np, nfl))
        self.nHe, self.nO = tile(nan, (np, nfl)), tile(nan, (np, nfl))
        self.nN2, self.nO2 = tile(nan, (np, nfl)), tile(nan, (np, nfl))
        self.nAr, self.nH = tile(nan, (np, nfl)), tile(nan, (np, nfl))
        self.nN, self.babs = tile(nan, (np, nfl)), tile(nan, (np, nfl))
        if FIRI: self.neFIRI = tile(nan, (np, nfl))

        for fl in range(nfl):

            curr_coordl = transpose(self.coordl[fl, :, :])

            ind = where(curr_coordl[:, 1] >= (hlim[0] - 10.))

            if len(ind[0]) > 0:

                outf, oarr = irisubgl(jf, jmag, year, mmdd, hour2, \
                    curr_coordl[ind[0], :], DataFolder)

                self.ne[ind[0], fl] = outf[0, :]

                self.tn[ind[0], fl] = outf[1, :]
                self.ti[ind[0], fl] = outf[2, :]
                self.te[ind[0], fl] = outf[3, :]

                if FIRI: self.neFIRI[ind[0], fl], ierr = firisubl(year, doy, hour2, \
                    curr_coordl[ind[0], :], DataFolder)

                self.nHe[ind[0], fl] = outf[20, :]
                self.nO[ind[0], fl] = outf[21, :]
                self.nN2[ind[0], fl] = outf[22, :]
                self.nO2[ind[0], fl] = outf[23, :]
                self.nAr[ind[0], fl] = outf[24, :]
                self.nH[ind[0], fl] = outf[26, :]
                self.nN[ind[0], fl] = outf[27, :]

                self.babs[ind[0], fl] = list(self.getIGRF(curr_coordl[ind[0], :], date2)) \
                    if IGRF else outf[19, :]

        self.hlim = hlim

        self.date, self.time = date, time
        self.f107cm = oarr[40, 0]
        self.ap, self.Ap = oarr[50, 0], oarr[51, 0]

    #
    # End of 'LatVsFL'
    #####


    def _Get_Title(self):

        dateStr = 'DATE: {:4d}/{:02d}/{:02d}'.format(self.date[0], self.date[1], self.date[2])
        timeStr = 'TIME: {:02d}:{:02d} UT'.format(self.time[0], self.time[1])
        f107Str = 'F107: {:6.2f}'.format(self.f107cm)
        apStr = 'ap: {:3d}'.format(int(self.ap))
        ApStr = 'Ap: {:3d}'.format(int(self.Ap))
        gmlon = self.qdcoordl[0, 0, 0]
        gmlonStr = '{:7.2f} {:s}'.format(abs(gmlon), 'E' if gmlon > 0. else 'W')

        self._title1 = '{:s} - {:s}  -  MAG. LON.:{:s}'.format(dateStr, timeStr, gmlonStr)
        self._title2 = '{:s} - {:s}'.format(f107Str, ApStr)

    #
    # End of '_GetTitle'
    ######


    def getIGRF(self, coordl, year):

        for lon, alt, lat in coordl:

            bn, be, bd, xl, icode = GetIGRF(lat, lon, alt, year)

            # Horizontal component
            bh = (bn**2 + be**2)**.5

            yield bh


    def PlotLatVsFL(self):

        self._Get_Title()
        
        nrow, ncol = 2, 2

        spID = nrow * 100 + ncol * 10

        counter = 0

        X, Y = transpose(self.coordl[:, 2, :]), transpose(self.coordl[:, 1, :])

        f = figure(figsize=(16, 6))

        for ir in range(nrow):

            for ic in range(ncol):

                pn = f.add_subplot(spID + (counter + 1))

                if counter == 0:
                    Z = log10(self.ne)
                    vmin, vmax, nc = 8, 12, 32+1
                    zlabel = 'Log$_{10}$N$_e$(m$^{-3}$)'
                elif counter == 1:
                    Z = log10(self.nHe)
                    vmin, vmax, nc = 5, 9, 32+1
                    zlabel = 'Log$_{10}$H$_e$(m$^{-3}$)'
                elif counter == 2:
                    Z = self.te
                    vmin, vmax, nc = 100, 1200, 36+1
                    zlabel = 'T$_e$($^\circ$)'
                elif counter == 3:
                    Z = self.tn
                    vmin, vmax, nc = 100, 1200, 36+1
                    zlabel = 'T$_n$($^\circ$)'

                Z_masked = masked_where(isnan(Z), Z)

                C = linspace(vmin, vmax, nc, endpoint=True)
                ipc = pn.contourf(X, Y, Z_masked, C, cmap=cm.jet, extent='both', origin='lower')

                if counter == 0: pn.set_title(self._title1)

                if counter == 1: pn.set_title(self._title2)

                if counter > 1: pn.set_xlabel('Geog. Lat. ($^\circ$)')

                pn.set_ylabel('Altitude (km)')
                pn.set_ylim(self.hlim)
                pn.invert_xaxis()
                pn.grid()
                
                cp = colorbar(ipc)
                cp.set_label(zlabel)

                counter += 1

        show()

    #
    # End of 'PlotLatVsFL' 
    #####

    def PlotLatVsFLFIRI(self, save=False, verbose=False):

        self._Get_Title()
        
        nrow, ncol = 1, 1

        spID = nrow * 100 + ncol * 10

        counter = 0

        X, Y = transpose(self.coordl[:, 2, :]), transpose(self.coordl[:, 1, :])

        f = figure(figsize=(16, 6))

        for ir in range(nrow):

            for ic in range(ncol):

                pn = f.add_subplot(spID + (counter + 1))

                if counter == 0:
                    Z = log10(self.neFIRI)
                    vmin, vmax, nc = 9, 12, 24+1
                    zlabel = 'Log$_{10}$N$_e$(m$^{-3}$)'

                #Z_masked = masked_where(isnan(Z), Z)
                Z[where(Z < vmin)] = vmin

                C = linspace(vmin, vmax, nc, endpoint=True)
                ipc = pn.contourf(X, Y, Z, C, cmap=cm.jet, extent='both', origin='lower')

                if counter == 0: pn.set_title(self._title1)
                #if counter == 1: pn.set_title(self._title2)
                pn.set_xlabel('Geog. Lat. ($^\circ$)')
                pn.set_ylabel('Altitude (km)')
                pn.set_ylim(self.hlim)
                pn.invert_xaxis()
                pn.grid()
                
                cp = colorbar(ipc)
                cp.set_label(zlabel)

                counter += 1
        
        if not save:
            show()
        else:
            gpath = '../figures/' + '{:04d}{:02d}{:02d}/'.format(self.year, self.month, self.dom)
            if not isdir(gpath): mkdir(gpath)
            self.figname = gpath + 'firi-{:02d}{:02d}.jpg'.format(self.time[0], self.time[1])
            if verbose: print('Saving at: {:s}'.format(self.figname))
            savefig(self.figname, bbox_inches='tight', format='jpg', dpi=100)
            

        clf()
        close()

    #
    # End of 'PlotLatVsFL' 
    #####

    def Plot2D(self):

        f = figure(figsize=(24, 6))

        if self.option == 1:

            pn = f.add_subplot(131)
            X, Y = meshgrid(self.data2D['hour'], self.data2D['alt'])
            ipc = pn.pcolor(X, Y, transpose(log10(self.data2D['Ne'])), cmap=cm.jet, vmax=13, vmin=9)
            pn.set_title(self.data2D['title1'])
            pn.set_xlabel('Hour (UT)')
            pn.set_ylabel('Altitude (km)')
            cp1 = colorbar(ipc)
            cp1.set_label('Log$_{10}$N$_e$(m$^{-3}$)')

            pn = f.add_subplot(132)
            ipc = pn.pcolor(X, Y, transpose(self.data2D['Te']), cmap=cm.jet, vmax=4000, vmin=100)
            pn.set_title(self.data2D['title2'])
            pn.set_xlabel('Hour (UT)')
            pn.set_ylabel('Altitude (km)')
            cp1 = colorbar(ipc)
            cp1.set_label('T$_e$ ($^\circ$)')

            pn = f.add_subplot(133)
            ipc = pn.pcolor(X, Y, transpose(self.data2D['Ti']), cmap=cm.jet, vmax=4000, vmin=100)
            pn.set_xlabel('Hour (UT)')
            pn.set_ylabel('Altitude (km)')
            cp1 = colorbar(ipc)
            cp1.set_label('T$_i$ ($^\circ$)')


        elif self.option == 2:

            pn1 = f.add_subplot(111)

            m = Basemap(llcrnrlon=self.data2D['lon'][0], llcrnrlat=self.data2D['lat'][0], \
                        urcrnrlon=self.data2D['lon'][-1], urcrnrlat=self.data2D['lat'][-1], \
                        resolution='l')
            m.drawcoastlines()

            parallelsLim = self._RoundLim([self.data2D['lat'][0], self.data2D['lat'][-1]])
            m.drawparallels(arange(parallelsLim[0], parallelsLim[1], 20.), \
            labels=[True, False, False, True])

            meridiansLim = self._RoundLim([self.data2D['lon'][0], self.data2D['lon'][-1]])
            m.drawmeridians(arange(meridiansLim[0], meridiansLim[1], 30.), \
            labels=[True, False, False, True])

            X, Y = meshgrid(self.data2D['lon'], self.data2D['lat'])
            ipc = m.pcolor(X, Y, transpose(9.*self.data2D['NmF2']**.5 * 1e-6), \
            cmap=cm.jet, vmax=15., vmin=0)
            m.contour(X, Y, transpose(self.data2D['dip']), colors='k', linestyles='--')
            pn1.set_title(self.data2D['title'])

            cp1 = m.colorbar(ipc)
            cp1.set_label('foF2 (MHz)')

        elif self.option == 8:
            pass

        if True: show()
        elif False:
            gpath = '../figures/' + '{:04d}{:02d}{:02d}/'.format(self.year, self.month, self.dom)
            if not isdir(gpath): mkdir(gpath)
            figname = gpath + 'iri-{:02d}{:02d}.jpg'.format(self.HH, self.MM)
            savefig(figname, bbox_inches='tight', format='jpg', dpi=100)
            # convert -resize 50% -delay 20 -loop 0 *.jpg myimage.gif

    #
    # End of 'Plot2D'
    #####

    def PlotFIRI2D(self):

        f = figure(figsize=(8,6))

        pn = f.add_subplot(111)

        if self.option == 1:

            X, Y = meshgrid(self.FIRI2D['hour'], self.FIRI2D['alt'])

            #ipc = pn.pcolor(X, Y, transpose(log10(self.FIRI2D['Ne'])), cmap=cm.jet, 
            #vmax=12, vmin=9)

            Z = self.FIRI2D['Ne']
            Z[where(Z < 10**9)] = 10**9
            Z = transpose(log10(Z))

            C = linspace(9, 12, 24+1, endpoint=True)
            ipc = pn.contourf(X, Y, Z, C, \
                cmap=cm.jet, extent='both', origin='lower')
            pn.grid()
            pn.set_title(self.FIRI2D['title1'])
            pn.set_xlabel('Hour (UT)')
            pn.set_ylabel('Altitude (km)')

        elif self.option == 2:

            pass

        cp = colorbar(ipc)
        cp.set_label('Log$_{10}$N$_e$(m$^{-3}$)')

        if True: show()
        elif False:
            pass

    #
    # End of 'PlotFIRI2D' 
    #####

    def _RoundLim(self, lim):

        return list(map(lambda x: x * 10., [floor(lim[0] / 10.), ceil(lim[1] / 10.)]))


    def Plot2DMUF(self):

        f = figure(figsize=(16, 12))

        f.add_subplot(231)
        self.MapPColor(9.*self.data2D['NmF2']**.5 * 1e-6, 15., 5.)

        f.add_subplot(234)
        self.IntLatVsLon()
        self.MapPColorInt(self.data2DInt['foF2'], 15., 5.)

        f.add_subplot(232)
        self.MapPColor(self.data2D['hmF2'], 550., 250.)

        f.add_subplot(235)
        self.MapPColorInt(self.data2DInt['hmF2'], 550., 250.)

        f.add_subplot(233)
        self.MapPColor(self.data2D['B0'], 250., 100.)

        f.add_subplot(236)
        self.MapPColorInt(self.data2DInt['B0'], 250., 100.)

        show()


    def MapPColor(self, arr, vmax, vmin):

        self.m = Basemap(llcrnrlon=self.data2D['lon'][0], llcrnrlat=self.data2D['lat'][0], \
                    urcrnrlon=self.data2D['lon'][-1], urcrnrlat=self.data2D['lat'][-1], \
                    resolution='l')
        self.m.drawcoastlines()
        self.m.drawcountries()

        parallelsLim = self._RoundLim([self.data2D['lat'][0], self.data2D['lat'][-1]])
        self.m.drawparallels(arange(parallelsLim[0], parallelsLim[1], 2.), \
            labels=[True, False, False, True])

        meridiansLim = self._RoundLim([self.data2D['lon'][0], self.data2D['lon'][-1]])
        self.m.drawmeridians(arange(meridiansLim[0], meridiansLim[1], 5.), \
            labels=[True, False, False, True])

        X, Y = meshgrid(self.data2D['lon'], self.data2D['lat'])
        ipc = self.m.pcolor(X, Y, transpose(arr), cmap=cm.jet, vmax=vmax, vmin=vmin)
        self.m.contour(X, Y, transpose(self.data2D['dip']), colors='k', linestyles='--')

        #self.m.plot(X, Y, color='k', linestyle='None', marker='o')

        #lon0, lat0 = -11.95, -76.87
        #x0, y0 = meshgrid(lon0, lat0)
        #self.m.plot(x0, y0, color='k', linestyle='None', marker='o')
        
        #print(x0, y0)

#------------------------------------------------------------------------------

    def IntLatVsLon(self, lat0=-11.95, lon0=-76.87):

        #self.m.plot(lon0, lat0, 'bx')

        X0, Y0 = meshgrid(self.data2D['lon'], self.data2D['lat'])

        lon1 = lon0 + (array(self.data2D['lon']) - lon0) * .5
        lat1 = lat0 + (array(self.data2D['lat']) - lat0) * .5

        x0, y0 = array(self.data2D['lon']), array(self.data2D['lat'])        

        foF2 = interp2d(x0, y0, 9.*transpose(self.data2D['NmF2'])**.5*1e-6)(lon1, lat1)
        hmF2 = interp2d(x0, y0, transpose(self.data2D['hmF2']))(lon1, lat1)
        B0 = interp2d(x0, y0, transpose(self.data2D['B0']))(lon1, lat1)

        self.data2DInt = {'lon' : lon1, 'lat' : lat1, \
                        'foF2' : transpose(foF2), 'hmF2' : transpose(hmF2), 'B0' : transpose(B0)}

        self.data2DTX = {}
        self.data2DTX['foF2'] = interp2d(x0, y0, 9.*transpose(self.data2D['NmF2'])**.5*1e-6)(lon0, lat0)[0]
        
    #
    # End of 'IntLatVsLon'    
    #####


    def MapPColorInt(self, arr, vmax, vmin):

        self.m = Basemap(llcrnrlon=self.data2D['lon'][0], llcrnrlat=self.data2D['lat'][0], \
                    urcrnrlon=self.data2D['lon'][-1], urcrnrlat=self.data2D['lat'][-1], \
                    resolution='l')
        self.m.drawcoastlines()
        self.m.drawcountries()

        parallelsLim = self._RoundLim([self.data2D['lat'][0], self.data2D['lat'][-1]])
        self.m.drawparallels(arange(parallelsLim[0], parallelsLim[1], 2.), labels=[True,False,False,True])

        meridiansLim = self._RoundLim([self.data2D['lon'][0], self.data2D['lon'][-1]])        
        self.m.drawmeridians(arange(meridiansLim[0], meridiansLim[1], 5.), labels=[True,False,False,True])            
        
        X, Y = meshgrid(self.data2DInt['lon'], self.data2DInt['lat'])                    
        ipc = self.m.pcolor(X, Y, transpose(arr), cmap=cm.jet, vmax=vmax, vmin=vmin)

        X0, Y0 = meshgrid(self.data2D['lon'],self.data2D['lat'])
        self.m.contour(X0, Y0, transpose(self.data2D['dip']), colors='k', linestyles='--')
        #print(X.shape, Y.shape, arr.shape)

