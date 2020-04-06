max    *     number of categories
jmax   *     number of samples minus one
kmax   *     number of nuisance parameters
---------------------------------------------------------------------------------------
shapes * * SHAPES__name_.root $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC
---------------------------------------------------------------------------------------
bin					SR_Y_				CR_Y_
observation			_SRN_		_CRN_
---------------------------------------------------------------------------------------
bin					SR_Y_		SR_Y_		SR_Y_		CR_Y_		CR_Y_		CR_Y_
process				0			1			2			0			3			2
process				Sig		qcdsr_Y_		ttbar_Y_	Sig		qcdcr_Y_		ttbar_Y_
rate				_SSR_		_QSR_		_TSR_		_SCR_		_QCR_		_TCR_
---------------------------------------------------------------------------------------
* autoMCStats 0 0 1
lumi_Y_ lnN			_lumU_		-			_lumU_		_lumU_		-			_lumU_
BBSF_Y_ lnN			_bbSFU_		-			_bbSFU_		_bbSFU_		-			_bbSFU_
ttA_Y_ shapeN2		-			1.000		1.000		-			1.000		1.000	
ttN_Y_ shapeN2		-			1.000		1.000		-			1.000		1.000
