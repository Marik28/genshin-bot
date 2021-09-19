install:
	pip install -U pip
	pip install -r requirements.txt

run:
	cd src; python -m genshin_bot

create-db:
	cd src; python -m genshin_bot.scripts.create_db

drop-db:
	rm db.sqlite3

insert-data:
	cd src; python -m genshin_bot.scripts.insert_data $(file)

test:
	export PYTHONPATH=$$(pwd)/src; pytest $(target) -s

parse-html:
	cd src; python -m genshin_bot.scripts.parse_html $(file)

download-characters-info:
	cd src; python -m genshin_bot.scripts.download_characters_info

dump:
	sqlite3 db.sqlite3 .dump > dump-$$(date "+%d-%m-%y_%H-%M-%S").sql
	echo "Дамп БД успешно создан"

restore:
	sqlite3 db.sqlite3 < $(file)
	echo "БД восстановлена из дампа"

admin-run-dev:
	cd src; python -m admin.main