import random
import time
import os
import requests
import keyboard
import yaml
from colorama import Fore, Back, Style, just_fix_windows_console
from discord_webhook import DiscordWebhook, DiscordEmbed
from playsound import playsound

CONFIG_FILE = 'config.yaml'

if not os.path.exists(CONFIG_FILE):
    print(
        "Welcome to Untitled Console Game! This is your first time running the program, so I'll give you a quick rundown of how it works.")
    print(
        "You can press 'ctrl + ~' to pause the program. When you pause the program, it will save your inventory to a file called 'inventory.txt'.")
    print(
        "There is also a config file called 'config.yaml'. You can edit this file to change the program's settings. If you want to reset the config file, delete it and run the program again.")
    print("There is NO objective. You just mine ores. That's it.")
    print(
        "For more information, check out the README.md file on GitHub. Or join the Discord. Or something. I don't know. I'm not your mom. I'm just a program. I don't know what you want from me.\nhttps://discord.gg/TrNUM7NST8")
    print("Anyways, let's get started.")
    print("We need to set up the config file. This file stores your settings for the program.")
    print("After this, you're good to go. Happy mining!")
    with open(CONFIG_FILE, 'w') as f:
        config = {
            'print_attempt': None,
            'enable_tracking': None,
            'print_inventory_on_pause': None,
            'webhook': ''
        }
        yaml.dump(config, f)

with open(CONFIG_FILE, 'r') as f:
    config = yaml.safe_load(f)
    print("Loaded config file.")

if config['print_attempt'] is None:
    print(
        "If you set this to True, the program will print every 10000 attempts. If you set this to False, the program will only print when it finds an ore.")
    print_attempt = input('Please enter a value for print_attempt (True/False): ')
    config['print_attempt'] = print_attempt
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

if config['enable_tracking'] is None:
    print("If you set this to True, the program will send a Discord webhook when it finds an ore.")
    enable_tracking = input('Please enter a value for enable_tracking (True/False): ')
    config['enable_tracking'] = enable_tracking
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

if config['print_inventory_on_pause'] is None:
    print("If you set this to True, the program will print your inventory when you pause your mining.")
    inventory_print = input('Please enter a value for print_inventory_on_pause (True/False): ')
    config['print_inventory_on_pause'] = inventory_print
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

if config['webhook'] == '':
    print("Set a URL to enable Discord webhooks.")
    webhook_url = input('Please enter a Discord webhook URL (leave blank to ignore): ')
    if webhook_url != '':
        webhook = DiscordWebhook(url=webhook_url)
        config['webhook'] = webhook_url
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(config, f)
    else:
        config['webhook'] = None
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(config, f)

print_attempt = config['print_attempt']
enable_tracking = config['enable_tracking']
webhook_url = config['webhook']
print_inventory_on_pause = config['print_inventory_on_pause']
webhook = DiscordWebhook(url=webhook_url)

github_url = 'https://raw.githubusercontent.com/terminite1/REx-Reincarnated-Fangame/main/src/rex%20but%20real.py'

response = requests.get(github_url)

if response.status_code == 200:
    print("Checking for updates...")
    file_contents = response.content.decode('utf-8')

    with open(__file__, 'r') as f:
        current_file_contents = f.read()

    if file_contents == current_file_contents:
        print('This is the newest version.')
    else:
        print('There is a newer version available.')
        print("Would you like to update? (y/n)")
        update = input('Please enter a value for update (y/n): ')
        if update == 'y':
            print('Installing....')
            with open("rex but real-UPDATED.py", 'w') as f:
                f.write(file_contents)
            print('Installed new version as rex but real-UPDATED.py')
            print('Please run that instead.')
            input('Press enter to exit.')
            exit()
        else:
            print('Update cancelled.')
else:
    print('Failed to fetch the file from GitHub.')

just_fix_windows_console()

print("Fetching newest blocks...")

time.sleep(1)

blocks = requests.get(
    'https://raw.githubusercontent.com/terminite1/REx-Reincarnated-Fangame/main/src/serversidedorelist.json').json()
print(blocks)

print("Done.")

embed = None


