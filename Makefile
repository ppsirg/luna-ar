PYTHON_BIN := python3
PORT := 8899

setup-dev:
	${PYTHON_BIN} -m venv env && . env/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

dev: beautify
	. env/bin/activate && python -m http.server ${PORT} --bind 0.0.0.0 -d ./front

beautify:
	. env/bin/activate && black .

test-dev: beautify
	. env/bin/activate && pytest -s --full-trace