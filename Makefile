scores:
	python3 main.py

fetch:
	python3 request_logic.py

ranking:
	python3 ranking.py

clean:
	rm -f CubaWeeki.db

# ESTO ES LO QUE HAY QUE CRONEAR:
.PHONY: scores.json
scores.json: fetch
	python3 main.py > scores.json

all: clean fetch scores ranking
