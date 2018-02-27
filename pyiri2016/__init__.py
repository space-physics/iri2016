try:
    from pathlib import Path
    Path().expanduser()
except (ImportError,AttributeError):  # Python < 3.5
    from pathlib2 import Path
#%%
from datetime import datetime
from dateutil.parser import parse
from iri2016 import iriwebg
from numpy import arange, nan, ones, squeeze, where

class IRI2016(object):

    def __init__(self):
        self.iriDataFolder = Path(__file__).parent / 'data'


    def Switches(self):
        """
         IRI switches to turn on/off several options
        """

        jf = ones(50)

                        #    i          1                       0                 standard version
                        #    ------------------------------------------------------------------------
        jf[ 1 - 1] = 1; #    1    Ne computed            Ne not computed                     1
        jf[ 2 - 1] = 1; #    2    Te, Ti computed        Te, Ti not computed                 1
        jf[ 3 - 1] = 1; #    3    Ne & Ni computed       Ni not computed                     1
        jf[ 4 - 1] = 0; #    4    B0 - Table option      B0 - other models jf(31)            0
        jf[ 5 - 1] = 0; #    5    foF2 - CCIR            foF2 - URSI                         0
        jf[ 6 - 1] = 0; #    6    Ni - DS-95 & DY-85     Ni - RBV-10 & TTS-03                0
        jf[ 7 - 1] = 1; #    7    Ne - Tops: f10.7<188   f10.7 unlimited                     1
        jf[ 8 - 1] = 1; #    8    foF2 from model        foF2 or NmF2 - user input           1
        jf[ 9 - 1] = 1; #    9    hmF2 from model        hmF2 or M3000F2 - user input        1
        jf[10 - 1] = 1; #   10    Te - Standard          Te - Using Te/Ne correlation        1
        jf[11 - 1] = 1; #   11    Ne - Standard Profile  Ne - Lay-function formalism         1
        jf[12 - 1] = 1; #   12    Messages to unit 6     to meesages.text on unit 11         1
        jf[13 - 1] = 1; #   13    foF1 from model        foF1 or NmF1 - user input           1
        jf[14 - 1] = 1; #   14    hmF1 from model        hmF1 - user input (only Lay version)1
        jf[15 - 1] = 1; #   15    foE  from model        foE or NmE - user input             1
        jf[16 - 1] = 1; #   16    hmE  from model        hmE - user input                    1
        jf[17 - 1] = 1; #   17    Rz12 from file         Rz12 - user input                   1
        jf[18 - 1] = 1; #   18    IGRF dip, magbr, modip old FIELDG using POGO68/10 for 1973 1
        jf[19 - 1] = 1; #   19    F1 probability model   critical solar zenith angle (old)   1
        jf[20 - 1] = 1; #   20    standard F1            standard F1 plus L condition        1
        jf[21 - 1] = 1; #   21    ion drift computed     ion drift not computed              0
        jf[22 - 1] = 1; #   22    ion densities in %     ion densities in m-3                1
        jf[23 - 1] = 0; #   23    Te_tops (Aeros,ISIS)   Te_topside (TBT-2011)               0
        jf[24 - 1] = 0; #   24    D-region: IRI-95       Special: 3 D-region models (FIRI)   1
        jf[25 - 1] = 1; #   25    F107D from APF107.DAT  F107D user input (oarr(41))         1
        jf[26 - 1] = 0; #   26    foF2 storm model       no storm updating                   1
        jf[27 - 1] = 1; #   27    IG12 from file         IG12 - user                         1
        jf[28 - 1] = 0; #   28    spread-F probability   not computed                        0
        jf[29 - 1] = 0; #   29    IRI01-topside          new options as def. by JF(30)       0
        jf[30 - 1] = 0; #   30    IRI01-topside corr.    NeQuick topside model               0
                        # (29,30) = (1,1) IRIold, (0,1) IRIcor, (0,0) NeQuick, (1,0) Gulyaeva
        jf[31 - 1] = 1; #   31    B0,B1 ABT-2009         B0 Gulyaeva h0.5                    1
        jf[32 - 1] = 1; #   32    F10.7_81 from file     PF10.7_81 - user input (oarr(46))   1
        jf[33 - 1] = 0; #   33    Auroral boundary model on/off  true/false                  0
        jf[34 - 1] = 0; #   34    Messages on            Messages off                        1
        jf[35 - 1] = 0; #   35    foE storm model        no foE storm updating               0
                        #   ..    ....
                        #   50    ....
                        #   ------------------------------------------------------------------

        return jf

