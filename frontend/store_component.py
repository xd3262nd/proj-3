def generate_menu():
    print('1. Add New Artist\n2. Add New Artwork\n3. Update Artwork Availability\n4. List All Artworks by an '
          'Artist (Available and Sold)\n5. Display all Available Artwork by an Artist\n6. Delete an Artwork\n7. '
          'Show All Artwork in Library\n8. Show All Artist in Library\nQ. Quit the Program\n ')

    user_selection = get_selection()

    if user_selection is None:
        print('\n\nThanks for using the program')
        running = False
        return None
    else:
        return user_selection


def get_selection():
    selection = input('Enter one of the menu option or \'q\' to quit the program. ')

    if selection.upper() == 'Q':
        return None

    try:
        selection_int = int(selection)
        if selection_int > 8 or selection_int < 0:
            print(
                'Invalid option. Please enter one of the menu option, from number 1 to 7 or \'q\' to quit the '
                'program.\n ')
            return get_selection()
        return selection_int
    except ValueError:
        print('Input Error. Please enter one of the menu option, from number 1 to 7 or \'q\' to quit the program.\n')
        return get_selection()



