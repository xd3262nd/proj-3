from unittest import TestCase
from peewee import *

from backend.model import Artist, Artwork
from backend import db_config

from backend.database import *

db_config.database_path = 'test_art_store.sqlite'
test_db = SqliteDatabase(db_config.database_path)
test_tables = [Artist, Artwork]


class TestArtWork(TestCase):

    def setUp(self):
        test_db.bind(test_tables, bind_refs=False, bind_backrefs=False)
        # Create a new DB
        self.art_db = ArtDB()
        test_db.create_tables(test_tables)
        Artist.database = test_db
        Artwork.database = test_db
        Artwork.delete().execute()
        Artist.delete().execute()

    def add_sample_data(self):
        self.artist1 = Artist(name='John Doe', email='JD@gmail.com')
        self.artist2 = Artist(name='Kim Doe', email='kim_doe@gmail.com')
        self.artist3 = Artist(name='Ryan Doe', email='r_doe@gmail.com')
        self.artist1.save()
        self.artist2.save()
        self.artist3.save()

    def test_add_artist(self):
        artist = Artist(name='Artist ABC', email='artistabc@gmail.com')
        artist.save()
        self.assertEqual(1, self.art_db.artist_num())

    def test_add_artist_not_unique(self):
        self.add_sample_data()

        artist4 = Artist(name='Lola You', email='l_you@gmail.com')
        artist5 = Artist(name='Luke Yong', email='l_you@gmail.com')
        artist6 = Artist(name='Lola You', email='lola_you@gmail.com')

        with self.assertRaises(IntegrityError):
            artist4.save()
            artist5.save()
            artist6.save()

    def test_artwork_availability(self):
        self.add_sample_data()
        artwork = Artwork(artist='John Doe', art_name='The Sample Art', market_price=999, availability='123')
        self.assertRaises(AssertionError, artwork.save())