def write_ores_to_file(blocks):
    with open('ores.txt', 'w') as f:
        for block in blocks:
            rarity = float(block['rarity'])
            f.write(f"{block['name']}: {rarity * 100:.20f}%\n")


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
            if count % 10000 == 0 and (print_attempt is True or print_attempt == 'true' or print_attempt == 'True'):
                print(Back.RED + f"Attempt {count}..." + Back.RESET)
            if select_block() == selected_block:
                found = True
                block_name = selected_block['name']
                current_rarity = selected_block['rarity']
                percentage_rarity = current_rarity * 100
                percentage_rarity_str = '{:.20f}'.format(percentage_rarity)
                if block_name in inventory:
                    inventory[block_name] += 1
                else:
                    inventory[block_name] = 1
                print(
                    f"Found {block_name} after {count} attempts. ({'{:.10f}'.format(percentage_rarity)}%) (Total: {inventory[block_name]})")

                if 1 / 10000 >= current_rarity > 1 / 49999:  # exotic
                    print(Fore.LIGHTYELLOW_EX + "A chill goes down your spine..." + Fore.RESET)
                    playsound('./sounds/chill.wav')
                elif 1 / 50000 >= current_rarity > 1 / 99999:  # exquisite
                    print(Fore.GREEN + "Your heart skips a beat..." + Fore.RESET)
                    playsound('./sounds/skip.wav')
                elif 1 / 100000 >= current_rarity > 1 / 499999:  # transcendent
                    print(Fore.LIGHTBLUE_EX + "You hear a ringing in your ears..." + Fore.RESET)
                    playsound('./sounds/ringing.wav')
                elif 1 / 500000 >= current_rarity > 1 / 999999:  # enigmatic
                    print(Fore.YELLOW + "Your vision begins to blur..." + Fore.RESET)
                    playsound('./sounds/blur.wav')
                    embed = DiscordEmbed(title='An Enigmatic tier ore has spawned...',
                                         description=f'The ore {block_name} has spawned with rarity {percentage_rarity_str}% and {count} attempts',
                                         color=0xcdf600)
                elif 1 / 1000000 >= current_rarity >= 1 / 12500000:  # unfathomable
                    print(Fore.BLUE + "An unforeseen force violently shakes the ground..." + Fore.RESET)
                    playsound('./sounds/unfath.wav')
                    embed = DiscordEmbed(title='An Unfathomable tier ore has spawned...',
                                         description=f'The ore {block_name} has spawned with rarity {percentage_rarity_str}% and {count} attempts',
                                         color=0x032c79)
                elif 1 / 12500000 >= current_rarity >= 1 / 21500000:  # otherworldly
                    print(Fore.LIGHTMAGENTA_EX + "You feel a strange presence creeping up behind you..." + Fore.RESET)
                    playsound('./sounds/other.wav')
                    embed = DiscordEmbed(title='An Otherworldly tier ore has spawned...',
                                         description=f'The ore {block_name} has spawned with rarity {percentage_rarity_str}% and {count} attempts',
                                         color=0x5e0e32)
                elif 1 / 21500000 >= current_rarity >= 1 / 47500000:  # zenith
                    print(
                        Fore.LIGHTBLACK_EX + "An unutterable horror has emerged from the depths of the earth..." + Fore.RESET)
                    playsound('./sounds/zenith.wav')
                    embed = DiscordEmbed(title='A Zenith tier ore has spawned...',
                                         description=f'The ore {block_name} has spawned with rarity {percentage_rarity_str}% and {count} attempts',
                                         color=0x000000)
                elif 1 / 47500000 >= current_rarity >= 1 / 80000000:  # ethereal
                    print(
                        Fore.CYAN + "A faint glow appears in the distance, blinking in and out of existence..." + Fore.RESET)
                    playsound('./sounds/ethereal.mp3')
                    embed = DiscordEmbed(title='An Ethereal tier ore has spawned...',
                                         description=f'The ore {block_name} has spawned with rarity {percentage_rarity_str}% and {count} attempts',
                                         color=0x1dd7a9)
                elif 1 / 80000000 >= current_rarity >= 1 / 275000000:  # celestial
                    print(
                        Fore.LIGHTRED_EX + "A strange light fills the air, as you feel your body begin to float..." + Fore.RESET)
                    playsound('./sounds/celestial.mp3')
                    embed = DiscordEmbed(title='A Celestial tier ore has spawned...',
                                         description=f'The ore {block_name} has spawned with rarity {percentage_rarity_str}% and {count} attempts',
                                         color=0xff2626)
                elif 1 / 275000000 >= current_rarity >= 1 / 500000000:  # cosmic
                    print(
                        Fore.LIGHTCYAN_EX + "The awakening of a supermassive singularity brings time itself to a halt..." + Fore.RESET)
                    playsound('./sounds/cosmic.mp3')
                    embed = DiscordEmbed(title='A Cosmic tier ore has spawned...',
                                         description=f'The ore {block_name} has spawned with rarity {percentage_rarity_str}% and {count} attempts',
                                         color=0x6FA8DC)
                elif 1 / 500000000 >= current_rarity >= 1 / 750000000:  # mystical
                    print(
                        Fore.MAGENTA + "A subtle atmospheric shift catches your attention, accompanied by a soft murmur..." + Fore.RESET)
                    playsound('./sounds/mystical.mp3')
                    embed = DiscordEmbed(title='A Mystical tier ore has spawned...',
                                         description=f'The ore {block_name} has spawned with rarity {percentage_rarity_str}% and {count} attempts',
                                         color=0xf300ff)
                elif current_rarity <= 1 / 750000000:  # divine
                    print(
                        Fore.LIGHTWHITE_EX + "You feel a presence in the air, as you hear a voice say, 'You have been chosen...'" + Fore.RESET)
                    playsound('./sounds/divine.mp3')
                    embed = DiscordEmbed(title='A Divine tier ore has spawned!!!',
                                         description=f'The ore {block_name} has spawned with rarity {percentage_rarity_str}% and {count} attempts',
                                         color=0xc1c1c1)
                if embed is not None and (
                        enable_tracking is True or enable_tracking == 'true' or enable_tracking == 'True'):
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    webhook.remove_embed(0)
                embed = None
                write_inventory_to_file(inventory)

        time.sleep(0.001)
    else:
        if not saved:
            print("Mining disabled. Press 'ctrl + ~' to enable.")
            write_inventory_to_file(inventory)
            saved = True
            print("Saved inventory.")
            print("Please confirm that your inventory file is not empty before exiting.")
            if print_inventory_on_pause is True or print_inventory_on_pause == 'true' or print_inventory_on_pause == 'True':
                print(print_inventory_on_pause)
                print("Inventory:")
                for block in blocks:
                    if block['name'] in inventory:
                        print(f"{block['name']}: {inventory[block['name']]}")
        time.sleep(0.001)
