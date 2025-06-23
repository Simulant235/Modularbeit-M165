import json
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from pymongo.synchronous.collection import Collection as mongoCol
import time
import os


# Filepath
games_src = 'spiele.pcgames.json'
database_name = 'spiele'
collection_name = 'pcgames'

client = MongoClient('localhost', 27017) # Verbindung MongoDb
db = client[database_name]  # Wert database_name
collection = db[collection_name]  # Wert collection_name

# Mögliche abfragen
data_names = [
    'title',
    'release_date',
    'genres',
    'age_rating',
    'rating',
    'downloads'
]

sort_options = [
    'title',
    'release_date',
    'age_rating',
    'rating',
    'downloads'
]

game_template = [
    'release_date',
    'genres',
    'age_rating',
    'rating',
    'downloads'
]

def pause(mili: int):
    try:
        seconds = (mili * 3) / 1000  # Multipliziere die Zeit mit 3
        time.sleep(seconds)
    except Exception as e:
        print(f"    An error occurred: {e}")

def fill_db(collection: mongoCol):
    db = read_json_db(games_src)
    collection.insert_many(db)

def read_json_db(json_path: str):
    with open(games_src) as f:
        return json.load(f)

def initiate_mongo_db(db_name: str, col_name: str):
    db_exist = False
    col_exist = False

    print('''
                                                                                                 
                                                                                                 
                                                                                                 
                 =%%                                                                             
               =*==%@.                                                                           
             :#+-.:##@@           @@@@@@ @@@    .@@@@  @@@@@@    @-@@   /@@@@                    
            ***=-::#**%@:          @:  @@   @  @@   @@  @@  -@  @   @  @@   @@                   
           %++=-=::#*++#@+         @   %#   @  @@   +@  @@   @   @@%   @@    @                   
          #*+===-::#*+++*@-       @@@  @@  @@@  @@@@@  *@@. @@@  @@@@\  @@@@@                    
         +*+=-==-::##****#@.                                         @@                          
         ##++====-:#*+++**#@                                    @@#*@.                           
        +#+=+=+=-::#*+++++*@-                                                                    
        *#==+===+-:##******#@                                                                    
        ##++*+===-:#**+*+***@     .@@@@@@@@@@@@@@@@@       .@@@@@@@@@@@@@@.                      
        #*+++====-:#*******+@         @*@         @@@@         @*@      *@@@                     
        #*+=+++===:#*+*****+@         @*@           @@@#       @#@       @+@                     
        ##++++++=-:##+**+**#@         @*@            @#@       @#@       @@@                     
        =%+++++==-:##******%%         @*@            @*@@      @#*      @@                       
         @#++*+++-:##*****%@          @*@            *##@      @#@@@@@@@@@@                      
          %*+++++=:#******@*          @*@            @#@@      @**       @@@@                    
           @*+++=--#****#@%           @*@            @#@.      @#@        @#%@                   
            @#*++=+%#**#@%            @*@            @@@       @#@        =#@@                   
             #%#+=-#*#@@*             @+@          #@@:       .@*@        @@@                    
               %@#.@@@@               @%@#       @@@          *@%@      .@@#                     
                 #=-@              @@@@%@@@@@@@@%          =@@@@%@@@@@@@+                        
                  .                                                                              
                  .                                                                              
                                                                                                 
                                                                                                 
''')

    pause(750)
    print("    Connecting to MongoDB...")
    pause(250)
    print('\n    Connecting to Database "spiele" ...')
    pause(100)
    if db_name in client.list_database_names():
        db_exist = True
    
    database = client[db_name]#                                    variable collection

    pause(100)
    if col_name in database.list_collection_names():
        col_exist = True
    print('\n    Succsesfully connected to "spiele"!')
    pause(100)
    collection = database[col_name]#                                    variable collection

    return collection, [db_exist, col_exist]

def main():
    os.system('cls')
    # MongoDB-Verbindung und Sammlung initialisieren
    collection, exist = initiate_mongo_db(database_name, collection_name)
    if not exist[0]:
        fill_db(collection)
        
    # Direkt zum Hauptmenü
    main_menu(collection)

def main_menu(collection):
    while True:
        # Hauptmenü
        print("\n    Menu:")
        print("    1 - Add a new game")
        print("    2 - Update an existing game")
        print("    3 - Delete a game")
        print("    4 - Search for a game")
        print("    5 - Display all games")
        print("    6 - Exit")

        choice = input("    Enter your choice: ").strip()

        if choice == '1':
            add_game(collection)
        elif choice == '2':
            update_game(collection)
        elif choice == '3':
            delete_game(collection)
        elif choice == '4':
            search_game(collection)
        elif choice == '5':
            display_games(collection)
        elif choice == '6':
            print("    Exiting the program...")
            break
        else:
            print("    Invalid choice! Please enter a number between 1 and 6.")

