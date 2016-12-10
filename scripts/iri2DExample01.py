from iri2016prof2D import IRI2016_2DProf

if __name__ == '__main__':

    def example01():

        iri2016Obj = IRI2016_2DProf(altlim=[100.,1000.], altstp=5., hrstp=.25/3, \
        lat=-11.95, lon=-76.77, month=6, option=1, verbose=False)
        iri2016Obj.HeightVsTime()
        iri2016Obj.Plot2D()

    # 2D Example: Height vs Time
    example01()
