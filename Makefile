venv/bin/python:
	virtualenv --python=python3 venv
	venv/bin/pip install -r requirements.txt

run: venv/bin/python
	venv/bin/python app.py

test: venv/bin/python
	venv/bin/python app.py &
	sleep 1 # give app a second to startup
	-venv/bin/python test_client.py
	pkill -in python # hope that the newest python process is the app

clean:
	rm -rf venv
	rm -f *.db
	rm -f *.pyc
	rm -rf __pycache__/
