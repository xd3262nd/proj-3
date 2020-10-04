from unittest import TestCase
# order matters - swap out the test db before any of your code uses it
from backend import db_config

db_config.database_path = 'test_art_store.sqlite'

from backend.database import *


class TestArtWork(TestCase):

    def setUp(self):
        # Create a new DB
        self.art_db = ArtDB()
        # Clear all tables in DB
        Artwork.delete().execute()
        Artist.delete().execute()

    def add_sample_data(self):
        # Sample data with three artist and one artwork under each artist
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

    def test_add_artist(self):

        artist = Artist(name='Artist ABC', email='abc@gmail.com')
        artist.save()
        self.assertEqual(1, self.art_db.artist_num())

        # Test with more data
        self.add_sample_data()
        # Should return 4 artist
        self.assertEqual(4, self.art_db.artist_num())


    def test_add_duplicate_artist_model(self):
        self.add_sample_data()
        # adding example artist
        test_artist = Artist(name='Lola You', email='l_you@gmail.com')
        # Test adding artist with duplicate email address as test_artist
        duplicate_artist_email = Artist(name='Luke Yong', email='l_you@gmail.com')
        # Test adding artist with duplicate artist name as test_artist
        duplicate_artist_name = Artist(name='Lola You', email='lola_you@gmail.com')

        # Adding the example artist that will pass
        test_artist.save()

        with self.assertRaises(IntegrityError):
            duplicate_artist_email.save()
            duplicate_artist_name.save()

    def test_artwork_availability_type(self):
        # Add sample data
        self.add_sample_data()

        # Test different type of availability input type
        # Test with string type on availability
        artwork = Artwork(artist='John Doe', art_name='The Sample Art', market_price=999, availability='yes')
        self.assertRaises(TypeError, artwork.save())
        # Another string type
        artwork2 = Artwork(artist='John Doe', art_name='The Sample Art 2', market_price=999, availability='122233')
        self.assertRaises(TypeError, artwork2.save())
        # Test with integer on availability
        artwork3 = Artwork(artist='John Doe', art_name='The Sample Art 3', market_price=999, availability=0)
        self.assertRaises(TypeError, artwork3.save())

        # Test without having availability in the query
        artwork4 = Artwork(artist='John Doe', art_name='The Sample Art 4', market_price=999)
        with self.assertRaises(IntegrityError):
            artwork4.save()

    def test_add_duplicate_artwork(self):

        self.add_sample_data()
        # Add artwork with duplicate art name and duplicate artist name
        test_artwork = Artwork(art_name='Swim Along', market_price=602, artist=self.artist3.name, availability=True)
        # Add artwork with duplicate art name
        test_artwork_2 = Artwork(art_name='Swim Along', market_price=602, artist=self.artist1.name, availability=True)
        # Add a proper artwork
        test_artwork_3 = Artwork(art_name='Another Drawing', market_price=602, artist=self.artist1.name,
                                 availability=False)

        test_artwork_3.save()

        with self.assertRaises(IntegrityError):
            test_artwork.save()
            test_artwork_2.save()

    def test_add_new_artwork(self):
        self.add_sample_data()
        artwork_pt2 = Artwork(art_name='Swim Along PT2', market_price=602, artist=self.artist3.name, availability=True)
        artwork_pt2.save()
        self.assertEqual(4, self.art_db.artwork_num())

    def test_delete_existing_artwork(self):
        self.add_sample_data()
        self.art_db.delete_artwork('Sing Along')
        self.assertEqual(2, self.art_db.artwork_num())

    def test_delete_invalid_artwork(self):
        self.add_sample_data()
        # Delete an artwork that does not exist in the database
        self.assertRaises(TypeError, self.art_db.delete_artwork('Sample Artwork'))
        # Delete an artwork that does not exist in the database and store in a list
        self.assertRaises(TypeError, self.art_db.delete_artwork(['Sample Artwork']))
        # Delete an artwork that does exist in the database and store in a list
        self.art_db.delete_artwork(['Swim Along'])
        # Delete an artwork with a variable name, should be able to delete the artwork
        tmp_name = self.artwork1.art_name
        self.art_db.delete_artwork(tmp_name)

    def test_change_artwork_status(self):


        self.add_sample_data()
        # Test changing artwork availability
        artwork1_availability = self.artwork1.availability

        self.art_db.update_availability(self.artwork1.art_name, not artwork1_availability)
        data = self.art_db.search_artwork(self.artwork1.art_name)
        for row in data:
            availability = row['availability']
        self.assertEqual(not artwork1_availability, availability)

    def test_change_invalid_artwork_status(self):
        self.add_sample_data()
        # Update the availability to string
        self.assertRaises(TypeError, self.art_db.update_availability(self.artwork1.art_name, '123'))
        # Update the availability to string with true or false in it
        self.assertRaises(TypeError, self.art_db.update_availability(self.artwork1.art_name, 'true'))
        self.assertRaises(TypeError, self.art_db.update_availability(self.artwork1.art_name, 'false'))
        # Update the availability to integer with true or false in it
        self.assertRaises(TypeError, self.art_db.update_availability(self.artwork1.art_name, 1))

    def test_artwork_price(self):
        self.add_sample_data()
        # Test adding String type on price column
        artwork_test1 = Artwork(art_name='This is Arts', market_price='991', artist=self.artist1.name,
                                availability=False)
        self.assertRaises(TypeError, artwork_test1.save())
        # Test adding List type on price column
        artwork_test2 = Artwork(art_name='Art is amazing', market_price=['122'], artist=self.artist1.name,
                                availability=False)
        with self.assertRaises(InterfaceError):
            artwork_test2.save()
        artwork_test3 = Artwork(art_name='Art in Code', market_price=-122, artist=self.artist1.name, availability=False)
        self.assertRaises(TypeError, artwork_test3.save())
        # Test when adding decimals on price
        artwork_test4 = Artwork(art_name='Here it is', market_price=322.90, artist=self.artist1.name,
                                availability=False)
        artwork_test4.save()

    def test_artist_number(self):
        self.add_sample_data()
        count = self.art_db.artist_num()
        self.assertEqual(3, count)

    def test_artwork_number(self):
        self.add_sample_data()
        count = self.art_db.artwork_num()
        self.assertEqual(3, count)

    def test_empty_artwork(self):
        data = self.art_db.show_all_artwork()

        self.assertEqual(0, data.__len__())

    def test_empty_artist(self):
        data = self.art_db.show_all_artist()

        self.assertEqual(0, data.__len__())

    def test_show_artwork_by_one_artist(self):
        self.add_sample_data()
        artwork_test = Artwork(art_name='Starlight', market_price=786, artist=self.artist1.name, availability=False)
        artwork_test.save()

        data = self.art_db.show_all_artwork_one_artist(self.artist1.name)
        self.assertEqual(2, data.__len__())

    def test_get_invalid_artist(self):
        self.add_sample_data()

        self.assertEqual(0, self.art_db.search_artist('Test Artist ABC').__len__())

    def test_get_invalid_artwork(self):
        self.add_sample_data()

        self.assertEqual(0, self.art_db.search_artwork('Artwork Test').__len__())

    def test_get_available_artwork(self):

        # Add test artist and some artworks

        self.test_artist = Artist(name='John Doe', email='JD@gmail.com')
        self.test_artist.save()


        self.test_artwork_1 = Artwork(art_name='Flower in the Vase', market_price=1223, artist=self.test_artist.name,
                                      availability=False)
        self.test_artwork_2 = Artwork(art_name='Wallpaper', market_price=8273.92, artist=self.test_artist.name,
                                      availability=True)
        self.test_artwork_3 = Artwork(art_name='Sunflower Field', market_price=231.23, artist=self.test_artist.name,
                                      availability=True)
        self.test_artwork_4 = Artwork(art_name='Morning Glory', market_price=3210.20, artist=self.test_artist.name,
                                      availability=False)
        self.test_artwork_5 = Artwork(art_name='Superman Return', market_price=3210.20, artist=self.test_artist.name,
                                      availability=True)
        self.test_artwork_1.save()
        self.test_artwork_2.save()
        self.test_artwork_3.save()
        self.test_artwork_4.save()
        self.test_artwork_5.save()

        available_artwork = self.art_db.show_all_available_artwork_by_artist(self.test_artist.name)
        self.assertEqual(3, available_artwork.__len__())





