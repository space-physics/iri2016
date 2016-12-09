
		subroutine iriwebg(inJMAG,inJF,inALATI,inALONG,inIYYYY,
     &	inMMDD,inIUT,inDHOUR,inHEIGHT,inH_TEC_MAX,
     &	inIVAR,inVBEG,inVEND,inVSTP,inADDINP,dirdata,outA,outB)

		real*8 inJMAG,inJF(50),inALATI,inALONG,inIYYYY,
     &	inMMDD,inIUT,inDHOUR,inHEIGHT,inH_TEC_MAX,
     &	inIVAR,inVBEG,inVEND,inVSTP,inADDINP(12)
		real*8 outA(30,1000),outB(100,1000)
		character*256 dirdata,dirdata1

		logical jf(50)
		dimension addinp(12),a(30,1000),b(100,1000)

		integer i

Cf2py	intent(in) inJMAG, inJF, inALATI, inALONG, inIYYYY, inMMDD
Cf2py	intent(in) inIUT, inDHOUR, inHEIGHT, inH_TEC_MAX, inIVAR
Cf2py	intent(in) inVBEG, inVEND, inVSTP, inADDINP, dirdata
Cf2py	intent(out) outA, outB		

		common /folders/ dirdata1
		dirdata1 = trim(dirdata)
		
		call read_ig_rz
        call readapf107

		jmag = int(inJMAG, kind(jmag))
		do i = 1, 50
			if(inJF(i).ge.1.) then
				jf(i) = .true.
			else
				jf(i) = .false.
			endif
		end do
		alati = real(inALATI, kind(alati))
		along = real(inALONG, kind(along))
		iyyyy = int(inIYYYY, kind(iyyyy))
		mmdd = int(inMMDD, kind(mmdd))
		iut = int(inIUT, kind(iut))
		dhour = real(inDHOUR, kind(dhour))
		height = real(inHEIGHT, kind(height))
		h_tec_max = real(inH_TEC_MAX, kind(h_tec_max))
		ivar = int(inIVAR, kind(ivar))
		vbeg = real(inVBEG, kind(vbeg))
		vend = real(inVEND, kind(vend))
		vstp = real(inVSTP, kind(vstp))
		do i = 1, 12
			addinp(i) = real(inADDINP(i), kind(addinp))
		end do
C	foF2 or NmF2
		if(addinp(1).ne.-1) then
			jf(8) = .false.
			b(1,1) = addinp(1)
		endif
C	hmF2 or M(3000)F2
		if(addinp(2).ne.-1) then
			jf(9) = .false.
			b(2,1) = addinp(2)
		endif
C	Ne(300km)		
		if(addinp(3).ne.-1) then
			jf(10) = .false.
			do i = 1, 1000
				b(15,i) = addinp(3)
			end do
		endif
C	Ne(400km)		
		if(addinp(4).ne.-1) then
			jf(10) = .false.
			do i = 1, 1000
				b(16,i) = addinp(4)
			end do
		endif
C	Ne(550km)		
		if(addinp(5).ne.-1) then
			jf(10) = .false.
			jf(23) = .false.
			do i = 1, 1000
				b(16,i) = addinp(5)
			end do
		endif
C	foF1 or NmF1		
		if(addinp(6).ne.-1) then
			jf(13) = .false.
			b(3,1) = addinp(6)
		endif
C	hmF1		
		if(addinp(7).ne.-1) then
			jf(14) = .false.
			b(4,1) = addinp(7)
		endif
C	foE or NmE		
		if(addinp(8).ne.-1) then
			jf(15) = .false.
			b(5,1) = addinp(8)
		endif
C	hmE		
		if(addinp(9).ne.-1) then
			jf(16) = .false.
			b(6,1) = addinp(9)
		endif
C	Rz12		
		if(addinp(10).ne.-1) then
			jf(17) = .false.
			do i = 1, 1000
				b(33,i) = addinp(10)
			end do
		endif
C	F10.7		
		if(addinp(11).ne.-1) then
			jf(21) = .true.
			jf(23) = .false.
			jf(24) = .false.
			jf(25) = .false.
			jf(28) = .false.
			do i = 1, 1000
				b(41,i) = addinp(11)
			end do
		endif
C	IG12		
		if(addinp(12).ne.-1) then
			jf(27) = .false.
			do i = 1, 1000
				b(39,i) = addinp(12)
			end do
		endif

		call iri_web(jmag,jf,alati,along,iyyyy,mmdd,iut,dhour,
     &	height,h_tec_max,ivar,vbeg,vend,vstp,a,b)

		do j = 1, 1000
			do i = 1, 30
				outA(i,j) = real(a(i,j), 8)
			end do
			do i = 1, 100
				outB(i,j) = real(b(i,j), 8)
			end do
		end do

		end subroutine



        subroutine irisubg(jf,jmag,alati,along,iyyyy,mmdd,dhour,
     &      heibeg,heiend,heistp,dirdata,outf,oarr)

            logical jf(50)
            integer jmag,iyyyy,mmdd
            real alati,along,dhour,heibeg,heiend,heistp
            character*256 dirdata,dirdata1
            dimension outf(30,1000),oarr(100)

Cf2py       intent(in) jf,jmag,iyyyy,mmdd,alati,along,dhour
Cf2py       intent(in) heibeg,heiend,heistp,dirdata
Cf2py       intent(out) outf,oarr

    		common /folders/ dirdata1
	    	dirdata1 = trim(dirdata)

            call read_ig_rz
            call readapf107

            call iri_sub(jf,jmag,alati,along,iyyyy,mmdd,dhour,
     &          heibeg,heiend,heistp,outf,oarr)

        end subroutine irisubg



        subroutine irisubgl(jf,jmag,iyyyy,mmdd,dhour,
     &      coordl,lenl,dirdata,outf1,oarr1)

            logical jf(50)
            integer jmag,iyyyy,mmdd
            real alati,along,dhour,heibeg,heiend,heistp
            integer lenl,i,j
            dimension coordl(lenl,3)
            character*256 dirdata,dirdata1
            real outf1(30,lenl),oarr1(100,lenl)
            dimension outf(30,1000),oarr(100)

Cf2py       intent(in) jf,jmag,iyyyy,mmdd,dhour,coordl,dirdata
Cf2py       integer intent(hide),depend(coordl) :: lenl=shape(coordl,0)
Cf2py       intent(out) outf1,oarr1

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
