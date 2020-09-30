# About data testing - whether can do add, update, delete & Check constraints & can I say if an artwork no artist &
# validation empty data or weird data

from backend.database import ArtDB
from frontend import store, connection


def main():
    # Create a new DB
    art_db = ArtDB()
    # Connect the DB with a connector
    art_connector = connection.Connector(art_db)
    # Open a new Store
    art_store = store.Store(art_connector)
    # Start Store main page
    art_store.main_page()


if __name__ == '__main__':
    main()
