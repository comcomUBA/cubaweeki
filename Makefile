# ESTO ES LO QUE HAY QUE CRONEAR
json: edits.json

# json a partir de la data de la db
.PHONY: edits.json
edits.json: fetch
	python3 main.py > edits.json

# bajar de cubawiki a la db
fetch:
	python3 request_logic.py

# graficos animados
ranking:
	python3 ranking.py

# bye bye ocean
clean:
	rm -f CubaWeeki.db
