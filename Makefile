manage.py = homework5/manage.py

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

flake8-install:
	pip install flake8
	pip install flake8-import-order # сортировку импортов
	pip install flake8-docstrings # доки есть и правильно оформлены
	pip install flake8-builtins # что в коде проекта нет переменных с именем из списка встроенных имён
	pip install flake8-quotes # проверять кавычки

	# ставим гит-хук
	flake8 --install-hook git
	git config --bool flake8.strict true

run:
	python $(manage.py) runserver

kill-port:
	sudo fuser -k 8000/tcp

migrate:
	python $(manage.py) makemigrations
	python $(manage.py) migrate