def add_game(collection: mongoCol):
    new_game = {}

    # Zuerst den Titel abfragen
    title = input("    Enter the title of the game: ").strip()
    if not title:  # Prüfen, ob der Titel eingegeben wurde
        print("    Title cannot be empty. Aborting...\n")
        pause(175)
        return

    new_game['title'] = title  # Den Titel zum Spiel hinzufügen

    # Abfrage, welche Felder hinzugefügt werden sollen
    fields_prompt = '''
Please choose one of the following fields to add to the new game. 
Enter the number of your choice, or press Enter to finish adding fields.

0 - Release Date
1 - Genres
2 - Age Rating
3 - Rating
4 - Downloads
'''

    while True:
        print(fields_prompt)
        field_choice = input("    Enter your choice: ").strip()

        # Wenn der Benutzer fertig ist, brechen wir die Schleife ab
        if field_choice == '':
            break

        # Prüfen, ob die Eingabe eine gültige Zahl ist und im gültigen Bereich liegt
        if field_choice.isnumeric() and int(field_choice) in range(len(game_template)):
            field_name = game_template[int(field_choice)]  # Den Feldnamen abrufen
            value = input(f"    Enter value for {field_name}: ").strip()

            # Besondere Behandlung für das Feld 'downloads', da dies eine Zahl ist
            if field_name in ['downloads', 'release_date', 'age_rating', 'rating']:
                if value.isdigit():
                    new_game[field_name] = int(value)
                else:
                    print("    Invalid input! Please enter a numeric input.")
            else:
                new_game[field_name] = value.replace(' ', '').split(',')
        else:
            print("    Invalid input! Please enter a number between 0 and 4 or press Enter to finish.")

    # Spiel in die MongoDB-Sammlung einfügen
    collection.insert_one(new_game)

    print("\n    Game added successfully with the following fields:")
    for key, value in new_game.items():
        print(f"{key.capitalize()}: {value}")
    pause(250)

def update_game(collection):
        game_title = input("    Enter the title of the game you want to update: ").strip()
        game = collection.find_one({'title': game_title})

        if game:
            print("    Game found! Please enter the new details (leave blank to keep current values).")
            updated_game = {}
            for field in game_template:
                while True:
                    value = input(f"    Enter new {field} (current: {game[field]}): ").strip()

                    if field in ['downloads', 'release_date', 'age_rating', 'rating']:
                        if value.isdigit():
                            updated_game[field] = int(value)
                            break
                        else:
                            print("    Invalid input! Please enter a numeric input.")
                            continue
                    else:
                        updated_game[field] = value.replace(' ', '').split(',')
                        break

            collection.update_one({'title': game_title}, {"$set": updated_game})
            print("    Game updated successfully!\n")
        else:
            print(f"    Game '{game_title}' not found!\n")
        pause(175)

def delete_game(collection: mongoCol):
        game_title = input("    Enter the title of the game you want to delete: ").strip()

        # Suche nach dem Spiel
        game = collection.find_one({'title': game_title})

        if game:
            confirm = input(f"    Are you sure you want to delete '{game_title}'? (y/n): ").strip().lower()

            if confirm == 'y':
                # Lösche das Spiel
                collection.delete_one({'title': game_title})
                print(f"    Game '{game_title}' has been deleted successfully!")
            elif confirm == 'n':
                print("    Deletion aborted.")
            else:
                print("Invalid choice! Deletion aborted.")

        else:
            print(f"    Game '{game_title}' not found!")

        pause(175)

