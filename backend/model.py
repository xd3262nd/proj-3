from peewee import *
from backend import db_config

db = SqliteDatabase(db_config.database_path)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Artist(BaseModel):
    name = CharField(unique=True)
    email = CharField(unique=True)

    class Meta:
        database = db

    def __str__(self):
        return f'Artist ID: {self.id}, Name: {self.name}, Email: {self.email}'


class Artwork(Model):
    art_name = CharField(unique=True)
    artist = ForeignKeyField(model=Artist, field=Artist.name, backref='artwork')
    market_price = DecimalField(10, 2)
    availability = BooleanField()

    class Meta:
        database = db

    def __str__(self):
        return f'Artist: {self.artist.name} \n\tArtwork Name: {self.art_name}\n\tPrice: ${self.market_price}\n' \
               f'\tAvailability: {self.availability} '


db.create_tables([Artist, Artwork])
