src=./scripts


all:  example.eps

%.eps: %.rplt matplotlibrc
	rplt --savefig $@ $<

%.rplt: scripts/plot_%.py
	python $< 

.PRECIOUS: %.rplt

clean:
	rm -f *.rplt *.pdf *.eps