def search_game(collection: mongoCol):
        os.system('cls')

        # 1. Abfrage, Auswahl des Aggregates
        data_type_prompt = f'''
    Please choose one of the following categories to search by

    0 - Title
    1 - Release Date
    2 - Genres
    3 - Age Rating
    4 - Rating
    5 - Downloads

    Enter the number of your choice: '''

        while True:
            input_data_type = input(data_type_prompt)

            # Muss Nummer sein und checkt ob eine zahl zwischen 0 - 5
            if input_data_type.isnumeric() and int(input_data_type) in range(6):
                input_data_type = int(input_data_type)
                break
            else:
                print("    Invalid input! Please enter a number between 0 and 5 or type 'exit' to quit.\n")

        # 2. Abfrage der Werte
        input_data_search = input('\n    Input what kind of value you are searching for: ')

        # sorgt dafür, wenn die Angabe eine Zahl ist, dass sie als Int gespeichert wird und sonst als String
        if input_data_search.isnumeric():
            input_data_search = int(input_data_search)

        os.system('cls')

        sort_order_prompt = '''
    How would you like to sort the results?

    0 - Sort by Title
    1 - Sort by Release Date 
    2 - Sort by Age Rating 
    3 - Sort by Rating 
    4 - Sort by Downloads

    Or Type "skip" to skip sorting.

    Enter your choice: '''

        # Get the sort order from the user
        input_sort_choice = input(sort_order_prompt).strip()

        # Determine the sort field and order based on user input
        sort_field = None
        sort_order = None

        if input_sort_choice.isnumeric() and int(input_sort_choice) in range(5):  # Validate number input
            input_sort_choice = int(input_sort_choice)
            sort_field = sort_options[input_sort_choice]  # Get the field
            order_input = input("\n    Enter 'asc' for ascending or 'desc' for descending: ").strip().lower()

            if order_input == "desc":
                sort_order = DESCENDING
            elif order_input == "asc":
                sort_order = ASCENDING
            else:
                print("\n    Invalid input! Skipping sorting.")
                pause(250)
        else:
            if input_sort_choice.lower() == 'skip':
                print("\n    Skipping sorting.")
            else:
                print("\n    Invalid input! Skipping sorting.")
            pause(250)

        # For querying
        query = {data_names[input_data_type]: input_data_search}

        os.system('cls')

        # Abfrage, welche Aggregate angezeigt werden sollen
        while True:
            display_prompt = '''
    Which fields would you like to display? (Enter numbers separated by commas)

    0 - Title
    1 - Release Date
    2 - Genres 
    3 - Age Rating 
    4 - Rating
    5 - Downloads

    Example: 0,1,3

    Enter your choice: '''

            display_choice = input(display_prompt).split(',')

            for choice in display_choice:
                if not choice.strip().isdigit() or int(choice.strip()) > 5:
                    print("    Invalid input detected!")
                    pause(750)
                    os.system('cls')
                    continue
            break

        display_fields = [data_names[int(choice.strip())] for choice in display_choice if choice.strip().isdigit()]
        os.system('cls')
        print('\n    Results:\n')
        pause(100)

        # Ergebnisse ausgeben, je nachdem ob Sortierung gewählt wurde
        if sort_field:
            for game in collection.find(query).sort(sort_field, sort_order):  # Verwende "collection" statt "games_db"
                for field in display_fields:
                    print(f'    {field.replace("_", " ").capitalize()}:', game.get(field, 'N/A'))
                print('')
                pause(100)
        else:
            for game in collection.find(query):  # Verwende "collection" statt "games_db"
                for field in display_fields:
                    print(f'    {field.replace("_", " ").capitalize()}:', game.get(field, 'N/A'))
                print('')
                pause(100)

def display_games(collection: mongoCol):
        os.system('cls')
        # Zähle die Anzahl der Spiele in der Sammlung
        game_count = collection.count_documents({})  # Zählt alle Dokumente in der Sammlung

        if game_count == 0:
            print("    No games found in the database.")
            return
        
        # Abrufen aller Spiele aus der Sammlung
        all_games = collection.find()
        
        game_titles = []
        games = []
        for game in all_games:
            game_titles.append(dict(game.items())['title'])
            games.append(game)

        print(f"\n    There are '{game_count}' in the database!")
        pause(300)
        print("    Displaying all games in the collection:\n")
        pause(300)
        printing = [f' {ind + 1}: {game_titles[ind]}' for ind in range(game_count)]
        print('\n'.join(printing) + '\n')

        while True:
            pause(300)
            continue_display = input('    Enter index of game to access details (press enter to see full list / enter 0 to go to main menu): ')
            os.system('cls')
            if continue_display.lower() == '':
                print('\n'.join(printing) + '\n')
                continue
            elif continue_display.isnumeric():
                continue_display = int(continue_display) - 1
                if continue_display == -1:
                    return
                elif continue_display in range(game_count):
                    for field, value in list(games[continue_display].items())[1:]:
                        print(f'    {field.replace("_", " ").capitalize()}: {value}')
                    print('   ','-' * 40)  # Trennt die einzelnen Spiele
                    continue

            print("    Invalid input!")


if __name__ == "__main__":
    main()
