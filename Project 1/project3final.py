import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

class Player:
    def __init__(self):
        self.current_room = None
        self.turn_count = 0

class Neighbor:
    def __init__(self):
        self.current_room = "Bedroom"
        self.move_count = 0

class Room:
    def __init__(self, name, connected_rooms):
        self.name = name
        self.connected_rooms = connected_rooms

class Mission:
    def __init__(self, description, room):
        self.description = description
        self.room = room
        self.completed = False

def initialize_game():
    rooms = {
        "Living Room": Room("Living Room", ["Kitchen", "Bathroom"]),
        "Kitchen": Room("Kitchen", ["Living Room", "Garage"]),
        "Bathroom": Room("Bathroom", ["Living Room", "Bedroom"]),
        "Bedroom": Room("Bedroom", ["Bathroom", "Garage"]),
        "Garage": Room("Garage", ["Kitchen", "Bedroom"]),
    }

    missions = [
        Mission("Flood the bathroom sink", "Bathroom"),
        Mission("Unplug the fridge", "Kitchen"),
        Mission("Scratch the neighbor's car", "Garage"),
        Mission("Mess up the living room furniture", "Living Room"),
        Mission("Hide the neighbor's alarm clock", "Bedroom"),
    ]

    player = Player()
    neighbor = Neighbor()

    return player, neighbor, rooms, missions

def show_intro():
    clear_screen()
    slow_print("Welcome to Sabotage Your Neighbor!")
    slow_print("Complete 5 sabotage missions before getting caught!")
    slow_print("Type 'help' if you need a list of commands.")

def show_help():
    slow_print("\n== HELP MENU ==")
    slow_print("- move to [room]: Move to a connected room.")
    slow_print("- sabotage: Attempt a sabotage mission.")
    slow_print("- listen: Listen for your neighbor's location.")
    slow_print("- status: View your progress.")
    slow_print("- help: Show help menu again.")

def move_neighbor(neighbor, rooms):
    current_room = rooms[neighbor.current_room]
    neighbor.current_room = random.choice(current_room.connected_rooms)
    neighbor.move_count += 1
    if neighbor.move_count % 3 == 0:
        next_room = rooms[neighbor.current_room]
        neighbor.current_room = random.choice(next_room.connected_rooms)

def display_location(player, room, neighbor, rooms, missions):
    clear_screen()
    slow_print(f"You are in the {room.name}.")
    slow_print(f"Turn: {player.turn_count}")
    connected = ", ".join(room.connected_rooms)
    slow_print(f"Connected rooms: {connected}")

    available_missions = [m for m in missions if m.room == room.name and not m.completed]
    if available_missions:
        slow_print("There are sabotage missions available! (use 'sabotage')")

    slow_print("\nAvailable actions:")
    slow_print("- move to [room name]")
    slow_print("- listen")
    slow_print("- status")
    slow_print("- help")
    if available_missions:
        slow_print("- sabotage")

def solve_math_problem():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operation = random.choice(["+", "-", "*"])

    if operation == "+":
        answer = num1 + num2
        problem = f"What is {num1} + {num2}?"
    elif operation == "-":
        if num1 < num2:
            num1, num2 = num2, num1
        answer = num1 - num2
        problem = f"What is {num1} - {num2}?"
    else:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        answer = num1 * num2
        problem = f"What is {num1} * {num2}?"

    slow_print("\nSolve to complete sabotage:")
    slow_print(problem)

    try:
        user_answer = int(input("Your answer: ").strip())
        return user_answer == answer
    except ValueError:
        slow_print("Invalid answer.")
        return False

def neighbor_gets_closer(neighbor, player, rooms):
    path = find_path_to_player(neighbor.current_room, player.current_room, rooms)
    if len(path) > 1:
        neighbor.current_room = path[1]
        slow_print("You hear your neighbor getting closer!")

def find_path_to_player(start_room, target_room, rooms):
    queue = [[start_room]]
    visited = set([start_room])

    while queue:
        path = queue.pop(0)
        current = path[-1]

        if current == target_room:
            return path

        for next_room in rooms[current].connected_rooms:
            if next_room not in visited:
                visited.add(next_room)
                new_path = list(path)
                new_path.append(next_room)
                queue.append(new_path)
    return [start_room]

def listen_for_neighbor(player, neighbor, rooms):
    distance = len(find_path_to_player(player.current_room, neighbor.current_room, rooms)) - 1
    if distance == 0:
        slow_print("RUN!!! Your neighbor is here!")
    elif distance == 1:
        slow_print("You hear your neighbor very close!")
    elif distance == 2:
        slow_print("Neighbor footsteps nearby...")
    else:
        slow_print("You hear your neighbor somewhere far away.")

def show_status(player, neighbor, missions_completed, failed_missions):
    clear_screen()
    slow_print("== STATUS ==")
    slow_print(f"Current room: {player.current_room}")
    slow_print(f"Missions completed: {missions_completed}/5")
    slow_print(f"Missions failed: {failed_missions}/3")
    slow_print(f"Turns played: {player.turn_count}")

def show_game_over(message, success):
    clear_screen()
    if success:
        slow_print("== VICTORY ==")
    else:
        slow_print("== GAME OVER ==")

    slow_print(message)
    input("\nPress Enter to exit.")

def main():
    show_intro()
    player, neighbor, rooms, missions = initialize_game()

    current_room = rooms["Living Room"]
    player.current_room = current_room.name

    missions_completed = 0
    failed_missions = 0
    turn = 0

    while True:
        turn += 1
        player.turn_count = turn
        move_neighbor(neighbor, rooms)
        display_location(player, current_room, neighbor, rooms, missions)

        if neighbor.current_room == player.current_room:
            show_game_over("You have been caught by your neighbor!", False)
            break

        if missions_completed >= 5:
            show_game_over("You completed 5 sabotage missions! Your neighbor is having a terrible day.", True)
            break

        if failed_missions >= 3:
            show_game_over("You failed 3 missions. Your neighbor's day went too well.", False)
            break

        command = input("\nWhat do you want to do? ").strip().lower()

        if command.startswith("move to "):
            destination = command[8:].title()
            if destination in current_room.connected_rooms:
                current_room = rooms[destination]
                player.current_room = current_room.name
                slow_print(f"Moving to {destination}...")
                time.sleep(1)
            else:
                slow_print("That room isn't connected to your current location.")
                input("Press Enter to continue.")

        elif command == "sabotage":
            available_missions = [m for m in missions if m.room == current_room.name and not m.completed]
            if available_missions:
                mission = random.choice(available_missions)
                slow_print(f"Mission: {mission.description}")
                if solve_math_problem():
                    slow_print("Congrats! You sabotaged your neighbor!")
                    mission.completed = True
                    missions_completed += 1
                    slow_print(f"Missions completed: {missions_completed}/5")
                else:
                    slow_print("You failed the sabotage.")
                    failed_missions += 1
                    slow_print(f"Missions failed: {failed_missions}/3")
                    neighbor_gets_closer(neighbor, player, rooms)
            else:
                slow_print("No available sabotage missions here.")
            input("Press Enter to continue.")

        elif command == "listen":
            listen_for_neighbor(player, neighbor, rooms)
            input("Press Enter to continue.")

        elif command == "status":
            show_status(player, neighbor, missions_completed, failed_missions)
            input("Press Enter to continue.")

        elif command == "help":
            show_help()
            input("Press Enter to continue.")

        else:
            slow_print("Invalid command. Type 'help' for options.")
            input("Press Enter to continue.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
