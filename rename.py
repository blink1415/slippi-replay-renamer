import glob
import os
import re
from slippi import Game  

# More readable character names
character_names = {
    "InGameCharacter.DR_MARIO": "Dr. Mario",
    "InGameCharacter.MARIO": "Mario",
    "InGameCharacter.LUIGI": "Luigi",
    "InGameCharacter.BOWSER": "Bowser",
    "InGameCharacter.PEACH": "Peach",
    "InGameCharacter.YOSHI": "Yoshi",
    "InGameCharacter.DONKEY_KONG": "Donkey Kong",
    "InGameCharacter.CAPTAIN_FALCON": "Captain Falcon",
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
    "InGameCharacter.GAME_AND_WATCH": "Mr. Game & Watch",
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
    entity = entity[1:len(entity) - 1] 
    

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
        return str(game.metadata.date.month)

    elif entity == "day":
        return str(game.metadata.date.day)

    elif entity == "hour":
        return str(game.metadata.date.hour)

    elif entity == "minute":
        return str(game.metadata.date.minute)

    elif entity == "second":
        return str(game.metadata.date.second)

    elif entity == "p1_char":
        p1_char = ""
        for char in game.metadata.players[0].characters:
            if p1_char != "":
                p1_char += "/"
            p1_char += character_names[str(char)]
        return p1_char

    elif entity == "p2_char":
        p2_char = ""
        for char in game.metadata.players[1].characters:
            if p2_char != "":
                p2_char += "/"
            p2_char += character_names[str(char)]
        return p2_char

    elif entity == "p1_name":
        return str(game.metadata.players[0].netplay_name)

    elif entity == "p2_name":
        return str(game.metadata.players[1].netplay_name)

    elif entity == "stage":
        return str(stage_names[str(game.start.stage)])

    elif entity == "duration":
        return str(game.metadata.duration)

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


#Preset templates
preset_templates = ["{year}-{month}-{day} {p1_char} vs {p2_char} on {stage}",
                    "{day}.{month} {hour}:{minute} - {p1_char} vs {p2_char}",
                    "{month}.{day} {hour}:{minute} - {p1_char} vs {p2_char}",
                    "{p1_char}-{p2_char}-{stage}"]


print("Welcome to Slippi Replay Renamer!")
print("You can use this tool to rename your slippi replays however you like. We have a few template premade, but you can also make your own! The readme file contains information on how to format your own template.")

confirmed = False

validchoices = ("0")

for i in range(0, len(preset_templates)):
    validchoices = (str(i),) + validchoices

while not confirmed:
    print("Press the number corresponding to the template you want to use:")
    for i in range(0, len(preset_templates)):
        print("%d. %s" % (i, preset_templates[i]))
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
        template = preset_templates[int(choice)]

    if len(re.findall('\{.*?\}',template)) == 0:
        print("Your template has no search terms. Multiple files cannot have the same name, so please select a template with terms.\n")
    else:
        print("\nCurrently selected template: %s" % template)
        selection = input("Is this the template you want to use? y/n \n")
        if selection == "y":
            confirmed = True

terms = re.findall('\{.*?\}',template)


# Renames all files in current directory and all subdirectories.
for f in glob.glob('**/*.slp', recursive=True):
    
    # Some games give an error in the parse.py module of py-slippi. I don't know what causes this.
    try:
        game = Game(f)
    except:
        print("There was an error processing the following game:  \"%s\"" % f)
        continue
        
    # File path needed to make sure files ends up in correct subfolder.
    path = f.split("/")[0]

    filename = template
 
    for term in terms:
        value = fetch_entity(term, game)
        filename = filename.replace(term, value)
    #print("----------")
    #print(f)
    #print(path + "/" + filename + ".slp")
    print(filename)
    os.rename(f, path + "/" + filename + ".slp")
   # input()
