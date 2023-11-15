import random
import time
import os
import requests
import keyboard
from playsound import playsound
from colorama import Fore, Back, Style, just_fix_windows_console
from discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='YourWebhookHere')

just_fix_windows_console()

print("Fetching newest blocks...")

time.sleep(1)

blocks = requests.get('https://raw.githubusercontent.com/terminite1/REx-Reincarnated-Fangame/main/src/serversidedorelist.json').json()
print(blocks)

print("Done.")

embed = None

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

mining_enabled = True
saved = False

def toggle_mining():
    global mining_enabled
    mining_enabled = not mining_enabled
    print(f"Mining {'enabled' if mining_enabled else 'disabled'}.")

keyboard.add_hotkey('ctrl+`', toggle_mining)

while True:
    if mining_enabled:
        saved = False
        selected_block = select_block()
        found = False
        count = 0

        while not found:
            count += 1
            if select_block() == selected_block:
                found = True
                block_name = selected_block['name']
                current_rarity = selected_block['rarity']
                if block_name in inventory:
                    inventory[block_name] += 1
                else:
                    inventory[block_name] = 1
                print(f"Found {block_name} after {count} attempts. ({current_rarity * 100}%) (Total: {inventory[block_name]})")
                write_inventory_to_file(inventory)
                
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
                    embed = DiscordEmbed(title='An Enigmatic tier ore has spawned...', description=f'The ore {block_name} has spawned with rarity {current_rarity * 100}%', color=0xcdf600)
                elif current_rarity <= 1/1000000 and current_rarity >= 1/7500000: # unfathomable
                    print(Fore.BLUE + "The ground shakes below your feet..." + Fore.RESET)
                    playsound('./sounds/unfath.wav', True)
                    embed = DiscordEmbed(title='An Unfathomable tier ore has spawned...', description=f'The ore {block_name} has spawned with rarity {current_rarity * 100}%', color=0x032c79)
                elif current_rarity <= 1/7500000 and current_rarity >= 1/10000000: # otherworldly
                    print(Fore.LIGHTMAGENTA_EX + "You feel a presence behind you..." + Fore.RESET)
                    playsound('./sounds/other.wav', True)
                    embed = DiscordEmbed(title='An Otherworldly tier ore has spawned...', description=f'The ore {block_name} has spawned with rarity {current_rarity * 100}%', color=0x5e0e32)
                elif current_rarity <= 1/10000000 and current_rarity >= 1/50000000: # zenith
                    print(Fore.LIGHTBLACK_EX + "An unutterable horror has spawned..." + Fore.RESET)
                    playsound('./sounds/zenith.wav', True)
                    embed = DiscordEmbed(title='A Zenith tier ore has spawned...', description=f'The ore {block_name} has spawned with rarity {current_rarity * 100}%', color=0x000000)
                elif current_rarity <= 1/50000000 and current_rarity >= 1/100000000: # ethereal
                    print(Fore.CYAN + "A faint glow appears in the distance, and you hear a faint whisper..." + Fore.RESET)
                    playsound('./sounds/ethereal.mp3', True)
                    embed = DiscordEmbed(title='An Ethereal tier ore has spawned...', description=f'The ore {block_name} has spawned with rarity {current_rarity * 100}%', color=0x1dd7a9)
                elif current_rarity <= 1/100000000 and current_rarity >= 1/1000000000: # celestial
                    print(Fore.LIGHTRED_EX + "A strange light fills the air, as you feel your body begin to float..." + Fore.RESET)
                    playsound('./sounds/celestial.mp3', True)
                    embed = DiscordEmbed(title='A Celestial tier ore has spawned...', description=f'The ore {block_name} has spawned with rarity {current_rarity * 100}%', color=0xff2626)
                elif current_rarity <= 1/1000000000: # divine
                    print(Fore.LIGHTWHITE_EX + "You feel a presence in the air, as you hear a voice say, 'You have been chosen...'" + Fore.RESET)
                    playsound('./sounds/divine.mp3', True)
                    embed = DiscordEmbed(title='A Divine tier ore has spawned...', description=f'The ore {block_name} has spawned with rarity {current_rarity * 100}%', color=0xc1c1c1)
                if embed != None:
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    webhook.remove_embed(0)
                embed = None
        time.sleep(0.01)
    else:
        if not saved:
            print("Mining disabled. Press 'ctrl + ~' to enable.")
            write_inventory_to_file(inventory)
            saved = True
            print("Saved inventory.")
            print("Please confirm that your inventory file is not empty before exiting.")
        time.sleep(0.01)