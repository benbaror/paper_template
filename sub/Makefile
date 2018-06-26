TEXtoPDF = pdflatex -halt-on-error

ms: ms.pdf

ms.pdf : ms.tex
	${TEXtoPDF} ms.tex
	${TEXtoPDF} ms.tex
	tar -cf ms.tar Fig*.eps *.cls ms.tex

clean:
	rm -f Fig*.pdf ms.aux *.bib *.log *.bbl
