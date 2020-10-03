from .store_component import generate_menu
from .input_validatation import *

VALIDATOR = SimpleValidator()


class Store:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def main_page(self):

        print('Welcome to the Art Store')

        while True:
            selection = generate_menu()

            if selection == 1:
                add_artist(self)
            elif selection == 2:
                add_artwork(self)
            elif selection == 3:
                update_artwork_availability(self)
            elif selection == 4:
                show_all_artwork_by_artist(self)
            elif selection == 5:
                display_available_artwork_by_artist(self)
            elif selection == 6:
                delete_artwork(self)
            elif selection == 7:
                show_all_artwork(self)
            elif selection == 8:
                show_all_artist(self)

            elif selection is None:
                break

def add_artist(self, name=''):
    if name == '':
        name = input('What is the artist name?\t\t')

        validated_name = validate_name(name)

        is_existing = search_artist(self, validated_name)

        if is_existing is None:
            email = input(f'What is the email address for {validated_name}?\t\t')
            validated_email = validate_email_address(email)

            try:
                self.db_connection.add_artist(validated_name, validated_email)
                data = search_artist(self, validated_name)
                print('Artist added.\nInformation:\n\t')
                print(f'{data}\n')
            except Exception as e:
                print(f'Error in adding {validated_name}. More detail: {e}')
        else:
            print(f'{validated_name} is already in the system. Please try to add another artist.')


def add_artwork(self):
    # name, price, artist, availability = True
    artist_name = input('What is the artist name?\t\t')
    validated_artist_name = validate_name(artist_name)
    is_existing = search_artist(self, validated_artist_name)

    # When the artist is not in the system
    if is_existing is None:
        print(f'{artist_name} is not in the system yet.')
        data = self.db_connection.show_all_artist()
        # When there is some artist name in the system
        if data.exists():
            print('Please re-enter another artist name from the artist list below')
            print('Available Artist Name:')
            for row in data:
                print(f"\t{row['name']}")
            add_artwork(self)
        else:
            # Prompt the user to add more artist in the system before add new artwork
            print('Please add more data in the system beforehand.')
            add_artist(self)
    # When the artist is in the system
    else:
        artwork_name = input('What is the name of the artwork?\t\t')
        validated_art_name = validate_artname(artwork_name)
        artwork_result = self.db_connection.search_art_name(validated_art_name, is_existing['name'])

        if artwork_result.exists():
            print(f"Error.{is_existing['name']}\'s {validated_art_name} is already in the system.")
        else:
            price = int(input(f'What is the price for {validated_art_name}?\t\t'))
            availability = input(f'Is this {validated_art_name} still available? (yes/no)')
            validated_price = validate_price(price)
            validated_availability = validate_availability(availability)

            # Add new artwork
            try:
                self.db_connection.add_artwork(validated_art_name, validated_price, validated_artist_name,
                                               validated_availability)
                print(f'Added {validated_art_name} to the system!')
                artwork_result = self.db_connection.search_art_name(validated_art_name, is_existing['name'])
                for i in artwork_result:
                    print(i)
                print()
            except Exception as e:
                print(f'Error in adding {validated_art_name}. More detail: {e}')


# Artwork (available and not available)
def show_all_artwork_by_artist(self):
    name = input('What is the artist name?\t\t')
    validated_name = validate_name(name)
    is_existing = search_artist(self, validated_name)

    if is_existing is not None:
        try:
            data = self.db_connection.search_all_artwork_one_artist(validated_name)
            for row in data:
                print(row)
            print()
        except Exception as e:
            print(f'Error in searching for {validated_name}. More detail: {e}')
    else:
        print('Invalid Artist Name. Please refer to the artist list below and re-enter a valid artist name.')
        show_all_artist(self)
        show_all_artwork_by_artist(self)



def display_available_artwork_by_artist(self):
    name = input('What is the artist name?\t\t')
    validated_name = validate_name(name)
    is_existing = search_artist(self, validated_name)

    if is_existing is not None:
        try:
            data = self.db_connection.show_all_available_artwork(validated_name)
            for row in data:
                print(row)
            print()
        except Exception as e:
            print(f'Error in searching for {validated_name}. More detail: {e}')
    else:
        print('Invalid Artist Name. Please refer to the artist list below and re-enter a valid artist name.')
        show_all_artist(self)
        display_available_artwork_by_artist(self)


def update_artwork_availability(self):
    artist_name = input('What is the artist name you are trying to update their artwork from?\t\t')
    validated_name = validate_name(artist_name)
    is_existing = search_artist(self, validated_name)

    artwork_list = list()

    if is_existing is not None:
        try:
            data = self.db_connection.search_all_artwork_one_artist(validated_name)
            print(f'Here is a list of artwork from {validated_name} and the art work availability')
            for row in data:
                if row.availability:
                    availability = 'Available'
                else:
                    availability = 'Not Available'
                print(f'ArtWork Name: {row.art_name}\tAvailability: {availability}')
                artwork_list.append(row.art_name.lower())
            print()
            artwork_name = input('What is artwork name you wish to update the availability?\t\t')
            while artwork_name.lower() not in artwork_list:
                artwork_name = input(f'Invalid input. Please enter the artwork by {validated_name} only.\t\t')

            tmp_data = self.db_connection.search_art_name(artwork_name, validated_name)
            art_availability = bool()
            for row in tmp_data:
                art_availability = row.availability

            if art_availability:
                art_availability = False
            elif not art_availability:
                art_availability = True

            row_updated = self.db_connection.update_availability(artwork_name, art_availability)

            if row_updated == 0:
                print('Error occurred while updating the artwork. ')
            else:
                print('Successfully updated the artwork availability')

            data = self.db_connection.search_art_name(artwork_name, validated_name)
            for row in data:
                print(row)
            print()
        except Exception as e:
            print(f'Error in searching for {validated_name}. More detail: {e}')
    else:
        print('Sorry the artist you have entered is not valid. Please refer to the artist name list below.')
        show_all_artist(self)

        update_artwork_availability(self)



def delete_artwork(self):
    artwork_name = input('What is the artwork that you are trying to update their artwork from?\t\t')
    validated_art_name = validate_name(artwork_name)
    result = self.db_connection.get_artist_by_art_name(validated_art_name)

    if result.exists() is None:
        print(f'The {validated_art_name} is not in the system yet. Please try again later.')
        return

    data = self.db_connection.search_art_name(self, validated_art_name, result['artist'])
    for row in data:
        print(row)

    decision = input(f'Do you still wish to proceed and delete {validated_art_name}? (yes/no)  ')
    while True:
        if decision.lower() == 'yes':
            row_updated = self.db_connection.delete_artwork(validated_art_name)
            if row_updated == 0:
                print(f'Error occurred. Unable to delete {validated_art_name} from the system.')
            else:
                print(f'Successfully deleted the {validated_art_name} from the system')
        elif decision.lower() == 'no':
            print('Cancelling request.')
            break
        else:
            decision = input(f'Invalid input. Please enter \'yes\' or \'no\' only.    ')


def show_all_artwork(self):
    results = self.db_connection.search_all_artwork()

    for data in results:
        print(data)
        print('---------------------------------------')

    print()


def show_all_artist(self):
    results = self.db_connection.show_all_artist()

    for data in results:
        print(data)
        print('**********************************')

    print()


def search_artist(self, name):
    data = self.db_connection.search_artist(name)

    if not data.exists():
        return None
    else:
        for row in data:
            return row


def get_artist_model(self, name):
    data = self.db_connection.search_artist_model(name)

    if not data.exists():
        return None
    else:
        return data
