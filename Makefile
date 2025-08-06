# PYTHON = python3
PYTHON = venv/bin/python3

# ESTO ES LO QUE HAY QUE CRONEAR
json: edits.json

# json a partir de la data de la db
.PHONY: edits.json
edits.json: fetch
	$(PYTHON) main.py > edits.json

# bajar de cubawiki a la db
fetch:
	$(PYTHON) request_logic.py

# graficos animados
ranking:
	$(PYTHON) ranking.py

# bye bye ocean
clean:
	rm -f CubaWeeki.db

venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

serve:
	cd race; python3 -m http.server

docker-build:
	sudo docker build -t weeki .

docker-run:
	sudo docker run --rm -it -v $$PWD:/app weeki
