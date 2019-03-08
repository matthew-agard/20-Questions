import sqlite3
from time import sleep

# Questions dictionary that stores all 20 database attributes as keys and a list of binary questions
# ("Is it ... or is it not?) as values that prompt user input."""
questions = {"Insect": ["Is it a mammal, bird, reptile, or amphibian? Y/N: ",
                        "Is it an insect? Y/N: "],
             "Wild": ["Can it realistically be a household pet? Y/N: ",
                      "Is it often found in the wild? Y/N: "],
             "Land": ["Does it live in a body of water? Y/N: ",
                      "Does it live on land? Y/N: "],
             "WarmClimate": ["Does it prefer cool/cold climates? Y/N: ",
                             "Does it prefer warm/hot climates? Y/N: "],
             "Large": ["Is it smaller than an oven? Y/N: ",
                       "Is it bigger than an oven? Y/N: "],
             "Speedy": ["Is it known for being slow? Y/N: ",
                        "Is it known for being fast? Y/N: "],
             "Legs": ["Does it have less than four legs? Y/N: ",
                      "Does it have four or more legs? Y/N: "],
             "Paws": ["Does it have webbed feet or fins? Y/N: ",
                      "Does it have paws and/or claws? Y/N: "],
             "Tail": ["Is it an animal without a tail/fin? Y/N: ",
                      "Does it have a tail? Y/N: "],
             "Protrusions": ["Does it not have any protruding body parts (tusk, horn, needle)? Y/N: ",
                             "Does it have a protruding body part (tusk, horn, needle)? Y/N: "],
             "Texture": ["Is its skin bare (no fur, feathers, etc.)? Y/N: ",
                         "Does it have fur or feathers? Y/N: "],
             "Pattern": ["Is it an animal with no distinct pattern (stripes, spots)? Y/N: ",
                         "Does it have stripes or spots? Y/N: "],
             "Color": ["Is it a relatively dull color? Y/N: ",
                       "Is it colorful? Y/N: "],
             "Herbivore": ["Does it eat meat? Y/N: ",
                           "Does it only eat vegetation? Y/N: "],
             "Wings": ["Is it an animal with no wings? Y/N: ",
                       "Does it have wings? Y/N: "],
             "Flight": ["Is it unable to fly? Y/N: ",
                        "Can it fly? Y/N: "],
             "Climb": ["Is it unable to climb? Y/N: ",
                       "Does it have the ability to climb? Y/N: "],
             "Nocturnal": ["Is it mostly awake during the day? Y/N: ",
                           "Is it mostly awake during the night? Y/N: "],
             "Camouflage": ["Is it unable to camouflage? Y/N: ",
                            "Can it camouflage? Y/N: "],
             "Poisonous": ["Is it incapable of poisoning you? Y/N: ",
                           "Is it poisonous? Y/N: "]
}

# User_data list that stores user input as is provided in response to question prompts.
user_data = []

"""The following method ensures user input fits the constraints of the corresponding database attributes for purposes of
    insertion and comparison."""
def validate_user_input(response):
    while response != 'Y' and response != 'N':
        response = input("Please enter only Y or N: ").upper()
    return response


"""The following methods generates the animal in the database the user is most likely answering about. The GameCount
    score takes precedence in the selection process, following by the SelectFreq variable in the event that more than
    one instance of the animal exists in the database."""
def generate_cpu_guess():
    print("\nHmm, let me think...")
    sleep(2)
    get_animal = "SELECT Animal FROM AnimalChoice ORDER BY GameCount DESC, SelectFreq DESC LIMIT 1"
    cursor.execute(get_animal)
    guess = str(cursor.fetchone())[2:-3]
    return guess


"""The following method retrieves all animals from the database and returns them as a tuple to the function call."""
def get_all_animals():
    get_animals = "SELECT Animal FROM AnimalChoice"
    cursor.execute(get_animals)
    animals = [str(animal)[2:-3] for animal in cursor.fetchall()]
    return animals


"""The following method updates only one existing animal in the case that a user's animal of choice is already in the
    database. The animal with the best score for the game is selected and has its SelectFreq variable incremented by 1."""
def update_existing_animal(animal):
    retrieve_animal = "SELECT Animal, GameCount, SelectFreq FROM AnimalChoice WHERE Animal = '{}' " \
                      "ORDER BY GameCount DESC, SelectFreq DESC LIMIT 1".format(animal)
    cursor.execute(retrieve_animal)
    chosen_animal = str(cursor.fetchall())[1:-1]
    freq_update = "UPDATE AnimalChoice SET SelectFreq = SelectFreq + 1 WHERE " \
                  "Animal IN {0} AND GameCount IN {0} AND SelectFreq IN {0}".format(chosen_animal)
    cursor.execute(freq_update)


