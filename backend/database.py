from peewee import *
from .model import Artist, Artwork


class ArtDB:

    def add_new_artist(self, name, email):
        try:
            artist = Artist(name=name, email=email)
            artist.save()
        except IntegrityError as e:
            raise ArtStoreError(f'Error occurred while adding artist.\nMore detail: {e}\n')

    def add_new_artwork(self, name, price, artist, availability=True):
        try:
            artwork = Artwork(art_name=name, artist=artist, market_price=price, availability=availability)
            artwork.save()
        except IntegrityError as e:
            raise ArtStoreError(f'Error occurred while adding new artwork.\nMore detail: {e}\n')

    def show_all_artwork_one_artist(self, artist):

        try:
            artwork_list = Artwork.select().where(Artwork.artist == artist)
            return artwork_list
        except IntegrityError as e:
            raise ArtStoreError(f'Error occurred while querying.\nMore detail: {e}\n')

    def update_availability(self, artwork, availability):
        updated_row = Artwork.update(availability=availability).where(Artwork.art_name == artwork).execute()
        return updated_row

    def show_all_artwork(self):
        data = Artwork.select()
        return data

    def show_all_available_artwork_by_artist(self, name):
        try:
            available_artwork = Artwork.select().where((Artwork.artist == name) & (Artwork.availability == True))
            return available_artwork
        except IntegrityError as e:
            raise ArtStoreError(f'Error occurred while querying.\nMore detail: {e}\n')

    def search_artist(self, name):
        try:
            result = Artist.select().where(Artist.name == name).limit(1).dicts()
            return result
        except IntegrityError as e:
            raise ArtStoreError(f'Error occurred.\nMore detail: {e}\n')

    def search_artist_model(self, name):
        try:
            result = Artist.select().where(Artist.name == name).limit(1)
            return result
        except IntegrityError as e:
            raise ArtStoreError(f'Error occurred.\nMore detail: {e}\n')

    def show_all_artist(self):
        try:
            artists = Artist.select().dicts()
            return artists
        except ArtStoreError as e:
            print(f'Error occurred.\nMore detail: {e}\n')

    def search_art_name(self, artname, artist):
        try:
            data = Artwork.select().where(Artwork.art_name == artname, Artwork.artist == artist)
            return data
        except ArtStoreError as e:
            print(f'Error occurred.\nMore detail: {e}\n')

    def get_artist_by_art_name(self, artname):

        try:
            data = Artwork.select().where(Artwork.art_name == artname).dicts()
            return data
        except ArtStoreError as e:
            print(f'Error occurred.\nMore detail: {e}\n')

    def delete_artwork(self, artname):

        try:
            updated_row = Artwork.delete().where(Artwork.art_name == artname).execute()
            return updated_row
        except ArtStoreError as e:
            print(f'Error occurred.\nMore detail: {e}\n')

    def artist_num(self):
        num_artists = Artist.select().count()
        return num_artists

    def artwork_num(self):
        num_artists = Artwork.select().count()
        return num_artists

    def search_artwork(self, art_name):
        data = Artwork.select().where(Artwork.art_name == art_name).dicts()
        return data


class ArtStoreError(Exception):
    pass
