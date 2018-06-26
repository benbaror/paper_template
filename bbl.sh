sed -i -e '/^\\bibliography{.*/r ms.bbl' $1
sed  -i -e '/^\\bibliography{.*/d' $1
sed  -i -e '/^\\bibliographystyle{.*/d' $1

