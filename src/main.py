import random
import time
import os
from colorama import Fore, Back, Style, just_fix_windows_console

just_fix_windows_console()
try:
    from playsound import playsound
except ImportError:
    print("You don't have the module, playsound, installed. Installing it now...")
    os.system("pip install playsound")
    from playsound import playsound

blocks = [
    {'name': 'stone', 'rarity': 1/1},
    {'name': 'placeholder', 'rarity': 1/7},
    {'name': 'the ore', 'rarity': 1/23},
    {'name': 'iron', 'rarity': 1/55},
    {'name': 'gold', 'rarity': 1/100},
    {'name': 'poop (regular)', 'rarity': 1/250},
    {'name': 'emerald', 'rarity': 1/340},
    {'name': 'sapphire', 'rarity': 1/500},
    {'name': 'your kitchen', 'rarity': 1/500},
    {'name': 'diamond', 'rarity': 1/680},
    {'name': 'ruby', 'rarity': 1/800},
    {'name': 'amethyst', 'rarity': 1/1000},
    {'name': 'topaz', 'rarity': 1/1200},
    {'name': 'platinum', 'rarity': 1/1280},
    {'name': 'obsidian', 'rarity': 1/1500},
    {'name': 'adamantium', 'rarity': 1/2000},
    {'name': 'uranium', 'rarity': 1/2500},
    {'name': 'quartz', 'rarity': 1/3000},
    {'name': 'neptunium', 'rarity': 1/4000},
    {'name': 'plutonium', 'rarity': 1/5000},
    {'name': 'flaming minion', 'rarity': 1/5232},
    {'name': 'neutronium', 'rarity': 1/6000},
    {'name': 'gilded', 'rarity': 1/10000},
    {'name': 'chicken ore', 'rarity': 1/15000},
    {'name': 'thing', 'rarity': 1/20000},
    {'name': 'ball', 'rarity': 1/25000},
    {'name': 'cube', 'rarity': 1/30000},
    {'name': 'dodecahedron', 'rarity': 1/33333},
    {'name': 'tricycle', 'rarity': 1/33333},
    {'name': 'tesseract', 'rarity': 1/40000},
    {'name': 'hypercube', 'rarity': 1/45000},
    {'name': 'spinning thing', 'rarity': 1/50000},
    {'name': 'cylinder', 'rarity': 1/55000},
    {'name': 'invisible staircase', 'rarity': 1/55445},
    {'name': 'sphere', 'rarity': 1/60000},
    {'name': 'dinosaur', 'rarity': 1/60000},
    {'name': 'dinosaur egg', 'rarity': 1/65000},
    {'name': 'dinosaur bone', 'rarity': 1/70000},
    {'name': 'dinosaur fossil', 'rarity': 1/75000},
    {'name': 'super flart', 'rarity': 1/77777},
    {'name': 'dinosaur poop', 'rarity': 1/80000},
    {'name': 'dinosaur meat', 'rarity': 1/85000},
    {'name': 'dinosaur skin', 'rarity': 1/90000},
    {'name': 'dinosaur blood', 'rarity': 1/95000},
    {'name': 'alexandrite', 'rarity': 1/100000},
    {'name': 'poudretteite', 'rarity': 1/125000},
    {'name': 'musgravite', 'rarity': 1/150000},
    {'name': 'benitoite', 'rarity': 1/150000},
    {'name': 'red beryl', 'rarity': 1/175000},
    {'name': 'grandidierite', 'rarity': 1/200000},
    {'name': 'black opal', 'rarity': 1/200000},
    {'name': 'jeremejevite', 'rarity': 1/225000},
    {'name': 'F25 key', 'rarity': 1/252525},
    {'name': 'albino fart', 'rarity': 1/300000},
    {'name': 'painite', 'rarity': 1/400000},
    {'name': 'diamond ore', 'rarity': 1/450000},
    {'name': 'tanzanite', 'rarity': 1/500000},
    {'name': 'Legacy Quasar Quasar Quasar 160529 618 618 V', 'rarity': 1/500000},
    {'name': 'taaffeite', 'rarity': 1/600000},
    {'name': 'beryl', 'rarity': 1/700000},
    {'name': 'cool lookin pebble', 'rarity': 1/750000},
    {'name': 'jadeite', 'rarity': 1/800000},
    {'name': 'red diamond', 'rarity': 1/900000},
    {'name': 'jakpot 72', 'rarity': 1/999999},
    {'name': 'serendibite', 'rarity': 1/1000000},
    {'name': 'blue garnet', 'rarity': 1/1000000},
    {'name': 'kyawthuite', 'rarity': 1/1000000},
    {'name': 'cool diamond', 'rarity': 1/1000001},
    {'name': 'cool emerald', 'rarity': 1/1000001},
    {'name': 'cool sapphire', 'rarity': 1/1000001},
    {'name': 'cool ruby', 'rarity': 1/1000001},
    {'name': 'netherine', 'rarity': 1/1250000},
    {'name': 'enderite', 'rarity': 1/1500000},
    {'name': 'bedrock', 'rarity': 1/1750000},
    {'name': 'bedrockium', 'rarity': 1/2000000},
    {'name': 'bedrockite', 'rarity': 1/2250000},
    {'name': 'roentgenium', 'rarity': 1/2250001},
    {'name': 'roxanite', 'rarity': 1/2500000},
    {'name': 'cool lookin ball', 'rarity': 1/2750000},
    {'name': 'cool lookin cube', 'rarity': 1/3000000},
    {'name': 'cool lookin dodecahedron', 'rarity': 1/3250000},
    {'name': 'cool lookin tricycle', 'rarity': 1/3500000},
    {'name': 'spectral hole', 'rarity': 1/3750000},
    {'name': 'manganese', 'rarity': 1/5000000},
    {'name': 'ADRENALINE', 'rarity': 1/10000000},
    {'name': 'cool lookin tricycle', 'rarity': 1/3500000},
    {'name': 'cool lookin tesseract', 'rarity': 1/3750000},
    {'name': 'guga leaf', 'rarity': 1/5500000},
    {'name': 'legacy blackhole 1236', 'rarity': 1/123600000},
    {'name': 'Lost RGB Sharkite Lamp ft. Stormal', 'rarity': 1/444444444},
    {'name': 'blutoof devious', 'rarity': 1/543277998},
    {'name': 'petrified wood 2', 'rarity': 1/2147483647},
    {'name': 'Grand Quasar Legacy 5171 A 160529 1236 V HR', 'rarity': 1/23882811155},
    {'name': 'the', 'rarity': 1/17000000000000}
]

