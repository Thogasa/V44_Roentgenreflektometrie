all: build/V44.pdf

build/V44.pdf: V44.tex build lit.bib header.tex content/theorie.tex content/durchfuehrung.tex content/auswertung.tex content/diskussion.tex build/plotdecScan.pdf build/plotparratt.pdf build/plotreflecScan.pdf build/plotrockingScan.pdf build/plotzScan.pdf
	lualatex --output-directory=build --interaction=batchmode --halt-on-error V44.tex
	biber build/V44.bcf
	lualatex --output-directory=build --interaction=batchmode --halt-on-error V44.tex

build/Scan_1_Detector.txt: data/Scan_1_Detector.UXD data/Scan_2_Z.UXD data/Scan_3_Rocking.UXD data/Scan_4_Z.UXD data/Scan_5_Rocking.UXD data/Scan_6_Oszillation_bei_0.UXD data/Scan_7_Oszillation_bei_0,1.UXD UXDtoTXT.py
	python UXDtoTXT.py Scan_1_Detector
	python UXDtoTXT.py Scan_2_Z
	python UXDtoTXT.py Scan_3_Rocking
	python UXDtoTXT.py Scan_4_Z
	python UXDtoTXT.py Scan_5_Rocking
	python UXDtoTXT.py Scan_6_Oszillation_bei_0 
	python UXDtoTXT.py Scan_7_Oszillation_bei_0,1

build/plotdecScan.pdf : build/Scan_1_Detector.txt detectorscan.py 
	python detectorscan.py

build/plotparratt.pdf : build/Scan_1_Detector.txt parratt.py 
	python parratt.py
build/plotreflecScan.pdf : build/Scan_1_Detector.txt reflec.py 
	python reflec.py
build/plotrockingScan.pdf : build/Scan_1_Detector.txt rockingscan.py 
	python rockingscan.py
build/plotzScan.pdf : build/Scan_1_Detector.txt zscan.py 
	python zscan.py


build : 
	mkdir -p build
clean : 
	rm -rf build

.PHONY : all clean
