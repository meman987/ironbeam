iron:
	python3 iron1.py input
	python3 iron2.py input/PURCHASE_AND_SALE.out pur
	python3 iron2.py input/CONFIRMATION.out conf
	mv input/PURCHASE_AND_SALE.csv iron_pur.csv
	mv input/CONFIRMATION.csv      iron_conf.csv
	hledger print -f iron_pur.csv  > iron_pur_csv.lgr
	hledger print -f iron_conf.csv > iron_conf_csv.lgr
	cat iron_ib.lgr iron_pur_csv.lgr iron_conf_csv.lgr > iron.lgr 
	hledger bal -f iron.lgr

