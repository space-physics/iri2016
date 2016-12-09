

from pyiri2016.iri2016 import IRI2016
from os.path import dirname, join, realpath
from pyiri2016.iriweb import iriwebg
from numpy import arange, array, ceil, empty, floor, log10, meshgrid, transpose


class IRI2016Profile(IRI2016):

    def __init__(self, alt=300., altlim=[90.,150.], altstp=2., dom=21, htecmax=0, \
                    hour=12., hrlim=[0., 24.], hrstp=.25, \
                    iut=0, jmag=0, \
                    lat=0., latlim=[-90, 90], latstp=10., \
                    lon=0., lonlim=[-180,180], lonstp=20., \
                    month=11, option=1, verbose=True, year=2003):

        self.iriDataFolder = join(dirname(realpath(__file__)), 'data')

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
        self.month, self.dom = month, dom
        self.mmdd = month * 100 + dom
        self.year = year
        self.iut = iut
        self.hour = hour
        self.alt = alt

        self.verbose = verbose
        self.numstp = int((self.vend - self.vbeg) / self.vstp) + 1

        if option == 1: self.HeiProfile()
        elif option == 2: self.LatProfile()
        elif option == 3: self.LonProfile()
        elif option == 8: self.HrProfile()

    #
    # End of '__init__'
    #####


    def _CallIRI(self):

        self.a, self.b = iriwebg(self.jmag, self.jf, self.lat, self.lon, self.year, self.mmdd, \
                            self.iut, self.hour, self.alt, self.htecmax, self.option, self.vbeg, \
                            self.vend, self.vstp, self.addinp, self.iriDataFolder)

    #
    # End of '_CallIRI'
    #####

    def _Hr2HHMMSS(self):

        self.HH = int(self.hour)
        self.MM = int((self.hour - float(self.HH)) * 60)
        self.SS = int((self.hour - float(self.HH)) * 60 - float(self.MM))

    #
    # End of '_Hr2HHMMSS'
    #####

    def GetTitle(self):

        dateStr = 'DATE: {:4d}-{:02d}-{:02d}'.format(self.year, self.month, self.dom)
        self._Hr2HHMMSS()        
        timeStr = 'TIME: {:02d}:{:02d}'.format(self.HH, self.MM)
        latStr = '{:6.2f} {:s}'.format(abs(self.lat), 'N' if self.lat > 0 else 'S')
        lonStr = '{:6.2f} {:s}'.format(abs(self.lon), 'E' if self.lon > 0 else 'W')

        Rz12Str = 'Rz12: {:6.2f}'.format(self.b[32, 0])
        f107Str = 'F107: {:6.2f}'.format(self.b[40, 0])
        apStr = 'ap: {:3d}'.format(int(self.b[50, 0]))
        ApStr = 'Ap: {:3d}'.format(int(self.b[51, 0]))
        KpStr = 'Kp: {:3d}'.format(int(self.b[82, 0]))
        
        self.title1 = '{:s} - {:s}  -  {:s}, {:s}'.format(dateStr, timeStr, latStr, lonStr)
        self.title2 = '{:s}  -  {:s}'.format(f107Str, KpStr)
        

    def HeiProfile(self):

        self._CallIRI()
        a = self.a
        b = self.b

        self.GetTitle()

        if self.verbose:

            print('------------------------------------------------------------------------------------------------------------------------------------------')
            print('  Height\tNe    Ne/NmF2\tTi\tTe\tO+\tH+\tN+    He+    O2+    NO+   Clust.  Rz12   IG12   F107   F107(81)   ap    AP')
            print('------------------------------------------------------------------------------------------------------------------------------------------')                        

            for i in range(self.numstp):
                        
                varval = self.vbeg + float(i) * self.vstp
                edens = a[1 - 1, i] * 1e-6
                edratio = a[1 - 1, i] / b[1 - 1, 1 - 1]

                print('%8.3f %10.3f %8.3f %8.3f %8.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %7.3f %7.3f %7.3f %7.3f' % \
                    (varval, edens, edratio, a[2,i], a[3,i], a[4,i], a[5,i], a[10,i], a[6,i], \
                    a[7,i], a[8,i], a[9,i], b[32,i], b[38,i], b[40,i], b[45,i], b[50,i], b[51,i]))

    #
    # End of 'HeiProfile'
    #####
    

    def LatProfile(self):

        self._CallIRI()

        if self.verbose:

            latbins = list(map(lambda x : self.vbeg + float(x) * self.vstp, range(self.numstp)))

            print('\tGLON\tGLAT\tNmF2\t\thmF2\tB0')
            for j in range(len(latbins)):
                print('%8.3f %8.3f %8.3e %8.3f %8.3f' % (self.lon, latbins[j], self.b[0, j], self.b[1, j], self.b[9, j])) 
            
    #
    # End of 'LatProfile'
    #####


    def LonProfile(self):

        self._CallIRI()

        if self.verbose:

            lonbins = list(map(lambda x : self.vbeg + float(x) * self.vstp, range(self.numstp)))

            print('\tGLON\tGLAT\tNmF2\t\thmF2\tB0')
            for j in range(len(lonbins)):
                print('%8.3f %8.3f %8.3e %8.3f %8.3f' % (lonbins[j], self.lat, self.b[0, j], self.b[1, j], self.b[9, j])) 
            
    #
    # End of 'LonProfile'
    #####


    def HrProfile(self):

        self._CallIRI()

        if self.verbose:

            hrbins = list(map(lambda x : self.vbeg + float(x) * self.vstp, range(self.numstp)))

            print('   GLON     GLAT\tHR\tNmF2\thmF2\tB0')
            for j in range(len(hrbins)):
                print('%8.3f %8.3f %8.3f %8.3e %8.3f %8.3f' % (self.lon, self.lat, hrbins[j], self.b[0, j], self.b[1, j], self.b[9, j])) 
            
    #
    # End of 'HrProfile'
    #####


#
# End of 'IRI2016Profile'
#####



if __name__ == '__main__':


    def main1():

        iri2016Obj = IRI2016Profile(option=1, verbose=True)
        

    # Height Profile Example
    main1()