#%%

    def IRI(self, ap=5, f107=150, glat=0., glon=0., time=datetime.now(),
            ssn=150, var=1, vbeg=130.,   vend=130.+1., vstp=1.):

        time = parse(time)
#        doy = squeeze(TimeUtilities().CalcDOY(year, month, dom))

        # IRI options
        jf = self.Switches()

        # additional "input parameters" (necessary to scale the empirical model results
        # to measurements)
        addinp = -ones(12)

        #------------------------------------------------------------------------------
        #
        if time.year < 1958:

            addinp[10 - 1] = ssn  # RZ12  (This switches 'jf[17 - 1]' to '0' and
                                # uses correlation function to estimate IG12)

            jf[25 - 1] = 1        #   25    F107D from APF107.DAT  F107D user input (oarr(41))         1
            jf[27 - 1] = 1        #   27    IG12 from file         IG12 - user                         1
            jf[32 - 1] = 1        #   32    F10.7_81 from file     PF10.7_81 - user input (oarr(46))   1

        else:  # case for solar and geomagnetic indices from files

            jf[17 - 1] = 1        #   17    Rz12 from file         Rz12 - user input                   1
            jf[26 - 1] = 1        #   26    foF2 storm model       no storm updating                   1
            jf[35 - 1] = 1        #   35    foE storm model        no foE storm updating               0
         #
         #------------------------------------------------------------------------------

        mmdd = int(1e2 * time.month) + time.day               # month and dom (MMDD)

# %% more inputs
        jmag = 0            #  0: geographic; 1: geomagnetic
        iut = 0             #  0: for LT;     1: for UT
        height = 300.       #  in km
        h_tec_max = 2000    #  0: no TEC; otherwise: upper boundary for integral
        ivar = var          #  1: altitude; 2: latitude; 3: longitude; ...

        ivbeg = vbeg
        ivend = vend
        ivstp = vstp

        # Ionosphere (IRI)
        a, b = iriwebg(jmag, jf, glat, glon, int(time.year), mmdd, iut, time.hour,
            height, h_tec_max, ivar, ivbeg, ivend, ivstp, addinp, self.iriDataFolder)

        bins = arange(ivbeg, ivend + ivstp * 0., ivstp)
        a = a[:, arange(len(bins))]
        b = b[:, arange(len(bins))]

