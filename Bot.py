#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import telepot
from telepot.loop import MessageLoop
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import subprocess
import RPi.GPIO as GPIO
import re
import os
import threading
import requests
import bitcoin

# New imports for HD wallet functionality
from mnemonic import Mnemonic
import bip32utils

# Run some system checks (optional)
os.system('pwd')
os.system('cd ~')
os.system('df -h')
os.system('ls -la')
stream = os.popen('ls -la')
stream = os.popen('df -h')
output = stream.readlines()

# Global flag variables
flag1 = False
flag2 = False
flag3 = False
flag4 = False
flag5 = False
flag6 = False
flag7 = False  # Flag for /chkinterval two-step process

# Set up GPIO output channels
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

# --- Dynamic Variable Loader ---
# The botdata.txt file should have:
# Line 1: ADMIN_ID
# Line 2: TOKEN
# Line 3: wallet_address
# Line 4: api_key
def load_variables():
    file_path = "/home/pi/botdata.txt"
    global ADMIN_ID, TOKEN, wallet_address, api_key
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            if len(lines) >= 4:
                ADMIN_ID = int(lines[0].strip())          # First line: ADMIN_ID
                TOKEN = lines[1].strip()                    # Second line: TOKEN
                wallet_address = lines[2].strip()           # Third line: wallet_address
                api_key = lines[3].strip()                  # Fourth line: api_key
            else:
                print("Error: botdata.txt does not contain the required 4 lines.")
    except Exception as e:
        print(f"Error reading botdata.txt: {e}")

# Initial load of variables
load_variables()

MESSAGE = 'BTC Loto BOT is back online!'

# Create the bot instance using the loaded TOKEN and send an online message
bot = telegram.Bot(token=TOKEN)
bot.send_message(chat_id=ADMIN_ID, text=MESSAGE)

# LED control functions
def on(pin):
    GPIO.output(pin, GPIO.HIGH)
    return

def off(pin):
    GPIO.output(pin, GPIO.LOW)
    return

def get_btc_price():
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
    btc_price = r.json()['USD']
    return btc_price

def get_btc_balance(wallet_address, api_key):
    url = f'https://www.blockonomics.co/api/balance?addr={wallet_address}'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    r = requests.get(url, headers=headers)
    print(r.text)
    satoshi_balance = r.json()['response'][0]['confirmed']
    btc_balance = satoshi_balance / 100000000
    return btc_balance

def send_btc_balance(bot, chat_id, wallet_address, api_key):
    btc_balance = get_btc_balance(wallet_address, api_key)
    btc_price = get_btc_price()  # Gets the current BTC price in USD
    usd_value = btc_balance * btc_price
    formatted_usd = f"{usd_value:,.0f}".replace(",", " ")
    message = f"The balance of the wallet is {btc_balance:0.8f} BTC / {formatted_usd} USD"
    bot.send_message(chat_id=chat_id, text=message)

def check_wallet_balance(wallet_address2, api_key):
    url = f'https://www.blockonomics.co/api/balance?addr={wallet_address2}'
    headers = {'Authorization': f'Bearer {api_key}'}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return f"Error: {r.text}"
    data = r.json()['response'][0]['confirmed']
    btc_balance = data / 100000000
    btc_price = get_btc_price()  # Get current BTC price in USD
    usd_value = btc_balance * btc_price
    formatted_usd = f"{usd_value:,.0f}".replace(",", " ")
    return f"The balance of the wallet is {btc_balance:0.8f} BTC / {formatted_usd} USD"

