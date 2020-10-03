from unittest import TestCase
# from peewee import *

# order matters - swap out the test db before any of your code uses it 
from backend import db_config
db_config.database_path = 'test_art_store.sqlite'  # this file will be created in the root directory of your project

import os   # or use this 
db_config.database_path = os.path.join('test', 'test_art_store.sqlite') # if you want the test db in the test directory 

from backend.model import Artist, Artwork

from backend.database import *

# test_db = SqliteDatabase(db_config.database_path)
# test_tables = [Artist, Artwork]


class TestArtWork(TestCase):

    def setUp(self):
        # Artist.database = test_db
        # Artwork.database = test_db
        # test_db.bind(test_tables, bind_refs=False, bind_backrefs=False)
        # Create a new DB
        self.art_db = ArtDB()
        # test_db.create_tables(test_tables)

        Artwork.delete().execute()
        Artist.delete().execute()

    def add_sample_data(self):
        self.artist1 = Artist(name='John Doe', email='JD@gmail.com')
        self.artist2 = Artist(name='Kim Doe', email='kim_doe@gmail.com')
        self.artist3 = Artist(name='Ryan Doe', email='r_doe@gmail.com')
        self.artist1.save()
        self.artist2.save()
        self.artist3.save()

        self.artwork1 = Artwork(art_name='Sing Along', market_price=300, artist=self.artist1.name, availability=True)
        self.artwork2 = Artwork(art_name='Paint Along', market_price=10, artist=self.artist2.name, availability=False)
        self.artwork3 = Artwork(art_name='Swim Along', market_price=602, artist=self.artist3.name, availability=True)

        self.artwork1.save()
        self.artwork2.save()
        self.artwork3.save()


    def test_artwork_num(self):
        # start with empty database 
        Artwork(art_name='Sing Along', market_price=300, artist='test', availability=True).save()
        self.assertEqual(1, self.art_db.artwork_num())
        
        Artwork(art_name='Walk Along', market_price=300, artist='test2', availability=True).save()
        self.assertEqual(2, self.art_db.artwork_num())
        
        # look at artwork_num - why is this test failing? Does this help fix the other failing tests?


    def test_add_artist(self):
        artist = Artist(name='Artist ABC', email='abc@gmail.com')
        artist.save()
        self.assertEqual(1, self.art_db.artist_num())

    def test_add_duplicate_artist_model(self):
        self.add_sample_data()

        artist4 = Artist(name='Lola You', email='l_you@gmail.com')
        artist5 = Artist(name='Luke Yong', email='l_you@gmail.com')
        artist6 = Artist(name='Lola You', email='lola_you@gmail.com')

        with self.assertRaises(IntegrityError):   
            artist4.save()
            artist5.save()   # Which one of these save calls do you expect to error? This test could use some more documentation
            artist6.save()

            

    def test_artwork_availability_type(self):
        self.add_sample_data()
        artwork = Artwork(artist='John Doe', art_name='The Sample Art', market_price=999, availability='yes')
        self.assertRaises(TypeError, artwork.save())
        artwork2 = Artwork(artist='John Doe', art_name='The Sample Art 2', market_price=999, availability='122233')
        self.assertRaises(TypeError, artwork2.save())
        artwork3 = Artwork(artist='John Doe', art_name='The Sample Art 3', market_price=999, availability=0)
        self.assertRaises(TypeError, artwork3.save())

        artwork4 = Artwork(artist='John Doe', art_name='The Sample Art 4', market_price=999)
        with self.assertRaises(IntegrityError):
            artwork4.save()

    def test_add_duplicate_artwork(self):
        self.add_sample_data()
        test_artwork = Artwork(art_name='Swim Along', market_price=602, artist=self.artist3.name, availability=True)

        with self.assertRaises(IntegrityError):
            test_artwork.save()

    def test_add_new_artwork(self):
        self.add_sample_data()
        artwork_pt2 = Artwork(art_name='Swim Along PT2', market_price=602, artist=self.artist3.name, availability=True)
        artwork_pt2.save()
        self.assertEqual(4, self.art_db.artwork_num())

    def test_delete_existing_artwork(self):
        self.add_sample_data()
        self.art_db.delete_artwork('Sing Along')
        self.assertEqual(2, self.art_db.artwork_num())

    def test_change_artwork_status(self):
        self.add_sample_data()