# %%
        # IRI Standard Ne (in m-3)
        neIRI = squeeze(self._RmZeros(self._RmNeg(a[0, :]))[0])

        # IRI Temperature (in K)
        teIRI = squeeze(a[4 - 1, :][0])
        tiIRI = squeeze(a[3 - 1, :][0])

        # FIRI Ne (in m-3)
        iri_ne_firi = squeeze(self._RmNeg(a[13 - 1, :])[0])

        ######### Ionic density (NO+, O2+, O+, H+, He+, N+, Cluster Ions)
        # Ionic density (O+, O2+, NO+)
        oplusIRI = squeeze(self._RmZeros(a[5 - 1, :])[0]) / 100. * neIRI       # in m-3
        o2plusIRI = squeeze(self._RmZeros(a[8 - 1, :])[0]) / 100. * neIRI      # in m-3
        noplusIRI = squeeze(self._RmZeros(a[9 - 1, :])[0]) / 100. * neIRI      # in m-3

        # more ionic densities (H+, He+, N+)
        hplusIRI = squeeze(self._RmZeros(a[6 - 1, :])[0]) / 100. * neIRI       # in m-3
        heplusIRI = squeeze(self._RmZeros(a[7 - 1, :])[0]) / 100. * neIRI      # in m-3
        nplusIRI = squeeze(self._RmZeros(a[11 - 1, :])[0]) / 100. * neIRI      # in m-3

        iri = {'ne' : neIRI, 'te' : teIRI, 'ti' : tiIRI, 'neFIRI' : iri_ne_firi,
            'oplus' : oplusIRI, 'o2plus' : o2plusIRI, 'noplus' : noplusIRI,
            'hplus' : hplusIRI, 'heplus' : heplusIRI, 'nplus' : nplusIRI}

        iriadd = { 'NmF2' : b[1 - 1, :][0], 'hmF2' : b[2 - 1, :][0],
                'B0' : b[10 - 1, :][0] }

        return iri, iriadd


    def _RmZeros(self, inputs):

        """ Replace "zero" values with 'NaN' """

        ind = where(inputs == 0.0)[0]
        if (len(ind) > 0): inputs[ind] = nan
        return(inputs)


    def _RmNeg(self, inputs):

        """ Replace negative values with 'NaN'  """

        ind = where(inputs < 0.)[0]
        if len(ind) > 0: inputs[ind] = nan
        return inputs


class IRI2016Profile(IRI2016):

    def __init__(self, alt=300., altlim=[90.,150.], altstp=2.,  htecmax=0,
                    time=datetime.now(), hrlim=[0., 24.], hrstp=.25,
                    iut=1, jmag=0,
                    lat=0., latlim=[-90, 90], latstp=10.,
                    lon=0., lonlim=[-180,180], lonstp=20.,
                    option=1, verbose=False):

        if isinstance(time,str):
            time = parse(time)

        self.iriDataFolder = Path(__file__).parent / 'data'

        self.jf = self.Switches()

        self.addinp = list(map(lambda x : -1, range(12)))

        self.option = option

        if option == 1:     # Height Profile
            self.vbeg = altlim[0]
            self.vend = altlim[1]
            self.vstp = altstp
        elif option == 2:   # Latitude Profile
            self.vbeg = latlim[0]
            self.vend = latlim[1]
            self.vstp = latstp
        elif option == 3:   # Longitude Profile
            self.vbeg = lonlim[0]
            self.vend = lonlim[1]
            self.vstp = lonstp
        elif option == 8:   # Local Time Profile
            self.vbeg = hrlim[0]
            self.vend = hrlim[1]
            self.vstp = hrstp
        else:
            print('Invalid option!')
            return

        self.htecmax = htecmax
        self.jmag = jmag
        self.lat = lat
        self.lon = lon
        self.month = time.month
        self.dom = time.day
        self.mmdd = self.month * 100 + self.dom
        self.year = time.year
        self.iut = iut
        self.hour = time.hour
        self.alt = alt

        self.verbose = verbose
        self.numstp = int((self.vend - self.vbeg) / self.vstp) + 1

        if option == 1: self.HeiProfile()
        elif option == 2: self.LatProfile()
        elif option == 3: self.LonProfile()
        elif option == 8: self.HrProfile()


    def _CallIRI(self):

        self.a, self.b = iriwebg(self.jmag, self.jf, self.lat, self.lon, self.year, self.mmdd,
                            self.iut, self.hour, self.alt, self.htecmax, self.option, self.vbeg,
                            self.vend, self.vstp, self.addinp, self.iriDataFolder)


    def _Hr2HHMMSS(self):

        self.HH = int(self.hour)
        self.MM = int((self.hour - float(self.HH)) * 60)
        self.SS = int((self.hour - float(self.HH)) * 60 - float(self.MM))


    def _GetTitle(self):

        dateStr = 'DATE: {:4d}-{:02d}-{:02d}'.format(self.year, self.month, self.dom)
        self._Hr2HHMMSS()
        timeStr = 'TIME: {:02d}:{:02d} UT'.format(self.HH, self.MM)
        latStr = '{:6.2f} {:s}'.format(abs(self.lat), 'N' if self.lat > 0 else 'S')
        lonStr = '{:6.2f} {:s}'.format(abs(self.lon), 'E' if self.lon > 0 else 'W')

