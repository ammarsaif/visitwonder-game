import geopy.distance
import queries.insert
import queries.select
import queries.update

destinations = {
    1: "Parthenon",
    2: "Easter Island",
    3: "Taj Mahal",
    4: "Colosseum",
    5: "Angkor",
    6: "Teotihuacan",
    7: "Petra",
    8: "Machu Picchu",
    9: "Great Wall of China",
    10: "Pyramids of Giza",
    11: "Stonehenge",
    12: "Hagia Sophia",
    13: "Chichen Itza",
    14: "Easter Islands",
    15: "Persepolis",
    16: "The Mezquita of Córdoba"
}


def start_game():
    want_to_play = input('Would you like to play a game? (Type yes OR no): ')
    return want_to_play


def input_player_email():
    player_email = input('Please, type in your email: ')
    return player_email


def input_player_name():
    input('Please, type in your name : ')
    return input('Please, type in your name : ')


def select_difficulty():
    input("Difficulty level, select easy, medium, or hard: ")


def input_destination():
    num_destination = int(input('Please, choose a number from the available destinations: '))
    return num_destination


def display_destinations(locations, chose_destination):
    print("Available Destinations:")
    new_locations = {}

    for num, destination in locations.items():
        if num != chose_destination:
            new_locations[num] = destination
            print(f"{num}: {destination}")

    return new_locations


def get_existing_player_info():
    existing_player = queries.select.select('email', 'user', f"email='{player_email}'")

    if existing_player:
        return existing_player  # Returning the player information
    else:
        return None  # Player not found


def insert_player_data(player_email, player_name, user_location):
    queries.insert.insert('user', f"email, player_name, location",
                          f"'{player_email}', '{player_name}', '{user_location}'")


def existing_player(player_email):
    queries.select.select('co2_consumed', 'user', f"email='{player_email}'")


def set_difficulty(difficulty, player_email):
    queries.update.update('user', 'co2_budget = %s', 'email = %s', (difficulty, player_email))


def get_location(serial_num):
    return queries.select.select('latitude_deg, longitude_deg', 'airport', f"serial_num='{serial_num}'")

def set_difficulty(difficulty, player_email):
    update.update_difficulty(difficulty, player_email)


def update_co2_consumed(co2_consumed_by_player, player_email):
    queries.update.update('user', f"co2_consumed={co2_consumed_by_player}", f"email='{player_email}'")


def calculate_distance(location_1, location_2):
    return geopy.distance.distance(location_1, location_2).km


def run_game(player_email, difficulty, game_win_threshold):
    while player_email is not None and (player_email[0] <= difficulty and game_win_threshold):
        existing_player(player_email)

        next_destination = input_destination()
        updated_destinations = display_destinations(destinations, next_destination)

        chosen_location = get_location(next_destination)
        current_location = chosen_location
        print(f"Your current location is: {destinations.get(next_destination)}")

        update_new_destination = update_new_destination(chosen_location, player_email)
        destinations = updated_destinations

        distance_in_kilometer = calculate_distance(start_location, chosen_location)
        co2_consumed_by_player = int(distance_in_kilometer * 0.2) + int(player_email[0])

        print(f"CO2 consumed: {co2_consumed_by_player}")

        update_co2_consumed(co2_consumed_by_player, player_email)

        num_visited_destinations += 1
        print(f"Number of visited Destinations: {num_visited_destinations}")

        if num_visited_destinations >= game_win_threshold:
            print("You have won the game")
            exit()

        if co2_consumed_by_player > difficulty:
            print("You lost the game the game!")
            exit()

# Default values
default_location = "Helsinki"
default_location_coordinates = '60.3172, 24.963301'
start_location = default_location_coordinates
user_location = default_location
current_location = None
player_name = None
num_visited_destinations = 0

# Game difficulty
difficulty_easy = 10000
difficulty_medium = 12000
difficulty_hard = 16000
game_win_easy = 7
game_win_medium = 10
game_win_hard = 14
difficulty = None
game_win_threshold = None

start_game()

if start_game().lower() == 'yes':

    player_email = input_player_email()
    existing_player = get_existing_player_info()

    if existing_player is None:
        player_name = input_player_name()
        insert_player_data(player_email, player_name, user_location)

    existing_player = existing_player(player_email)

    select_difficulty()
    if select_difficulty.lower() == "easy":
        difficulty = difficulty_easy
        set_difficulty(difficulty, player_email)
        game_win_threshold = game_win_easy
    elif select_difficulty.lower() == "medium":
        difficulty = difficulty_medium
        set_difficulty(difficulty, player_email)
        game_win_threshold = game_win_medium
    elif select_difficulty == "hard":
        difficulty = difficulty_hard
        set_difficulty(difficulty, player_email)
        game_win_threshold = game_win_hard

    print(destinations)
    run_game(player_email, difficulty, game_win_threshold, num_visited_destinations)

