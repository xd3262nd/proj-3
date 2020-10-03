
class Connector:

    def __init__(self, db):
        self.db = db

    def add_artist(self, name, email):
        self.db.add_new_artist(name, email)

    def search_artist(self, name):
        result = self.db.search_artist(name)
        return result

    def add_artwork(self, name, price ,artist ,availability):
        self.db.add_new_artwork(name, price, artist, availability)

    def search_all_artwork_one_artist(self, artist):
        result = self.db.show_all_artwork_one_artist(artist)
        return result

    def search_all_artwork(self):
        result = self.db.show_all_artwork()
        return result

    def update_availability(self, artwork, availability):
        rows_updated = self.db.update_availability(artwork, availability)
        return rows_updated

    def show_all_available_artwork(self, artist):
        available_artwork = self.db.show_all_available_artwork_by_artist(artist)
        return available_artwork

    def show_all_artist(self):
        artists = self.db.show_all_artist()
        return artists

    def search_art_name(self, name, artist):
        data = self.db.search_art_name(name, artist)
        return data

    def search_artist_model(self, name):
        result = self.db.search_artist_model(name)
        return result

    def get_artist_by_art_name(self, artname):
        result = self.db.get_artist_by_art_name(artname)

        return result

    def delete_artwork(self, artname):

        updated_row = self.db.delete_artwork(artname)

        return updated_row
    def show_artist_count(self):

        num_artists = self.db.artist_num()

        return num_artists
