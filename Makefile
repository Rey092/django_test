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

debugger-install:
	python -m pip install django-debug-toolbar
	# 'debug_toolbar'                                    | add to the INSTALLED_APPS in settings.py
	# debug_toolbar.middleware.DebugToolbarMiddleware    | add to the MIDDLEWARE in settings.py
	# INTERNAL_IPS = [ "127.0.0.1", ]					 | create in the settings.py
	# path('__debug__/', include(debug_toolbar.urls))    | add to the urls.py in project DIR
	# import debug_toolbar                               | add to the urls.py in project DIR

run:
	python $(manage.py) runserver

kill-port:
	sudo fuser -k 8000/tcp

migrate:
	python $(manage.py) makemigrations
	python $(manage.py) migrate

check:
	python $(manage.py) check

migrations-dry:
	python $(manage.py) makemigrations --dry-run
