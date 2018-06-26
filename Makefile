
TEXtoPDF = texfot pdflatex 
BIBTEX = bibtex
COUNT =  sh textcount.sh
BBL = sh bbl.sh

ms: ms.pdf
main: main.pdf
sub: sub/ms.pdf

ms.pdf : ms.tex main.bib 
	${TEXtoPDF} ms.tex 
	${BIBTEX} ms
	${TEXtoPDF} ms.tex > /dev/null
	${BBL} ms.tex
	${TEXtoPDF} ms.tex
	${COUNT} ms.tex > stats.txt
	cat stats.txt



ms.tex : main.tex
	latexpand main.tex > ms.tex

main.pdf : main.tex style/preamble.tex
	${TEXtoPDF} main.tex
	${BIBTEX} main
	${TEXtoPDF} main.tex
	${TEXtoPDF} main.tex

sub/ms.pdf: ms.pdf main.bib latexpand_eps.py make_for_sub
	rm -rf sub
	python latexpand_eps.py ms.tex sub
	cp *.cls sub
	cp make_for_sub sub/Makefile
	make -C sub ms clean

clean:
	rm -f ms.* msNotes.bib
