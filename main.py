import geopy.distance
import queries.insert
import queries.select
import queries.update
import time


def get_location(serial_num):
    return queries.select.select('latitude_deg, longitude_deg', 'airport', f"serial_num='{serial_num}'")


default_location = "Helsinki"
default_location_coordinates = '60.3172, 24.963301'
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


def calculate_distance(location_1, location_2):
    return geopy.distance.distance(location_1, location_2).km


def display_destinations(locations, chosen_num_by_player):
    print("Available Destinations:")
    new_locations = {}

    for num, destination in locations.items():
        if num != chosen_num_by_player:
            new_locations[num] = destination
            print(f"{num}: {destination}")

    return new_locations


want_to_play = input('Would you like to play a game? (Type y for yes OR n for no) : ')
start_location = default_location_coordinates
user_location = "location"

if want_to_play.lower() == 'y':
    player_name = None
    player_email = input('Please, type in your email : ')

    existing_player = queries.select.select('email', 'user', f"email='{player_email}'")

    if existing_player is None:
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
        game_win_threshold = game_win_medium
    elif select_difficulty == "hard":
        difficulty = difficulty_hard
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

"""
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
      "You will win the game if you visit seven wonders of your choice by spending co2 emission under the limit given. ")

time.sleep(1)

if user_input.lower() == "yes":
    player_name = input("Please type your name: ")
    print()
    print(f"Welcome, {player_name}")
    print()
    player_email = input("Please type your email: ")

"""
