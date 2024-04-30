.PHONY: format
format:
	python -m ufmt format .

.PHONY: test
test:
	ADVICE_DIR=. advice-animal test
