        subroutine iri_web(jmag,jf,alati,along,iyyyy,mmdd,iut,dhour,
     &          height,h_tec_max,ivar,vbeg,vend,vstp,a,b)
c-----------------------------------------------------------------------        
c changes:
c       11/16/99 jf(30) instead of jf(17)
c       10/31/08 outf, a, b (100 -> 500)
c
c-----------------------------------------------------------------------        
c input:   jmag,alati,along,iyyyy,mmdd,dhour  see IRI_SUB
c          height  height in km
c          h_tec_max  =0 no TEC otherwise upper boundary for integral
c          iut     =1 for UT       =0 for LT
c          ivar    =1      altitude
c                  =2,3    latitude,longitude
c                  =4,5,6  year,month,day
c                  =7      day of year
c                  =8      hour (UT or LT)
c          vbeg,vend,vstp  variable range (begin,end,step)
c output:  a       similar to outf in IRI_SUB
c          b       similar to oarr in IRI_SUB
c
c          numstp  number of steps; maximal 1000
c-----------------------------------------------------------------------        
        dimension   outf(20,1000),oar(100),oarr(100),a(20,1000)
        dimension   xvar(8),b(100,1000)
        logical     jf(50)

		nummax=1000
        numstp=int((vend-vbeg)/vstp)+1
        if(numstp.gt.nummax) numstp=nummax

        do 6249 i=1,100
6249          oar(i)=b(i,1) 

        if(ivar.eq.1) then
            do 1249 i=1,100
1249            oarr(i)=oar(i) 
            xhour=dhour+iut*25.
            call IRI_SUB(JF,JMAG,ALATI,ALONG,IYYYY,MMDD,XHOUR,
     &                  VBEG,VEND,VSTP,a,OARR)
            if(h_tec_max.gt.50.) then 
                call iri_tec (50.,h_tec_max,2,tec,tect,tecb)
                oarr(37)=tec
                oarr(38)=tect
                endif
            do 1111 i=1,100
1111            b(i,1)=oarr(i)
            return
            endif

        if(height.le.0.0) height=100
        xvar(2)=alati
        xvar(3)=along
        xvar(4)=iyyyy
        xvar(5)=mmdd/100
        xvar(6)=mmdd-xvar(5)*100
        xvar(7)=abs(mmdd*1.)
        xvar(8)=dhour

        xvar(ivar)=vbeg

        alati=xvar(2)
        along=xvar(3)
        iyyyy=int(xvar(4))
        if(ivar.eq.7) then
                mmdd=-int(vbeg)
        else
                mmdd=int(xvar(5)*100+xvar(6))
        endif
        dhour=xvar(8)+iut*25.

        do 1 i=1,numstp
                do 1349 iii=1,100
1349                    oarr(iii)=b(iii,i) 
                call IRI_SUB(JF,JMAG,ALATI,ALONG,IYYYY,MMDD,DHOUR,
     &                  height,height,1.,OUTF,OARR)
                if(h_tec_max.gt.50.) then
                        call iri_tec (50.,h_tec_max,2,tec,tect,tecb)
                        oarr(37)=tec
                        oarr(38)=tect
                        endif
                do 2 ii=1,20
2                       a(ii,i)=outf(ii,1)
                do 2222 ii=1,100
2222                    b(ii,i)=oarr(ii)
                xvar(ivar)=xvar(ivar)+vstp

                alati=xvar(2)
                along=xvar(3)
                iyyyy=int(xvar(4))
                if(ivar.eq.7) then
                        mmdd=-xvar(7)
                else
                        mmdd=int(xvar(5)*100+xvar(6))
                endif
                dhour=xvar(8)+iut*25.
1       continue

        return
        end

