\rm -f tmp.tex
sed 's@^\\begin{document}@ \\begin{document} \\n \\n %TC:ignore @; s@^\\begin{abstract}@ %@ ; s@^\\end{abstract}@ %TC:endignore@; s@^\\acknowledgements@ %TC:ignore@  ;  s@^\\end{document}@  %TC:endignore \\n \\end{document} @' $1 | sed 's/\\n/\'$'\n/g' > tmp.tex
n=`perl texcount.pl tmp.tex |  grep 'Words in text'`
echo $n "out of 3500 words"

\rm -f tmp.tex
sed 's@^\\begin{document}@ \\begin{document} \\n \\n %TC:ignore @; s@^\\begin{abstract}@ %TC:endignore@ ; s@^\\end{abstract}@ %TC:ignore@ ; s@^\\end{document}@  %TC:endignore \\n \\end{document} @' $1 | sed 's/\\n/\'$'\n/g' > tmp.tex
n=`perl texcount.pl tmp.tex |  grep 'Words in text' | sed 's@text@abstract@'`
\rm -f tmp.tex
echo $n "out of 250 words"
