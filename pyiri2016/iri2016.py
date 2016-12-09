
from math import ceil, floor
from os.path import dirname, join, realpath
from pyiri2016.iriweb import iriwebg
from timeutil.timeutil import TimeUtilities
from scipy import arange, nan, ones, squeeze, where



class IRI2016:


    def __init__(self):
        
        self.iriDataFolder = join(dirname(realpath(__file__)), 'data')

    #
    # End of '__init__' 
    #####


    def Switches(self):

        # IRI switches to turn on/off several options 

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
        jf[21 - 1] = 0; #   21    ion drift computed     ion drift not computed              0
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

    #
    # End of 'Switches'
    #####


    def IRI(self, ap=5, dom=21, f107=150, glat=0., glon=0., \
                hrlt=12., month=3, ssn=150, var=1, vbeg=130., \
                vend=130.+1., vstp=1., year=1980):

        doy = squeeze(TimeUtilities().CalcDOY(year, month, dom))

        hh, mm, ss = TimeUtilities().ToHMS(hrlt)

        # IRI options
        jf = self.Switches()

        # additional "input parameters" (necessary to scale the empirical model results 
        # to measurements)
        addinp = -ones(12)

        #------------------------------------------------------------------------------
        #
        if year < 1958:

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
        
        mmdd = int(1e2 * month) + dom                  # month and dom (MMDD)

        #
        # more inputs ...
        #
        jmag = 0       #  0: geographic; 1: geomagnetic
        iut = 0        #  0: for LT;     1: for UT
        height = 300.  #  in km
        h_tec_max = 0  #  0: no TEC; otherwise: upper boundary for integral
        ivar = var     #  1: altitude; 2: latitude; 3: longitude; ... 

        ivbeg = vbeg
        ivend = vend
        ivstp = vstp

        # Ionosphere (IRI)
        a, b = iriwebg(jmag, jf, glat, glon, year, mmdd, iut, hrlt, \
                            height, h_tec_max, ivar, ivbeg, ivend, ivstp, addinp, self.iriDataFolder)

        bins = arange(ivbeg, ivend + ivstp * 0., ivstp)
        a = a[:, arange(len(bins))]
        b = b[:, arange(len(bins))]

        #
        # Data Conditioning ...
        #

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

        iri = {'ne' : neIRI, 'te' : teIRI, 'ti' : tiIRI, 'neFIRI' : iri_ne_firi, \
            'oplus' : oplusIRI, 'o2plus' : o2plusIRI, 'noplus' : noplusIRI, \
            'hplus' : hplusIRI, 'heplus' : heplusIRI, 'nplus' : nplusIRI}

        iriadd = { 'NmF2' : b[1 - 1, :][0], 'hmF2' : b[2 - 1, :][0], \
                'B0' : b[10 - 1, :][0] }

        return iri, iriadd

#  #
#  ###############################################################################


    def _RmZeros(self, inputs):

        """ Replace "zero" values with 'NaN' """

        ind = where(inputs == 0.0)[0]
        if (len(ind) > 0): inputs[ind] = nan
        return(inputs)

    #
    # End of 'rmzeros'
    #####


    def _RmNeg(self, inputs):

        """ Replace negative values with 'NaN'  """

        ind = where(inputs < 0.)[0]
        if len(ind) > 0: inputs[ind] = nan
        return inputs

    #
    # End of 'rmneg'
    #####



if __name__ == '__main__':

    def main1():

        Obj = IRI2016()
        IRIData, IRIDATAAdd = Obj.IRI()
        print(IRIData['ne'])
        print(IRIDATAAdd['NmF2'], IRIDATAAdd['hmF2'])


    main1()
