from pathlib import Path
from datetime import datetime, timedelta
from dateutil.parser import parse
import xarray
import numpy as np
#
import iri16  # fortran

proot = Path(__file__).parent
simout = ['ne', 'Tn', 'Ti', 'Te', 'nO+', 'nH+', 'nHe+', 'nO2+', 'nNO+']


def datetimerange(start: datetime, end: datetime, step: timedelta) -> list:
    """like range() for datetime!"""
    if isinstance(start, str):
        start = parse(start)

    if isinstance(end, str):
        end = parse(end)

    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert isinstance(step, timedelta)

    return [start + i*step for i in range((end-start) // step)]


def Switches():
    """
     IRI switches to turn on/off several options
    """

    jf = np.ones(50, dtype=bool)

    #    i          1                       0                 standard version
    #    ------------------------------------------------------------------------
    jf[1 - 1] = 1  # 1    Ne computed            Ne not computed                     1
    jf[2 - 1] = 1  # 2    Te, Ti computed        Te, Ti not computed                 1
    jf[3 - 1] = 1  # 3    Ne & Ni computed       Ni not computed                     1
    jf[4 - 1] = 0  # 4    B0 - Table option      B0 - other models jf(31)            0
    jf[5 - 1] = 0  # 5    foF2 - CCIR            foF2 - URSI                         0
    jf[6 - 1] = 0  # 6    Ni - DS-95 & DY-85     Ni - RBV-10 & TTS-03                0
    jf[7 - 1] = 1  # 7    Ne - Tops: f10.7<188   f10.7 unlimited                     1
    jf[8 - 1] = 1  # 8    foF2 from model        foF2 or NmF2 - user input           1
    jf[9 - 1] = 1  # 9    hmF2 from model        hmF2 or M3000F2 - user input        1
    jf[10 - 1] = 1  # 10    Te - Standard          Te - Using Te/Ne correlation        1
    jf[11 - 1] = 1  # 11    Ne - Standard Profile  Ne - Lay-function formalism         1
    jf[12 - 1] = 1  # 12    Messages to unit 6     to meesages.text on unit 11         1
    jf[13 - 1] = 1  # 13    foF1 from model        foF1 or NmF1 - user input           1
    jf[14 - 1] = 1  # 14    hmF1 from model        hmF1 - user input (only Lay version)1
    jf[15 - 1] = 1  # 15    foE  from model        foE or NmE - user input             1
    jf[16 - 1] = 1  # 16    hmE  from model        hmE - user input                    1
    jf[17 - 1] = 1  # 17    Rz12 from file         Rz12 - user input                   1
    jf[18 - 1] = 1  # 18    IGRF dip, magbr, modip old FIELDG using POGO68/10 for 1973 1
    jf[19 - 1] = 1  # 19    F1 probability model   critical solar zenith angle (old)   1
    jf[20 - 1] = 1  # 20    standard F1            standard F1 plus L condition        1
    jf[21 - 1] = 1  # 21    ion drift computed     ion drift not computed              0
    jf[22 - 1] = 0  # 22    ion densities in %     ion densities in m-3                1
    jf[23 - 1] = 0  # 23    Te_tops (Aeros,ISIS)   Te_topside (TBT-2011)               0
    jf[24 - 1] = 1  # 24    D-region: IRI-95       Special: 3 D-region models (FIRI)   1
    jf[25 - 1] = 1  # 25    F107D from APF107.DAT  F107D user input (oarr(41))         1
    jf[26 - 1] = 0  # 26    foF2 storm model       no storm updating                   1
    jf[27 - 1] = 1  # 27    IG12 from file         IG12 - user                         1
    jf[28 - 1] = 0  # 28    spread-F probability   not computed                        0
    jf[29 - 1] = 0  # 29    IRI01-topside          new options as def. by JF(30)       0
    jf[30 - 1] = 0  # 30    IRI01-topside corr.    NeQuick topside model               0
    # (29,30) = (1,1) IRIold, (0,1) IRIcor, (0,0) NeQuick, (1,0) Gulyaeva
    jf[31 - 1] = 1  # 31    B0,B1 ABT-2009         B0 Gulyaeva h0.5                    1
    jf[32 - 1] = 1  # 32    F10.7_81 from file     PF10.7_81 - user input (oarr(46))   1
    jf[33 - 1] = 0  # 33    Auroral boundary model on/off  true/false                  0
    jf[34 - 1] = 0  # 34    Messages on            Messages off                        1
    jf[35 - 1] = 0  # 35    foE storm model        no foE storm updating               0
    #   ..    ....
    #   50    ....
    #   ------------------------------------------------------------------

    return jf


def IRI(time, altkm, glat, glon, ap=None, f107=None, ssn=None, var=None):

    if isinstance(time, str):
        time = parse(time)

    altkm = np.atleast_1d(altkm)

#        doy = squeeze(TimeUtilities().CalcDOY(year, month, dom))

    # IRI options
    jf = Switches()

    # additional "input parameters" (necessary to scale the empirical model results
    # to measurements)
#    addinp = -np.ones(12)

    # ------------------------------------------------------------------------------
    #
#    if time.year < 1958:
#
#        addinp[10 - 1] = ssn  # RZ12  (This switches 'jf[17 - 1]' to '0' and
#                            # uses correlation function to estimate IG12)
#
#        jf[25 - 1] = 1        #   25    F107D from APF107.DAT  F107D user input (oarr(41))         1
#        jf[27 - 1] = 1        #   27    IG12 from file         IG12 - user                         1
#        jf[32 - 1] = 1        #   32    F10.7_81 from file     PF10.7_81 - user input (oarr(46))   1
#
#    else:  # case for solar and geomagnetic indices from files
#
#        jf[17 - 1] = 1        #   17    Rz12 from file         Rz12 - user input                   1
#        jf[26 - 1] = 1        #   26    foF2 storm model       no storm updating                   1
#        jf[35 - 1] = 1        #   35    foE storm model        no foE storm updating               0
#     #
#     #------------------------------------------------------------------------------

    mmdd = 100*time.month + time.day               # month and dom (MMDD)
    # hour + 25 denotes UTC time
    dhour = (time.hour + 25) + time.minute/60.
# %% more inputs
    jmag = 0  # 0: geographic; 1: geomagnetic
    # iut = 0             #  0: for LT;     1: for UT
    # height = 300.       #  in km
    # h_tec_max = 2000    #  0: no TEC; otherwise: upper boundary for integral
    # ivar = var          #  1: altitude; 2: latitude; 3: longitude; ...

    # Ionosphere (IRI)
#        a, b = iriwebg(jmag, jf, glat, glon, int(time.year), mmdd, iut, time.hour,
#            height, h_tec_max, ivar, ivbeg, ivend, ivstp, addinp, self.iriDataFolder)

    outf, oarr = iri16.iri_sub(jf, jmag, glat, glon,
                               time.year, mmdd, dhour, altkm,
                               proot/'data/')

# %% collect output
    dsf = {k: (('time', 'alt_km', 'lat', 'lon'), np.atleast_2d(v[None, :, None, None])) for (k, v) in zip(simout, outf[:9, :])}

    dsf.update({'NmF2': (('time', 'lat', 'lon'), np.atleast_3d(oarr[0]))})
    dsf.update({'hmF2': (('time', 'lat', 'lon'), np.atleast_3d(oarr[1]))})
    dsf.update({'NmF1': (('time', 'lat', 'lon'), np.atleast_3d(oarr[2]))})
    dsf.update({'hmF1': (('time', 'lat', 'lon'), np.atleast_3d(oarr[3]))})
    dsf.update({'NmE': (('time', 'lat', 'lon'), np.atleast_3d(oarr[4]))})
    dsf.update({'hmE': (('time', 'lat', 'lon'), np.atleast_3d(oarr[5]))})
    dsf.update({'B0': (('time', 'lat', 'lon'), np.atleast_3d(oarr[9]))})

    iri = xarray.Dataset(dsf,
                         coords={'time': [time], 'alt_km': altkm, 'lat': [glat], 'lon': [glon]},
                         attrs={'f107': oarr[40], 'ap': oarr[50],
                                'glat': glat, 'glon': glon, 'time': time,
                                })

# FIRI Ne (in m-3)
#        iri_ne_firi = self._RmNeg(a[13 - 1, :])[0]

# Ionic density (NO+, O2+, O+, H+, He+, N+, Cluster Ions)

#        iri = {'ne' : neIRI, 'te' : teIRI, 'ti' : tiIRI, 'neFIRI' : iri_ne_firi,
#            'oplus' : oplusIRI, 'o2plus' : o2plusIRI, 'noplus' : noplusIRI,
#            'hplus' : hplusIRI, 'heplus' : heplusIRI, 'nplus' : nplusIRI}

#        iriadd = { 'NmF2' : b[1 - 1, :][0], 'hmF2' : b[2 - 1, :][0],
#                'B0' : b[10 - 1, :][0] }

    return iri


def timeprofile(tlim: tuple, dt: timedelta,
                altkm: np.ndarray, glat: float, glon: float) -> xarray.Dataset:
    """compute IRI90 altitude profile over time range for fixed lat/lon
    """

    T = datetimerange(tlim[0], tlim[1], dt)

    altkm = np.atleast_1d(altkm)

    iono: xarray.Dataset = None

    f107 = []
    ap = []
    for t in T:
        iri = IRI(t, altkm, glat, glon)
        if iono is None:
            iono = iri
        else:
            iono = xarray.merge((iono, iri))

        f107.append(iri.f107)
        ap.append(iri.ap)

    iono.attrs = iri.attrs
    iono.attrs['f107'] = f107
    iono.attrs['ap'] = ap

    return iono


def geoprofile(latlim: tuple, dlat: float, glon: float,
               altkm: np.ndarray, time: datetime) -> xarray.Dataset:
    """compute IRI90 altitude profiles at time, over lat or lon range
    """

    glat = np.arange(*latlim, dlat)

    altkm = np.atleast_1d(altkm)

    iono: xarray.Dataset = None

    f107 = []
    ap = []
    for l in glat:
        iri = IRI(time, altkm, l, glon)
        if iono is None:
            iono = iri
        else:
            iono = xarray.merge((iono, iri))

        f107.append(iri.f107)
        ap.append(iri.ap)

    iono.attrs = iri.attrs
    iono.attrs['f107'] = f107
    iono.attrs['ap'] = ap

    return iono


#    def _CallIRI(self):
#
#        self.a, self.b = iriwebg(self.jmag, self.jf, self.lat, self.lon, self.year, self.mmdd,
#                            self.iut, self.hour, self.alt, self.htecmax, self.simtype, self.vbeg,
#                            self.vend, self.vstp, self.addinp, self.iriDataFolder)

    def _Hr2HHMMSS(self):

        self.HH = int(self.hour)
        self.MM = int((self.hour - float(self.HH)) * 60)
        self.SS = int((self.hour - float(self.HH)) * 60 - float(self.MM))

    def _GetTitle(self):

        dateStr = f'{self.year:4d}-{self.month:02d}-{self.dom:02d}'
        self._Hr2HHMMSS()
        timeStr = 'TIME: {:02d}:{:02d} UT'.format(self.HH, self.MM)
        latStr = '{:6.2f} {:s}'.format(abs(self.lat), 'N' if self.lat > 0 else 'S')
        lonStr = '{:6.2f} {:s}'.format(abs(self.lon), 'E' if self.lon > 0 else 'W')

#        Rz12Str = 'Rz12: {:6.2f}'.format(self.b[32, 0])
        f107Str = f'F107: {self.b[40, 0]:6.2f}'
#        apStr = 'ap: {:3d}'.format(int(self.b[50, 0]))
        ApStr = f'Ap: {int(self.b[51, 0]):3d}'
#        KpStr = 'Kp: {:3d}'.format(int(self.b[82, 0]))

        if self.option == 'vertical':
            self.title1 = f'{dateStr:s} - {timeStr:s}  -  {latStr:s}, {lonStr:s}'
        elif self.option == 'lat':
            self.title1 = '{:s} - {:s}  -  GEOG. LON.: {:s}'.format(dateStr, timeStr, lonStr)
        elif self.option == 'time':
            self.title1 = f'{dateStr}   {latStr}, {lonStr}'
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

            print('  Height\tNe    Ne/NmF2\tTi\tTe\tO+\tH+\tN+    He+    O2+    NO+'
                  '   Clust.  Rz12   IG12   F107   F107(81)   ap    AP')
            print('-----------------------------------------------------------------------------------------'
                  '-------------------------------------------------')

            for i in range(self.numstp):

                varval = self.vbeg + float(i) * self.vstp
                edens = a[1 - 1, i] * 1e-6
                edratio = a[1 - 1, i] / b[1 - 1, 1 - 1]

                print('%8.3f %10.3f %8.3f %8.3f %8.3f %6.3f %6.3f %6.3f %6.3f %6.3f'
                      ' %6.3f %6.3f %6.3f %6.3f %7.3f %7.3f %7.3f %7.3f' %
                      (varval, edens, edratio, a[2, i], a[3, i], a[4, i], a[5, i], a[10, i], a[6, i],
                       a[7, i], a[8, i], a[9, i], b[32, i], b[38, i], b[40, i], b[45, i], b[50, i], b[51, i]))
