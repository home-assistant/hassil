all:
	antlr4 -Dlanguage=Python3 HassILGrammar.g4 -visitor -o hassil/grammar
	touch hassil/grammar/__init__.py
