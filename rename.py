import glob
import os
import re
import logging
from slippi import Game  

version = "v0.9.0"

# More readable character names
character_names = {
    "InGameCharacter.DR_MARIO": "Dr Mario",
    "InGameCharacter.MARIO": "Mario",
    "InGameCharacter.LUIGI": "Luigi",
    "InGameCharacter.BOWSER": "Bowser",
    "InGameCharacter.PEACH": "Peach",
    "InGameCharacter.YOSHI": "Yoshi",
    "InGameCharacter.DONKEY_KONG": "DK",
    "InGameCharacter.CAPTAIN_FALCON": "Falcon",
    "InGameCharacter.GANONDORF": "Ganondorf",
    "InGameCharacter.FALCO": "Falco",
    "InGameCharacter.FOX": "Fox",
    "InGameCharacter.NESS": "Ness",
    "InGameCharacter.POPO": "Popo",
    "InGameCharacter.NANA": "Nana",
    "InGameCharacter.KIRBY": "Kirby",
    "InGameCharacter.SAMUS": "Samus",
    "InGameCharacter.ZELDA": "Zelda",
    "InGameCharacter.SHEIK": "Sheik",
    "InGameCharacter.LINK": "Link",
    "InGameCharacter.YOUNG_LINK": "Young Link",
    "InGameCharacter.PICHU": "Pichu",
    "InGameCharacter.PIKACHU": "Pikachu",
    "InGameCharacter.JIGGLYPUFF": "Jigglypuff",
    "InGameCharacter.MEWTWO": "Mewtwo",
    "InGameCharacter.GAME_AND_WATCH": "G&W",
    "InGameCharacter.MARTH": "Marth",
    "InGameCharacter.ROY": "Roy"
}

# More readable stage names
stage_names = {
    "Stage.FOUNTAIN_OF_DREAMS": "Fountain of Dreams",
    "Stage.POKEMON_STADIUM": "Pokemon Stadium",
    "Stage.PRINCESS_PEACHS_CASTLE": "Princess Peach's Castle",
    "Stage.KONGO_JUNGLE": "Kongo Jungle",
    "Stage.BRINSTAR": "Brinstar",
    "Stage.CORNERIA": "Corneria",
    "Stage.YOSHIS_STORY": "Yoshi's Story",
    "Stage.ONETT": "Onett",
    "Stage.MUTE_CITY": "Mute City",
    "Stage.RAINBOW_CRUISE": "Rainbow Cruise",
    "Stage.JUNGLE_JAPES": "Jungle Japes",
    "Stage.GREAT_BAY": "Great Bay",
    "Stage.HYRULE_TEMPLE": "Hyrule Temple",
    "Stage.BRINSTAR_DEPTHS": "Brinstar Depths",
    "Stage.YOSHIS_ISLAND": "Yoshi's Island",
    "Stage.GREEN_GREENS": "Green Greens",
    "Stage.FOURSIDE": "Fourside",
    "Stage.MUSHROOM_KINGDOM_I": "Mushroom Kingdom I",
    "Stage.MUSHROOM_KINGDOM_II": "Mushroom Kingdom 2",
    "Stage.VENOM": "Venom",
    "Stage.POKE_FLOATS": "Poké Floats",
    "Stage.BIG_BLUE": "Big Blue",
    "Stage.ICICLE_MOUNTAIN": "Icicle Mountain",
    "Stage.ICETOP": "Icetop",
    "Stage.FLAT_ZONE": "Flat Zone",
    "Stage.DREAM_LAND_N64": "Dream Land",
    "Stage.YOSHIS_ISLAND_N64": "Yoshi's Island N64",
    "Stage.KONGO_JUNGLE_N64": "Kongo Jungle N64",
    "Stage.BATTLEFIELD": "Battlefield",
    "Stage.FINAL_DESTINATION": "Final Destination"
}

# Characters that are not valid in a file name
invalid_characters = '<>:"/\\|?*'

# Supported search terms
allowed_terms = ("year", "month", "day", "hour", "minute", "second", "p1_char", "p2_char", "p1_name", "p2_name", "stage", "duration")

# Gets a value from a game based on the search term given
def fetch_entity(entity, game):
    # Removes {} from search term
    entity = entity[1:-1] 
    

# I wanted to use a dictionary for this, but in the end a
# switch would work better. Since python doesn't have switches
# I'm forced to use this ugly if elif mess.
#
#    entities = {
#        "year": str(game.metadata.date.year),
#        "month": str(game.metadata.date.month),
#        "day": str(game.metadata.date.day),
#        "hour": str(game.metadata.date.hour),
#        "minute": str(game.metadata.date.minute),
#        "second": str(game.metadata.date.second),
#        "p1_char": p1_char,
#        
#    }
    
    if entity == "year":
        return str(game.metadata.date.year)

    elif entity == "month":
        month = str(game.metadata.date.month)
        if len(month) != 2:
            month = "0" + month
        return month

    elif entity == "day":
        day = str(game.metadata.date.day)
        if len(day) != 2:
            day = "0" + day
        return day

    elif entity == "hour":
        hour = str(game.metadata.date.hour)
        if len(hour) != 2:
            hour = "0" + hour
        return hour

    elif entity == "minute":
        minute = str(game.metadata.date.minute)
        if len(minute) != 2:
            minute = "0" + minute
        return minute

    elif entity == "second":
        second = str(game.metadata.date.second)
        if len(second) != 2:
            second = "0" + second
        return second

    elif entity == "p1_char":
        p1_char = ""
        try:
            for char in game.metadata.players[0].characters:

                # Special case to handle Ice Climbers
                if str(char) == "InGameCharacter.POPO":
                    return "ICs"

                # This should only apply to Zelda/Sheik
                if p1_char != "":
                    p1_char += "&"
                p1_char += character_names[str(char)]
        except:
            p1_char = "None"
        return p1_char

    elif entity == "p2_char":
        p2_char = ""
        try:
            for char in game.metadata.players[1].characters:
                
                # Special case to handle Ice Climbers
                if str(char) == "InGameCharacter.POPO":
                    return "ICs"

                # This should only apply to Zelda/Sheik
                if p2_char != "":
                    p2_char += "&"
                p2_char += character_names[str(char)]
        except:
            p2_char = "None"
        return p2_char

    elif entity == "p1_name":
        try:
            return re.sub("[<>:\"/\\\\|?*]", '', str(game.metadata.players[0].netplay_name))
        except:
            return ""

    elif entity == "p2_name":
        try:
            return re.sub("[<>:\"/\\\\|?*]", '', str(game.metadata.players[1].netplay_name))
        except:
            return ""

    elif entity == "stage":
        return str(stage_names[str(game.start.stage)])

    elif entity == "duration":
        return str(game.metadata.duration)

