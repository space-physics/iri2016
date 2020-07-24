
C
C       > f2py irisubg.for -m irisub -h irisubg.pyf
C       > f2py -c irisubg.pyf irisubg.for irisub.for irifun.for iritec.for iridreg.for cira.for igrf.for iriflip.for
C

        subroutine irisubg(jf,jmag,alati,along,iyyyy,mmdd,dhour,
     &      heibeg,heiend,heistp,dirdata,outf,oarr)

           real,intent(out) :: outf(30,1000),oarr(100)

            logical jf(50)
            integer jmag,iyyyy,mmdd
            real alati,along,dhour,heibeg,heiend,heistp
            character*256 dirdata,dirdata1
  

Cf2py       intent(in) jf,jmag,iyyyy,mmdd,alati,along,dhour
Cf2py       intent(in) heibeg,heiend,heistp,dirdata


    		common /folders/ dirdata1
	    	dirdata1 = trim(dirdata)

            call read_ig_rz
            call readapf107

            call iri_sub(jf,jmag,alati,along,iyyyy,mmdd,dhour,
     &          heibeg,heiend,heistp,outf,oarr)

        end subroutine irisubg



        subroutine irisubgl(jf,jmag,iyyyy,mmdd,dhour,
     &      coordl,lenl,dirdata,outf1,oarr1)

            real, intent(in) :: coordl(lenl,3)
            real, intent(out) :: outf1(30,lenl),oarr1(100,lenl)

            logical jf(50)
            integer jmag,iyyyy,mmdd
            real alati,along,dhour,heibeg,heiend,heistp
            integer lenl,i,j
 
            character*256 dirdata,dirdata1

            real outf(30,1000),oarr(100)

Cf2py       intent(in) jf,jmag,iyyyy,mmdd,dhour,dirdata
Cf2py       integer intent(hide),depend(coordl) :: lenl=shape(coordl,0)

    		common /folders/ dirdata1
	    	dirdata1 = trim(dirdata)

            call read_ig_rz
            call readapf107

            do i=1,lenl

                along = real(coordl(i,1),kind(along))                
                alati = real(coordl(i,3),kind(alati))

                heibeg = real(coordl(i,2),kind(heibeg))
                heiend = heibeg + 1.0
                heistp = 1.0
                
                call iri_sub(jf,jag,alati,along,iyyyy,mmdd,dhour,
     &              heibeg,heiend,heistp,outf,oarr)

                do j=1,30
                    outf1(j,i) = outf(j,1)
                end do

                do j=1,100
                    oarr1(j,i) = oarr(j)                    
                end do                

            end do

        end subroutine irisubgl
