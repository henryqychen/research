TEX_FILE_NAME=starcraft
LATEX=xelatex
BIBTEX=bibtex

all:
	@${LATEX} 	${TEX_FILE_NAME}.tex
	@${BIBTEX} 	${TEX_FILE_NAME}.aux
	@${LATEX} 	${TEX_FILE_NAME}.tex
	@${LATEX} 	${TEX_FILE_NAME}.tex

clean:
	-@find . -type f -iregex '.*\.\(aux\|log\|toc\|backup\|acr\|brf\|gz\|acn\|xdy\|alg\)$$' -delete
