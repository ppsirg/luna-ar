PYTHON_BIN := python3.13
PORT := 8899

setup-dev:
	${PYTHON_BIN} -m venv env && . env/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

clean-dev-env:
	rm -rfv env

dev: beautify
	. env/bin/activate && python app.py

beautify:
	. env/bin/activate && black .

test-dev: beautify
	. env/bin/activate && pytest -s --full-trace