"""

def get_location(serial_num):
    return queries.select.select('latitude_deg, longitude_deg', 'airport', f"serial_num='{serial_num}'")


def calculate_distance(location_1, location_2):
    return geopy.distance.distance(location_1, location_2).km


def display_destinations(locations, chose_destination):
    print("Available Destinations:")
    new_locations = {}

    for num, destination in locations.items():
        if num != chose_destination:
            new_locations[num] = destination
            print(f"{num}: {destination}")

    return new_locations


default_location = "Helsinki"
default_location_coordinates = '60.3172, 24.963301'
want_to_play = input('Would you like to play a game? (Type y for yes OR n for no) : ')
start_location = default_location_coordinates
user_location = default_location

if want_to_play.lower() == 'y':
    player_name = None
    player_email = input('Please, type in your email: ')

    def check_player_info():
        existing_player = queries.select.select('email', 'user', f"email='{player_email}'")

        if existing_player:
            return existing_player  # Returning the player information
        else:
            return None  # Player not found


    # existing_player = queries.select.select('email', 'user', f"email='{player_email}'")
    check_player = check_player_info()

    if check_player is None:
        player_name = input('Please, type in your name : ')
        queries.insert.insert('user', f"email, player_name, location",
                              f"'{player_email}', '{player_name}', '{user_location}'")

    user = queries.select.select('co2_consumed', 'user', f"email='{player_email}'")

    num_visited_destinations = 0

    difficulty_easy = 10000
    difficulty_medium = 12000
    difficulty_hard = 16000

    game_win_easy = 7
    game_win_medium = 10
    game_win_hard = 14

    difficulty = None
    game_win_threshold = None

    select_difficulty = input("Difficulty level, select easy, medium, or hard: ")

    if select_difficulty.lower() == "easy":
        difficulty = difficulty_easy
        game_win_threshold = game_win_easy
    elif select_difficulty.lower() == "medium":
        difficulty = difficulty_medium
        queries.update.update('user', 'co2_budget = %s', 'email = %s', (difficulty, player_email))
        game_win_threshold = game_win_medium
    elif select_difficulty == "hard":
        difficulty = difficulty_hard
        queries.update.update('user', 'co2_budget = %s', 'email = %s', (difficulty, player_email))
        game_win_threshold = game_win_hard

    print(destinations)

    while user is not None and (user[0] <= difficulty and game_win_threshold):
        user = queries.select.select('co2_consumed', 'user', f"email='{player_email}'")
        chosen_num_by_player = int(input('Please, choose a number from the available destinations: '))
        updated_destinations = display_destinations(destinations, chosen_num_by_player)

        chosen_location = get_location(chosen_num_by_player)
        current_location = chosen_location
        print(f"Your current location is: {destinations.get(chosen_num_by_player)}")
        queries.update.update_location(destinations.get(chosen_num_by_player), player_email)
        destinations = updated_destinations

        distance_in_kilometer = calculate_distance(start_location, chosen_location)
        co2_consumed_by_player = int(distance_in_kilometer * 0.2) + int(user[0])

        print(f"CO2 consumed: {co2_consumed_by_player}")

        queries.update.update('user', f"co2_consumed={co2_consumed_by_player}", f"email='{player_email}'")

        num_visited_destinations += 1
        print(f"Number of visited Destinations: {num_visited_destinations}")

        if num_visited_destinations >= game_win_threshold:
            print("You have won the game")
            exit()

        if co2_consumed_by_player > difficulty:
            print("You lost the game the game!")
            exit()







def get_location(serial_num):
    return queries.select.select('latitude_deg, longitude_deg', 'airport', f"serial_num='{serial_num}'")


destinations = {"parthenon": get_location(1),
                "Easter Island": get_location(2),
                "Taj Mahal": get_location(3),
                "Colosseum": get_location(4),
                "Angkor": get_location(5),
                "Teotihuacan": get_location(6),
                "Petra": get_location(7),
                "Machu Picchu": get_location(8),
                "Great Wall of China": get_location(9),
                "Pyramids of Giza": get_location(1)}


def calculate_distance(location_1, location_2):
    return geopy.distance.distance(location_1, location_2).km


want_to_play = input('Would you like to play a game? (Type y for yes OR n for no) : ')
CURRENT_LOCATION = '60.3172, 24.963301'

if want_to_play.lower() == 'y':
    CURRENT_LOCATION = '60.3172, 24.963301'

    player_name = None
    player_email = input('Please, type in your email : ')

    existing_player = queries.select.select('email', 'user', f"email='{player_email}'")

    if existing_player is None:
        player_name = input('Please, type in your name : ')
        queries.insert.insert('user',
                              f"email, player_name, location",
                              f"'{player_email}', '{player_name}', 'LOCATION'")

    user = queries.select.select('co2_consumed', 'user', f"email='{player_email}'")

    while user is not None and user[0] <= 10000:
        user = queries.select.select('co2_consumed', 'user', f"email='{player_email}'")
        chosen_num_by_player = int(input('Please, choose number from (1,2,3,4,5,6,7,8,9,10) : '))

        chosen_location = destinations[chosen_num_by_player]
        current_location = chosen_location

        distanceInKilometer = calculate_distance(CURRENT_LOCATION, chosen_location)

        co2_consumed_by_player = int(distanceInKilometer * 0.2) + int(user[0])
        print(f"co2 consumed {co2_consumed_by_player}")

        queries.update.update('user', f"co2_consumed={co2_consumed_by_player}", f"email='{player_email}'")

        if co2_consumed_by_player > 10000:
            exit()



# Version of the game
game_version = "V1.0"

# User input for game and name
user_input = input("Would you like to play the game? (yes/no): ")
print(f"Welcome to the game version {game_version}!")
time.sleep(1)
print("Welcome to Game - 'Visit Wonders'. \n"
      "In order to win this game, you must visit seven wonders of the world. \n"
      "You can choose from wonders by selecting number of keyboard and pressing enter. \n"
      "In order to win the game you must visit wonders of your choice given under the chosen difficulty level by spending co2 emission under the limit allocated.. ")

time.sleep(1)

if user_input.lower() == "yes":
    player_name = input("Please type your name: ")
    print()
    print(f"Welcome, {player_name}")
    print()
    player_email = input("Please type your email: ")

"""
