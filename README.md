# D-FiCracker

A beginner-friendly Wi-Fi handshake capture and cracker tool made for Kali Linux.

**👨‍💻 Developed by:** Dilshuppa  
**🎯 Purpose:** For ethical hacking practice, student learning, and pentesting on authorized networks only.

---

## 📦 Features

- Lists available wireless adapters
- Lets you pick a target Wi-Fi network
- Captures WPA handshake using `airodump-ng` & `aireplay-ng`
- Cracks the password using `aircrack-ng` with a wordlist

---

## 🧪 Requirements

- Kali Linux
- Wireless adapter that supports monitor mode
- Run the tool as `sudo`
- `aircrack-ng` installed (comes with Kali)

---

## 🚀 Usage

```bash
sudo python3 D-FiCracker.py
