all: build/V44.pdf

build/V44.pdf: V44.tex build lit.bib header.tex content/theorie.tex content/durchfuehrung.tex content/auswertung.tex content/diskussion.tex
	lualatex --output-directory=build --interaction=batchmode --halt-on-error V44.tex
	biber build/V44.bcf
	lualatex --output-directory=build --interaction=batchmode --halt-on-error V44.tex

build : 
	mkdir -p build
clean : 
	rm -rf build

.PHONY : all clean
