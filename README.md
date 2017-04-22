# track-scraper
An 8tracks favourite track scraper

## To Use
Clone repository

Install Python 3, mongoengine, mongodb, and django

### Start MongoDB

Run `"C:\Program Files\MongoDB\Server\3.4\bin\mongod.exe"` on commandline (with quotes)

Run `"C:\Program Files\MongoDB\Server\3.4\bin\mongo.exe"` in anothor commandline window (with quotes)

Run `use manage_music_db` in Mongo Shell

Run `db.myCollection.insertOne( { x: 1} );` in Mongo Shell (insertion makes the database, so this might not be a necessary step)

Quit Mongo Shell with `CTRL+C`

Leave mongod running

### Start track_scraper_app

Run `python manage.py runserver` in `track-scraper\track_scraper_app` (you should be able to see `manage.py` in the folder)

(Migrate schema changes if necessary)