def blink_led():
    global flag3
    flag3 = True
    while flag3:
        GPIO.output(11, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(11, GPIO.LOW)
        time.sleep(0.5)

def read_chat_ids():
    with open('/home/pi/chat_ids.txt', 'r') as f:
        chat_ids = [int(line.strip()) for line in f]
    return chat_ids

def make_seed_wallet():
    mnemo = Mnemonic("english")
    mnemonic_phrase = mnemo.generate(strength=256)
    seed = mnemo.to_seed(mnemonic_phrase, passphrase="")
    seed_hex = seed.hex()
    root_key = bip32utils.BIP32Key.fromEntropy(seed)
    master_xprv = root_key.ExtendedKey(private=True)
    master_xpub = root_key.ExtendedKey(private=False)
    child_key = root_key.ChildKey(0)
    child_private_wif = child_key.WalletImportFormat()
    child_public_hex = child_key.PublicKey().hex()
    typical_address = bitcoin.pubkey_to_address(child_public_hex)
    output = (
        f"Mnemonic Seed Words:\n{mnemonic_phrase}\n\n"
        f"Derived Seed (hex):\n{seed_hex}\n\n"
        f"Master Extended Private Key (xprv):\n{master_xprv}\n\n"
        f"Master Extended Public Key (xpub):\n{master_xpub}\n\n"
        f"First Child Private Key (WIF):\n{child_private_wif}\n\n"
        f"First Child Public Key:\n{child_public_hex}\n\n"
        f"Typical Public Bitcoin Address:\n{typical_address}\n\n"
        "Use these keys with extreme caution: anyone with access to these keys controls your funds."
    )
    return output

def make_btc_address():
    private_key = bitcoin.random_key()
    public_key = bitcoin.privkey_to_pubkey(private_key)
    address = bitcoin.pubkey_to_address(public_key)
    wif_private_key = bitcoin.encode_privkey(private_key, 'wif')
    return (
        f"New Public Key: {public_key}\n\n"
        f"New Public Address: \n{address}\n\n"
        f"WIF Private Key: {wif_private_key}\n\n"
        "Check at www.bitaddress.org"
    )

def check_private_key(check_address2):
    try:
        address_info = bitcoin.rpc.call('validateaddress', [check_address2])
        if address_info['isvalid']:
            message = f'{check_address2} is a valid bitcoin address'
        else:
            message = f'{check_address2} is not a valid bitcoin address'
    except:
        message = f'An error occurred while checking {check_address2} (Bitcoin Core may not be running)'
    return message

def backup_and_notify(context, chat_id):
    usb_device = "/dev/sdb2"     # Device to check for
    mount_point = "/mnt/usb"     # Mount point for backup

    # Check if the USB device exists
    if not os.path.exists(usb_device):
        context.bot.send_message(chat_id, "USB drive not detected. Please plug in your USB HD.")
        return

    # Create the mount point if it doesn't exist
    os.makedirs(mount_point, exist_ok=True)

    # Check if the device is already mounted at the mount point
    mount_check = subprocess.run(["mountpoint", "-q", mount_point])
    if mount_check.returncode != 0:
        # Device is not mounted; attempt to mount it
        mount_result = subprocess.run(["sudo", "mount", usb_device, mount_point], capture_output=True, text=True)
        if mount_result.returncode != 0:
            context.bot.send_message(chat_id, "Failed to mount USB drive: " + mount_result.stderr)
            return

    # Get information about Bitcoin directory and USB free space
    proc_bitcoin_size = subprocess.run("du -sh /mnt/hdd/.bitcoin", shell=True, capture_output=True, text=True)
    bitcoin_size = proc_bitcoin_size.stdout.strip()

    proc_usb_space = subprocess.run(f"df -h {mount_point}", shell=True, capture_output=True, text=True)
    usb_space = proc_usb_space.stdout.strip()

    context.bot.send_message(chat_id, text=f"Starting backup...\nBitcoin directory size: {bitcoin_size}\nUSB free space:\n{usb_space}")

    # Stop bitcoind for a consistent backup
    subprocess.run("sudo systemctl stop bitcoind.service", shell=True)
    context.bot.send_message(chat_id, text="bitcoind stopped, starting backup process...")

    # Run rsync to backup the .bitcoin directory to the USB drive
    backup_cmd = f"rsync -av --progress /mnt/hdd/.bitcoin {mount_point}/.bitcoin"
    rsync_proc = subprocess.run(backup_cmd, shell=True, capture_output=True, text=True)
    if rsync_proc.returncode != 0:
        context.bot.send_message(chat_id, text="Backup failed: " + rsync_proc.stderr)
        subprocess.run("sudo systemctl start bitcoind.service", shell=True)
        return
    else:
        context.bot.send_message(chat_id, text="Backup finished successfully!")

    # Restart bitcoind
    subprocess.run("sudo systemctl start bitcoind.service", shell=True)
    context.bot.send_message(chat_id, text="bitcoind restarted.")

    # Unmount the USB drive
    unmount_proc = subprocess.run(["sudo", "umount", mount_point], capture_output=True, text=True)
    if unmount_proc.returncode != 0:
        context.bot.send_message(chat_id, text="Warning: USB drive could not be unmounted: " + unmount_proc.stderr)
    else:
        context.bot.send_message(chat_id, text="USB drive unmounted successfully.")

    # Eject the drive (optional)
    eject_proc = subprocess.run(["sudo", "eject", usb_device], capture_output=True, text=True)
    if eject_proc.returncode != 0:
        context.bot.send_message(chat_id, text="Warning: USB drive could not be ejected: " + eject_proc.stderr)
    else:
        context.bot.send_message(chat_id, text="USB drive ejected successfully. Please unplug the USB drive now.")

def message_received(update, context):
    chat_id = update.message.chat_id
    allowed_chat_ids = read_chat_ids()
    if chat_id in allowed_chat_ids:
        command = update.message.text
        print('Got command: %s' % command)
        global flag1, flag2, flag3, flag4, flag5, flag6, flag7, wallet_address

        if command == '/walletcheck':
            flag4 = True
            context.bot.send_message(chat_id, 'Enter a bitcoin wallet address')

        elif flag4:
            wallet_address2 = command
            balance = check_wallet_balance(wallet_address2, api_key)
            context.bot.send_message(chat_id, balance)
            flag4 = False

        elif command == '/wallet':
            send_btc_balance(bot, chat_id, wallet_address, api_key)

        elif command == '/generate':
            btc_gen = make_btc_address()
            context.bot.send_message(chat_id, btc_gen)

        elif command == '/checkadd':
            flag5 = True
            context.bot.send_message(chat_id, 'Enter the private key to check')

        elif flag5:
            check_address2 = command
            check = check_private_key(check_address2)
            context.bot.send_message(chat_id, check)
            flag5 = False

        elif command == '/btc':
            btc_price = get_btc_price()
            context.bot.send_message(chat_id, f'The current price of BTC in USD is: ${btc_price:.0f} USD')

        elif command == '/mywallet':
            context.bot.send_message(chat_id, f'The public address of your wallet is: {wallet_address}')

        elif command == '/ping':
            flag1 = True
            context.bot.send_message(chat_id, 'Which IP do you want to ping?')

        elif flag1:
            ip = command
            run = subprocess.run(['ping', '-c', '3', ip], capture_output=True)
            context.bot.send_message(chat_id, run.stdout.decode())
            flag1 = False

        elif command == '/sudo':
            flag2 = True
            context.bot.send_message(chat_id, 'Type your cmd')

        elif flag2:
            sudo2 = command.split()
            run = subprocess.run(['sudo'] + sudo2, capture_output=True)
            context.bot.send_message(chat_id, run.stdout.decode())
            flag2 = False

        elif command == '/ledon':
            GPIO.output(11, GPIO.HIGH)
            context.bot.send_message(chat_id, 'LED turned on')

        elif command == '/ledoff':
            GPIO.output(11, GPIO.LOW)
            context.bot.send_message(chat_id, 'LED turned off')

        elif command == '/blinkon':
            thread = threading.Thread(target=blink_led)
            thread.start()
            context.bot.send_message(chat_id, 'LED blinking started')

        elif command == '/blinkoff':
            flag3 = False
            GPIO.output(11, GPIO.LOW)
            context.bot.send_message(chat_id, 'LED stopped blinking')

        elif command == '/fanon':
            context.bot.send_message(chat_id, 'FAN turned on', on(12))

        elif command == '/fanoff':
            context.bot.send_message(chat_id, 'FAN turned off', off(12))

        elif command == '/net':
            run_eth0 = subprocess.run(
                ["""ip link show eth0 | awk '/ether/ {print $2}'"""],
                shell=True, capture_output=True, text=True)
            run_wlan0 = subprocess.run(
                ["""ip link show wlan0 | awk '/ether/ {print $2}'"""],
                shell=True, capture_output=True, text=True)
            mac_eth0 = run_eth0.stdout.strip()
            mac_wlan0 = run_wlan0.stdout.strip()
            message = f"Mac Eth0: {mac_eth0}\nMac Wlan0: {mac_wlan0}"
            context.bot.send_message(chat_id, text=message)

        elif command == '/ip':
            run_public = subprocess.run(['curl ifconfig.co'], shell=True, capture_output=True, text=True)
            public_ip = run_public.stdout.strip()
            run_local = subprocess.run(['hostname -I'], shell=True, capture_output=True, text=True)
            local_ips = run_local.stdout.strip().split()
            if local_ips:
                local_ip = local_ips[0]
                tail_ip = local_ips[-1]
            else:
                local_ip = "N/A"
                tail_ip = "N/A"
            message = f"Public IP: {public_ip}\nLocal IP: {local_ip}\nTail IP: {tail_ip}"
            context.bot.send_message(chat_id, text=message)

        elif command == '/storage':
            run_sd = subprocess.run(
                ["""df -h / | tail -1 | awk '{print $3 " (" $5 ")"}'"""],
                shell=True, capture_output=True, text=True)
            sd_usage = run_sd.stdout.strip()
            run_hdex = subprocess.run(
                ["""df -h | grep "/dev/sd" | awk '{print $3 " (" $5 ")"}'"""],
                shell=True, capture_output=True, text=True)
            hdex_usage = run_hdex.stdout.strip()
            message = f"SD Used: {sd_usage}\nExternal HD Used: {hdex_usage}"
            context.bot.send_message(chat_id, text=message)

        elif command == '/htop':
            run = subprocess.run(['ps -e --sort -%mem | head -10'], shell=True, capture_output=True)
            context.bot.sendMessage(chat_id, text='Processes Running: ' + run.stdout.decode('utf-8'))

        elif command == '/device':
            # Merge device information and core temperature into one command
            model_proc = subprocess.run(['cat', '/proc/device-tree/model'], capture_output=True, text=True)
            model = model_proc.stdout.strip()
            user_proc = subprocess.run(['whoami'], capture_output=True, text=True)
            user = user_proc.stdout.strip()
            uptime_proc = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
            uptime_str = uptime_proc.stdout.strip()
            if uptime_str.lower().startswith("up "):
                uptime_str = uptime_str[3:]
            location_proc = subprocess.run(
                ["""curl -s https://extreme-ip-lookup.com/json/?key=ACJdcEKqljZrmlXp1GZA | jq -r '.country' | tr '[:lower:]' '[:upper:]'"""],
                shell=True, capture_output=True, text=True)
            location = location_proc.stdout.strip()
            time_proc = subprocess.run(['date'], capture_output=True, text=True)
            time_date = time_proc.stdout.strip()
            volts_proc = subprocess.run(
                ["""vcgencmd measure_volts $id | awk '{print substr($0, 6, length($0)-9) " V"}'"""],
                shell=True, capture_output=True, text=True)
            volts_used = volts_proc.stdout.strip()
            temp_proc = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
            raw_temp = temp_proc.stdout.strip()
            if raw_temp.startswith("temp=") and raw_temp.endswith("'C"):
                cpu_temp = raw_temp[len("temp="):-2]
            else:
                cpu_temp = "N/A"
            message = (
                f"{model}\n"
                f"User: {user}\n"
                f"Uptime: {uptime_str}\n"
                f"Location: {location}\n"
                f"Time/Date: {time_date}\n"
                f"Volts Used: {volts_used}\n"
                f"CPU temp: {cpu_temp} C"
            )
            context.bot.send_message(chat_id, text=message)

        elif command == '/backup':
            backup_and_notify(context, chat_id)

        elif command == '/chkinterval':
            service_file = '/etc/systemd/system/wallet.service'
            try:
                with open(service_file, 'r') as f:
                    content = f.read()
                m = re.search(r'RestartSec=(\d+)', content)
                if m:
                    current_sec = int(m.group(1))
                    hours = current_sec // 3600
                    minutes = (current_sec % 3600) // 60
                    seconds = current_sec % 60
                    current_interval = f"{hours:02}:{minutes:02}:{seconds:02}"
                else:
                    current_interval = "Unknown"
            except Exception as e:
                current_interval = f"Error reading service file: {str(e)}"
            context.bot.send_message(chat_id, text=f"Current interval is {current_interval}.\nEnter new interval in hh:mm:ss format:")
            flag7 = True

        elif flag7:
            new_interval = command.strip()
            try:
                time_parts = new_interval.split(':')
                if len(time_parts) != 3:
                    raise ValueError("Invalid format. Use hh:mm:ss")
                hours, minutes, seconds = map(int, time_parts)
                new_seconds = hours * 3600 + minutes * 60 + seconds
                service_file = '/etc/systemd/system/wallet.service'
                with open(service_file, 'r') as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    if line.startswith("RestartSec="):
                        lines[i] = f"RestartSec={new_seconds}\n"
                with open(service_file, 'w') as f:
                    f.writelines(lines)
                os.system("sudo systemctl daemon-reload")
                os.system("sudo systemctl restart wallet.service")
                context.bot.send_message(chat_id, f"Wallet service interval updated to {new_interval}.")
            except Exception as e:
                context.bot.send_message(chat_id, f"Error updating interval: {str(e)}")
            flag7 = False

        elif command == '/guide':
            context.bot.sendMessage(chat_id, '/help: Shows you all the commands available\n '
                                    '/reboot: Reboots the device\n '
                                    '/shutdown: Shuts down the device\n '
                                    '/startminer: Starts the BTC miner\n '
                                    '/stopminer: Stops the BTC miner\n '
                                    '/stopbtc: Stops Bitcoind\n '
                                    '/startbtc: Start Bitcoind\n '
                                    '/sync: Shows Blockchain Sync state in (% and size)\n '
                                    '/btc: Shows the current price of BTC in USD\n '
                                    '/backup: Tool to backup Blockchain\n '
                                    '/wallet: Shows the current balance of your BTC wallet in (BTC and USD)\n'
                                    '/mywallet: Shows the current wallet public address\n'
                                    '/changeadd: Change wallet your address\n'
                                    '/walletcheck: Checks the wallet balance in (BTC and USD) of your choice\n'
                                    '/checkadd: Checks Validity of BTC Address\n'
                                    '/chkinterval: Updates interval between wallet check\n'
                                    '/generate: Generates Public / Private key set\n'
                                    '/makeseedwallet: Generates HD seed phrase & addresses\n'
                                    '/fanon: Turns the fan on\n'
                                    '/fanoff: Turns the fan off\n'
                                    '/ledon: Turns LED on\n'
                                    '/ledoff: Turns LED off\n'
                                    '/blinkon: Turns LED on Blinking mode\n'
                                    '/blinkoff: Turns LED off Blinking mode\n'
                                    '/device: Shows Device Information\n'
                                    '/cpu: Shows CPU usage & clock speed\n'
                                    '/storage: Shows used space (GB and %)\n'
                                    '/htop: Runs htop limited to top processes\n'
                                    '/net: Shows Network Information\n'
                                    '/ip: Shows Public, Local, and Tail IP addresses\n'
                                    '/ping: Prompts for ping IP or Domain & gives you results\n'
                                    '/sudo: Prompts for sudo cmd and then executes it\n'
            )

        elif command == '/help':
            context.bot.sendMessage(chat_id,
                                    '/help /guide /reboot /shutdown /startminer /stopminer /stopbtc /startbtc /sync /btc /backup /wallet '
                                    '/mywallet /changeadd /walletcheck /checkadd /checkinterval /generate /makeseedwalet /fanon /fanoff /ledon /ledoff '
                                    '/blinkon /blinkoff /device /cpu /storage /htop /net /ip /ping /sudo'
            )


        elif command == '/reboot':
            context.bot.sendMessage(chat_id, 'Rebooting Now !')
            os.system('sudo reboot')

        elif command == '/shutdown':
            context.bot.sendMessage(chat_id, 'Shutting Down Now !')
            os.system('sudo shutdown')

        elif command == '/startminer':
            context.bot.sendMessage(chat_id, 'Miner Started !')
            os.system('sudo systemctl start bfgminer.service')

        elif command == '/stopminer':
            context.bot.sendMessage(chat_id, 'Miner Stopped !')
            os.system('sudo systemctl stop bfgminer.service')

        elif command == '/stopbtc':
            os.system('sudo systemctl stop bitcoind.service')
            context.bot.send_message(chat_id, 'bitcoind service stopped')

        elif command == '/startbtc':
            os.system('sudo systemctl start bitcoind.service')
            context.bot.send_message(chat_id, 'bitcoind service started')

        elif command == '/changeadd':
            flag6 = True
            context.bot.send_message(chat_id, 'Enter the new Bitcoin wallet address')

        elif flag6:
            new_address = command.strip()
            file_path = '/home/pi/botdata.txt'
            try:
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                if len(lines) >= 3:
                    # Update the third line (wallet_address)
                    lines[2] = new_address + '\n'
                    with open(file_path, 'w') as f:
                        f.writelines(lines)
                    wallet_address = new_address
                    context.bot.send_message(chat_id, f'Wallet address changed to: {new_address}')
                else:
                    context.bot.send_message(chat_id, 'Error: botdata.txt does not contain enough lines.')
            except Exception as e:
                context.bot.send_message(chat_id, f'Error updating wallet address: {str(e)}')
            flag6 = False

        elif command == '/makeseedwallet':
            seed_wallet_info = make_seed_wallet()
            context.bot.send_message(chat_id, seed_wallet_info)

        else:
            context.bot.send_message(chat_id, 'Try /help')
    else:
        context.bot.send_message(chat_id=chat_id, text='Unauthorized Access')

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, message_received))

updater.start_polling()
updater.idle()