"""Insert a new animal instance into the database."""
def insert_new_animal(animal):
    animal_insert = "INSERT INTO AnimalChoice VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', " \
                    "'{}', '{}', 0, 1)".format(animal, user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7],
                                               user_data[8], user_data[9], user_data[10], user_data[11], user_data[12], user_data[13], user_data[14], user_data[15],
                                               user_data[16], user_data[17], user_data[18], user_data[19])
    cursor.execute(animal_insert)

# Establish connection to 20Questions database
connection = sqlite3.connect("""Your database filepath here""")
cursor = connection.cursor()

replay_game = 'Y'
while replay_game == 'Y':
    # Clear screen for start of new game
    print("\nThink of an animal for me...")
    sleep(2)

    """Generate the question that most pertains to each animal characteristic by retrieving the index to be applied to
        the nested dictionary list of the dictionary key 'category'."""
    for category in questions:
        best_question = "SELECT {} FROM AnimalChoice ORDER BY GameCount DESC, SelectFreq DESC LIMIT 1".format(category)
        cursor.execute(best_question)
        best_question = int(str(cursor.fetchone())[1:-2])

        # Retrieve user input from the generated question
        user_answer = validate_user_input(input(questions[category][best_question]).upper())

        # Assign the index of the question displayed to the user to "best_question"
        if user_answer == 'Y':
            user_answer = best_question

        # Assign the index of the question not displayed to the user to "i"
        else:
            i = 0
            if best_question == i:
                i += 1
            user_answer = i

        # Append the index of the most pertinent question associated with the animal to "user_data"
        user_data.append(user_answer)

        # Increment GameCount variable for animal where corresponding attribute value is equal to user input; primary
        # attribute used in generating CPU animal guess
        game_update = "UPDATE AnimalChoice SET GameCount = GameCount + 1 WHERE {} = '{}'".format(category, user_answer)
        cursor.execute(game_update)
        connection.commit()

    # CPU generates and presents a guess for the user to confirm or deny
    cpu_guess = generate_cpu_guess()
    user_confirm = validate_user_input(input("Is it a(n)...{}? Y/N: ".format(cpu_guess)).upper())

    # CPU guesses correctly
    if user_confirm == 'Y':
        print("I win! Thanks for playing, come again.")
        update_existing_animal(cpu_guess)

    # CPU guesses incorrectly
    else:
        # Ask user what their animal in mind was
        animal = input("You got me this time! What animal were you thinking of? ").lower()
        animals = get_all_animals()

        if animal in animals:
            # Retrieve the highest game count from the record of the animal in question
            game_count = "SELECT GameCount FROM AnimalChoice WHERE Animal = '{}' ORDER BY GameCount DESC LIMIT 1".format(animal)
            cursor.execute(game_count)
            game_count = int(str(cursor.fetchone())[1:-2])

            # Update an already-existing animal record only if its attributes are at least 75% accurate to user input.
            if game_count >= 15:
                update_existing_animal(animal)

            # Insert a new animal instance into the database.
            else:
                insert_new_animal(animal)

        else:
            insert_new_animal(animal)

    # Clear the user_data list to be used for a new instance of the game
    user_data.clear()
    reset_game = "UPDATE AnimalChoice SET GameCount = 0"
    cursor.execute(reset_game)

    # Retrieve the total number of gameplay instances in the database; based on sum of animal selections
    user_plays = "SELECT SUM(SelectFreq) FROM AnimalChoice"
    cursor.execute(user_plays)
    total_user_plays = int(str(cursor.fetchone())[1:-2])

    """The following conditional and nested for loop validate database animal records after every 30 plays. The list of all
        all animals in the database is retrieved and checked for duplicate animals. If an animal with duplicates exists, the
        instance with the highest selection frequency is selected and stored in a temporary variable. The remaining, invalid
        duplicates are then deleted from the database. This is followed by a reinsertion of the valid animal record into the
        database."""
    if total_user_plays % 30 == 0:
        animals = get_all_animals()

        for animal in animals:
            if animals.count(animal) > 1:
                get_valid_animal = "SELECT * FROM AnimalChoice WHERE Animal = '{}' ORDER BY SelectFreq DESC, GameCount DESC LIMIT 1".format(animal)
                cursor.execute(get_valid_animal)
                valid_animal = str(cursor.fetchall())[1:-1]

                delete_invalid_animals = "DELETE FROM AnimalChoice WHERE Animal = '{}'".format(animal)
                cursor.execute(delete_invalid_animals)

                insert_valid_animal = "INSERT INTO AnimalChoice VALUES {}".format(valid_animal)
                cursor.execute(insert_valid_animal)

    # Save database changes made during gameplay and close the connection
    connection.commit()

    # Ask user if they'd like to play another round of 20 Questions
    replay_game = validate_user_input(input("\nWould you like to play again? Y/N: ").upper())

# Exit game
print("You've been a worthy foe...until next time.")

# Close database connection
connection.close()