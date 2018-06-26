src=./scripts


all:  example_1a.eps example_1b.eps example_1c.eps example_2.eps

%.eps: %.rplt matplotlibrc
	rplt --savefig $@ $<

%.rplt: scripts/plot_example.py
	python $< --save $@

.PRECIOUS: %.rplt

clean:
	rm -f *.rplt *.pdf *.eps
