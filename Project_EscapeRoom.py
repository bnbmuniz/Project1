##Import libraries
from IPython.display import display, Image
import sys
import os
import openpyxl
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
import time
import random

t1=time.time()

## define rooms and items
##define room and items for Safe Room


door_a = {
    "name": "door a",
    "type": "door",
}

key_a = {
    "name": "gold and the key for door a",
    "type": "key",
    "target": door_a,
}


bank_safe = {
    "name": "bank safe",
    "type": "prize",
}

safe_room = {
    "name": "safe room",
    "type": "room",
}

outside = {
  "name": "outside"
}

security_guard= {
    "name": "sleeping security guard",
    "type": "furniture",
}

randomlist = random.sample(range(10, 99), 4)
password = [str(num) for num in randomlist]
password = " ".join(password)

paper = {
    "name": "a paper with the code: " + password,
    "type": "paper_code",
    "target": bank_safe,
}

#define rooms and items for Meeting Room 


desk = {
    "name": "desk",
    "type": "furniture",
}

chair = {
    "name": "chair",
    "type": "furniture",
}

board = {
    "name": "board",
    "type": "furniture",
}

door_b = {
    "name": "door b",
    "type": "door",
}

door_c = {
    "name": "door c",
    "type": "door",
}

door_d = {
    "name": "door d",
    "type": "door",
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

meeting_room = {
    "name": "meeting room",
    "type": "room",
}



#define rooms and items for Restroom
toilet = {
    "name": "toilet seat",
    "type": "furniture",
}

hair_dryer = {
    "name": "hair dryer",
    "type": "furniture",
}

cabinet = {
    "name": "cabinet",
    "type": "furniture",
}


key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}


key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

restroom = {
    "name": "restroom",
    "type": "room",
}


#define rooms and items for Reception Room
reception_room = {
    "name": "reception room",
    "type": "room",
}

reception_desk = {
    "name": "reception desk",
    "type": "furniture",
}

security_guard_2 = {
    "name": "another sleeping security guard",
    "type": "get_arrested",
}


all_rooms = [safe_room, meeting_room, restroom, reception_room, outside]

all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related

object_relations = {
    "safe room": [bank_safe, security_guard, door_a],
    "bank safe": [key_a],
    "sleeping security guard": [paper],
    "outside": [door_d],
    "door a": [safe_room, meeting_room],
    "meeting room": [desk, chair, board, door_c, door_b, door_a],
    "door b": [meeting_room, restroom],
    "desk": [key_b],
    "restroom": [hair_dryer, cabinet, toilet, door_b],
    "hair dryer": [key_c],
    "cabinet": [key_d],
    "door c": [meeting_room, reception_room],
    "reception room": [reception_desk, door_c, door_d, security_guard_2],
    "door d": [reception_room, outside],
}

# define game state. Do not directly change this dict. 
# =============================================================================
# # Instead, when a new game starts, make a copy of this
# =============================================================================
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": safe_room,
    "keys_collected": [],
    "target_room": outside
}



def linebreak():
    """
    Print a line break
    """
    print("\n\n")


def decisions():
    """
    This function checks if the player wants to play the game before it starts.
    """
    decision = input("Do you want to play the game? (Please write yes or no)").lower().strip()
    if decision == "yes":
        print("Let the game start!")
        display(Image(filename='/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/Capture.png'))
    elif decision == "no":
        decision_2 = input("Are you sure? (Please write yes or no)").lower().strip()
        if decision_2 == "yes":
            print("Bye Bye! Have a nice day!")
            display(Image(filename='/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/Capture1.png'))
            sys.exit()
        elif decision_2 =="no":
            print("Ok, let the game start!")
            display(Image(filename='/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/Capture.png'))
        else:
            print("Please reply yes or no.")
            decisions()
    else:
        print("Please reply yes or no.")
        decisions()
        