#        Rz12Str = 'Rz12: {:6.2f}'.format(self.b[32, 0])
        f107Str = 'F107: {:6.2f}'.format(self.b[40, 0])
#        apStr = 'ap: {:3d}'.format(int(self.b[50, 0]))
        ApStr = 'Ap: {:3d}'.format(int(self.b[51, 0]))
#        KpStr = 'Kp: {:3d}'.format(int(self.b[82, 0]))

        if self.option in [1, 8]:
            self.title1 = '{:s} - {:s}  -  {:s}, {:s}'.format(dateStr, timeStr, latStr, lonStr)
        elif self.option == 2:
            self.title1 = '{:s} - {:s}  -  GEOG. LON.: {:s}'.format(dateStr, timeStr, lonStr)
        else:
            pass

        self.title2 = '{:s}  -  {:s}'.format(f107Str, ApStr)
        self.title3 = '{:s} - {:s}   -   {:s} - {:s}'.format(dateStr, timeStr, f107Str, ApStr)


    def HeiProfile(self):

        self._CallIRI()
        a = self.a
        b = self.b

        self._GetTitle()

        if self.verbose:

            print('------------------------------------------------------------------------------------------------------------------------------------------')
            print('  Height\tNe    Ne/NmF2\tTi\tTe\tO+\tH+\tN+    He+    O2+    NO+   Clust.  Rz12   IG12   F107   F107(81)   ap    AP')
            print('------------------------------------------------------------------------------------------------------------------------------------------')

            for i in range(self.numstp):

                varval = self.vbeg + float(i) * self.vstp
                edens = a[1 - 1, i] * 1e-6
                edratio = a[1 - 1, i] / b[1 - 1, 1 - 1]

                print('%8.3f %10.3f %8.3f %8.3f %8.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %7.3f %7.3f %7.3f %7.3f' %
                    (varval, edens, edratio, a[2,i], a[3,i], a[4,i], a[5,i], a[10,i], a[6,i],
                    a[7,i], a[8,i], a[9,i], b[32,i], b[38,i], b[40,i], b[45,i], b[50,i], b[51,i]))


    def LatProfile(self):

        self._CallIRI()

        self._GetTitle()

        if self.verbose:

            latbins = list(map(lambda x : self.vbeg + float(x) * self.vstp, range(self.numstp)))

            print('\tGLON\tGLAT\tNmF2\t\thmF2\tB0')
            for j in range(len(latbins)):
                print('%8.3f %8.3f %8.3e %8.3f %8.3f' % (self.lon, latbins[j], self.b[0, j], self.b[1, j], self.b[9, j]))


    def LonProfile(self):

        self._CallIRI()

        self._GetTitle()

        if self.verbose:

            lonbins = list(map(lambda x : self.vbeg + float(x) * self.vstp, range(self.numstp)))

            print('\tGLON\tGLAT\tNmF2\t\thmF2\tB0')
            for j in range(len(lonbins)):
                print('%8.3f %8.3f %8.3e %8.3f %8.3f' % (lonbins[j], self.lat, self.b[0, j], self.b[1, j], self.b[9, j]))


    def HrProfile(self):

        self._CallIRI()

        self._GetTitle()

        if self.verbose:

            hrbins = list(map(lambda x : self.vbeg + float(x) * self.vstp, range(self.numstp)))

            print('   GLON     GLAT\tHR\tNmF2\thmF2\tB0')
            for j in range(len(hrbins)):
                print('%8.3f %8.3f %8.3f %8.3e %8.3f %8.3f' % (self.lon, self.lat, hrbins[j], self.b[0, j], self.b[1, j], self.b[9, j]))
