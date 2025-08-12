# PYTHON = python3
PYTHON = venv/bin/python3

# ESTO ES LO QUE HAY QUE CRONEAR
json: race/edits.json race/teams.json

# json a partir de la data de la db
.PHONY: race/edits.json
race/edits.json: fetch
	$(PYTHON) main.py > race/edits.json

.PHONY: race/edits.json
race/teams.json: fetch
	$(PYTHON) main_teams.py > race/teams.json

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
	sudo docker run --rm -v $$PWD:/app weeki