# Validates a user submitted template
def is_template_valid(template):
    
    # Checks for invalid characters
    if re.search("[<>:\"/\\\\|?*]", template):
        print("The given pattern contains an invalid character.")
        print("The following characters are considered invalid: <>:\"/\\|?*")
        return False
    
    # Checks for invalid search terms
    terms = re.findall('\{.*?\}',template)
    for term in terms:
        if term[1:len(term) - 1] not in allowed_terms:
            print("%s is an invalid search term. See README.md for valid search terms." % term)
            return False
    
    return True

# Makes the complete filename and checks for duplicate filenames
def make_filename(filename):
    unique_filename = filename
    counter = 2

    # Check for duplicate filenames
    while os.path.isfile(unique_filename + ".slp"):
        unique_filename = filename + " " + str(counter)
        counter += 1

    return unique_filename + ".slp"

#Preset templates
preset_templates = ["{year}-{month}-{day} {p1_char} vs {p2_char} on {stage}",
                    "{year}-{month}-{day} {p1_name} {p1_char} vs {p2_name} {p2_char} on {stage}",
                    "{day}.{month} {hour}.{minute} - {p1_char} vs {p2_char}",
                    "{month}.{day} {hour}.{minute} - {p1_char} vs {p2_char}",
                    "{p1_char}-{p2_char}-{stage}",
                    "{year}-{month}-{day} {p1_name} {p1_char} vs {p2_name} {p2_char}",
                    "{year}-{month}-{day} {hour}.{minute} {p1_name} {p1_char} vs {p2_name} {p2_char} on {stage}"]






print("Welcome to Slippi Replay Renamer " + version + "!")
print("You can use this tool to rename your slippi replays however you like. We have a few templates premade, but you can also make your own! The readme file contains information on how to format your own template.")
print("For more info see https://github.com/blink1415/slippi-replay-renamer/\n")

os_version = {
        "windows": "\\",
        "linux": "/"
}

confirmed = False

validchoices = ["0"]

for i in range(1, len(preset_templates) + 1):
    validchoices.append(str(i))

while not confirmed:
    print("Press the number corresponding to the template you want to use:")
    for i in range(0, len(preset_templates)):
        print("%d. %s" % (i+1, preset_templates[i]))
    print("0. Custom template")    

    choice = input()

    while choice not in validchoices:
        print("The choice you entered was not valid. Please try again.")
        choice = input()
        print()
        
        
    if choice == "0":
        print("\nYou have chosen to make a custom template.")
        template = input("Please input your template: ")
        while not is_template_valid(template):
            template = input("\nHow would you like your replays' name to be formatted?")
    else:
        template = preset_templates[int(choice) - 1]

    if len(re.findall('\{.*?\}',template)) == 0:
        print("Your template has no search terms. Multiple files cannot have the same name, so please select a template with terms.\n")
    else:
        print("\nCurrently selected template: %s" % template)
        selection = input("Is this the template you want to use? y/n \n")
        if selection == "y":
            confirmed = True

terms = re.findall('\{.*?\}',template)

error_games = []
successful_games = 0

open("error-log.txt", "w").close()


# Renames all files in current directory and all subdirectories.
for f in glob.glob('**/*.slp', recursive=True):
    
    # Some games give an error in the parse.py module of py-slippi. I don't know what causes this.
    try:
        game = Game(f)
    except Exception as e:
        print("%d. There was an error processing the following game:  \"%s\"" % (len(error_games) + 1, f))
        error_games.append(f)

        error_log = open("error-log.txt", "a")
        error_log.write("\n---------------------------------------------------------")
        error_log.write("\nThere was an error processing the following game:  \"%s\"\n" % f)
        error_log.write(str(e))
        error_log.close()

        continue
        
    # File path needed to make sure files ends up in correct subfolder.
    path = f.split(os_version["windows"])
    if len(path) > 1:
        path = path[0] + os_version["windows"] 
    else:
        path = ""


    filename = template
 
    for term in terms:
        value = fetch_entity(term, game)
        filename = filename.replace(term, value)
    final_filename = make_filename(path + filename)
    print("%d. Renamed %s" % (successful_games + 1, final_filename))
    #print(make_filename(path + os_version["windows"], filename + ".slp"))
    os.rename(f, final_filename)
    successful_games += 1

print("\n-------------------------------")
print("Number of games renamed: %d" % successful_games)
print("-------------------------------")

if len(error_games) > 0:
    print("Number of games not processed due to an error: %s" % len(error_games))
    print("Sorry about that, I'm working on fixing it! (>_<)")
    print("Error logs have been written to error-log.txt. Feel free to send it to me so I can have a look at it! Contact info can be found on the github page.")
    print("-------------------------------")

input("\nPress enter to exit the program.")