def write_ores_to_file(blocks):
    with open('ores.txt', 'w') as f:
        for block in blocks:
            f.write(f"{block['name']}: {block['rarity'] * 100}%\n")

write_ores_to_file(blocks)

inventory = {}

def select_block():
    total_rarity = sum(block['rarity'] for block in blocks)
    random_value = random.uniform(0, total_rarity)
    for block in blocks:
        random_value -= block['rarity']
        if random_value <= 0:
            return block

def write_inventory_to_file(inventory):
    with open('inventory.txt', 'w') as f:
        for block in blocks:
            if block['name'] in inventory:
                f.write(f"{block['name']}: {inventory[block['name']]}\n")

def read_inventory_from_file():
    try:
        with open('inventory.txt', 'r') as f:
            for line in f:
                item, count = line.strip().split(': ')
                inventory[item] = int(count)
    except FileNotFoundError:
        pass

read_inventory_from_file()

while True:
    selected_block = select_block()
    found = False
    count = 0

    while not found:
        count += 1
        if select_block() == selected_block:
            found = True
            block_name = selected_block['name']
            if block_name in inventory:
                inventory[block_name] += 1
            else:
                inventory[block_name] = 1
            print(f"Found {block_name} after {count} attempts.")
            #print(f"Inventory: {inventory}")
            write_inventory_to_file(inventory)
            current_rarity = selected_block['rarity']
            if current_rarity <= 1/10000 and current_rarity > 1/49999: # exotic
                print(Fore.LIGHTYELLOW_EX + "A chill goes down your spine..." + Fore.RESET)
                playsound('./sounds/chill.wav', True)
            elif current_rarity <= 1/50000 and current_rarity > 1/99999: # exquisite
                print(Fore.GREEN + "Your heart skips a beat..." + Fore.RESET)
                playsound('./sounds/skip.wav', True)
            elif current_rarity <= 1/100000 and current_rarity > 1/499999: # transcendent
                print(Fore.LIGHTBLUE_EX + "You hear a ringing in your ears..." + Fore.RESET)
                playsound('./sounds/ringing.wav', True)
            elif current_rarity <= 1/500000 and current_rarity > 1/999999: # enigmatic
                print(Fore.YELLOW + "Your vision begins to blur..." + Fore.RESET)
                playsound('./sounds/blur.wav', True)
            elif current_rarity <= 1/1000000 and current_rarity >= 1/7500000: # unfathomable
                print(Fore.BLUE + "The ground shakes below your feet..." + Fore.RESET)
                playsound('./sounds/unfath.wav', True)
            elif current_rarity <= 1/7500000 and current_rarity >= 1/10000000: # otherworldly
                print(Fore.LIGHTMAGENTA_EX + "You feel a presence behind you..." + Fore.RESET)
                playsound('./sounds/other.wav', True)
            elif current_rarity <= 1/10000000 and current_rarity >= 1/50000000: # zenith
                print(Fore.LIGHTBLACK_EX + "An unutterable horror has spawned..." + Fore.RESET)
                playsound('./sounds/zenith.wav', True)
            elif current_rarity <= 1/50000000 and current_rarity >= 1/100000000: # ethereal
                print(Fore.CYAN + "A faint glow appears in the distance, and you hear a faint whisper..." + Fore.RESET)
                playsound('./sounds/ethereal.mp3', True)
            elif current_rarity <= 1/100000000 and current_rarity >= 1/1000000000: # celestial
                print(Fore.LIGHTRED_EX + "A strange light fills the air, as you feel your body begin to float..." + Fore.RESET)
                playsound('./sounds/celestial.mp3', True)
            elif current_rarity <= 1/1000000000: # divine
                print(Fore.LIGHTWHITE_EX + "You feel a presence in the air, as you hear a voice say, 'You have been chosen...'" + Fore.RESET)
                playsound('./sounds/divine.mp3', True)
    time.sleep(0.01)