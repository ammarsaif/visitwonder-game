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

def update_new_destination(chosen_location, player_email):
    queries.update.update_location(destinations.get(chosen_location), player_email)


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

default_location = "Helsinki"
default_location_coordinates = '60.3172, 24.963301'
start_location = default_location_coordinates
user_location = default_location
current_location = None
player_name = None

num_visited_destinations = 0
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

## <img class="hide-image" src="https://en.wikipedia.org/wiki/Parthenon#/media/File:The_Parthenon_in_Athens.jpg" alt="Parthenon Image">



