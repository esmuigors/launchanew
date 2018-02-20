#!/usr/bin/python
import sys, math

if len(sys.argv) > 3:
	foerster=float(sys.argv[1])
	seconder=float(sys.argv[2])
	threshol=float(sys.argv[3])
	try:
		#if abs(foerster-seconder) > threshol:
			logarr=int(math.floor(math.log10(abs(foerster-seconder)/threshol*0.00045))) #logarr=int(round(math.log10(abs(foerster-seconder))))
		#else:
		#	logarr=-100
	
	except OverflowError:
		logarr=-50
	except ValueError:
		logarr=-50
else:
	logarr=500

print(logarr)

