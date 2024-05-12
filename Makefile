INPUT_MD = $(wildcard *.md)

all: $(INPUT_MD)
	pandoc -o contributions.pdf contributions.md
	pandoc -o README.md report.pdf