def name_of_user():
    """
    This function asks the name of the player and saves it in an Excel file.
    """
    name = input("Please write your name:").capitalize().strip()
    #print(name) 
    
    if name.isalpha() == False:
        print("Please write your name using only letters")
        name_of_user()    
    else:

        file_name = '/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/Names_Players.xlsx'

        name_data = pd.DataFrame({name})

        # create excel file
        if os.path.isfile(file_name):  # if file already exists append to existing file
            workbook = openpyxl.load_workbook(file_name)  # load workbook if already exists
            sheet = workbook['file_name']  # declare the active sheet 

            # append the dataframe results to the current excel file
            for row in dataframe_to_rows(name_data, header = False, index = False):
                sheet.append(row)
            workbook.save(file_name)  # save workbook
            workbook.close()  # close workbook
        else:  # create the excel file if doesn't already exist
            with pd.ExcelWriter(path = file_name, engine = 'openpyxl') as writer:
                name_data.to_excel(writer, startrow=0, startcol=0, index = False, header = False, sheet_name = 'file_name')

def start_game():
    """
    Start the game
    """

    print("You wake up on the floor inside the Bank of Portugal. You don't remember why you are here and what had happened before. You know that the sleeping guard will wake up any time soon and you must find the gold and get out of the Bank, NOW!")

    play_room(game_state["current_room"])
    

def play_again():
    """
    This function checks if the player wants to play the game again once it's finished.
    """
    answer = input("Do you want to play again? (Please write yes or no)").lower().strip()
    object_relations["bank safe"]=[key_a]
    object_relations["sleeping security guard"]= [paper]
    object_relations["desk"]= [key_b]
    object_relations["hair dryer"]= [key_c]
    object_relations["cabinet"]= [key_d]

    if answer == "yes":
        game_state["current_room"] = safe_room
        game_state["keys_collected"]=[]
        global t1  ##we use global so python can understand that variable is not only inside the function, it takes the one that it's outisde
        t1 = time.time()
        start_game()
    elif answer == "no":
        display(Image(filename='/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/Capture1.png'))
        sys.exit()
    else:
        print("Please reply with yes or no.")
        play_again()

             
def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        global t1
        t2=time.time()
        time_game=t2-t1

        file_name = '/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/Names_Players.xlsx'

        time_data = pd.DataFrame({time_game})

        # create excel file
        if os.path.isfile(file_name):  # if file already exists append to existing file
            workbook = openpyxl.load_workbook(file_name)  # load workbook if already exists
            sheet = workbook['file_name']  # declare the active sheet 

            # append the dataframe results to the current excel file
            for row in dataframe_to_rows(time_data, header = False, index = False):
                sheet.append(row)
            workbook.save(file_name)  # save workbook
            workbook.close()  # close workbook
        else:  # create the excel file if doesn't already exist
            with pd.ExcelWriter(path = file_name, engine = 'openpyxl') as writer:
                time_data.to_excel(writer, startrow=0, startcol=1, index = False, header = False, sheet_name = 'file_name')
                
        print("Congrats! You escaped the bank with all Portugal gold!")
        print("Your time playing the game was:", time_game)
        display(Image(filename='/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/Capture3.png'))
        sound_file = '/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/bellaciao_correto.mp3'
        os.system("afplay " + sound_file)
        play_again()
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'examine'?").strip()
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine?").strip())
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "prize"):
                try_code = input("The bank safe is locked and you need a code to open it:")
                code_list = try_code.split()
                code = " ".join(code_list)
                if code == password:
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                    display(Image(filename='/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/gold.jpeg'))
                    sound_file = '/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/victory.mp3'
                    os.system("afplay " + sound_file)
                else:
                    output += "You don't have the right code"
            elif(item["type"] == "get_arrested"):
                print("Oh no! You woke up the security guard and now you're arrest. Good luck next time!")
                display(Image(filename='/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/arrested.jpeg'))
                ##Source Image Arrested: https://screenrant.com/simpsons-ways-homer-got-worse-unlikable/
                sound_file = '/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project1_EscapeRoomGame/youlose.mp3'
                os.system("afplay " + sound_file)
                play_again()
            elif(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")
    
    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
        play_room(next_room)
    else:
        play_room(current_room)
game_state = INIT_GAME_STATE.copy()
decisions()
name_of_user()
start_game()
