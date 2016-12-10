from iri2016prof2D import IRI2016_2DProf
from scipy import arange

if __name__ == '__main__':

    def example02():

        lonstp = 4
                
        iri2016Obj = IRI2016_2DProf(hour=17, lat=-11.95, latstp=2., lon=-76.77, lonstp=lonstp, \
                                    month=9, option=2, verbose=False, year=2010)
        iri2016Obj.LatVsLon(lonstp=lonstp)
        iri2016Obj.Plot2D()
    

    # 2D Example: Lat vs Lon, Earth's Map
    example02()
    