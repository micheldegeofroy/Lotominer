# BTCLOTO Bitcoin Solo Miner on Raspberry Pi 4

## V2 (2025)

This script provides a basic setup for running a Bitcoin Solo CPU miner on a Raspberry Pi 4 
with Tailscale and Telegram Bot.

**Intended Environment:**
- Raspberry Pi OS Lite (64-bit) Debian Bullseye
- Installed using Raspberry Pi Imager on an RPi 4

---

## Setup Instructions

### Connect via SSH

SSH into your Raspberry Pi:

```bash
ssh pi@YOURDEVICEIP
```

### Handling SSH Key Warnings

If you encounter this warning:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
```

Clear the previous key and reconnect:

```bash
ssh-keygen -R YOURDEVICEIP
```

---

## Running the Install Script

Execute the following command to download and run the installation script. Output is logged both to `install.log` and the terminal:

```bash
curl -L -o install.sh https://raw.githubusercontent.com/micheldegeofroy/Lotominer/main/install.sh && nohup sudo bash install.sh 2>&1 | tee install.log
```

To monitor installation progress from another terminal window:

```bash
tail -f install.log
```

---

## TODO List

- Option for solo pool mining (no need for a full node)
- Send alert if external HD is nearly full

---

## GPIO Pinout for Raspberry Pi 4

```
GPIO READALL
+-----+-----+-------------------+------+---+---Pi 4B--+---+------+--------------------+-----+-----+
| BCM | wPi |        Name       | Mode | V | Physical | V | Mode |         Name       | wPi | BCM |
+-----+-----+-------------------+------+---+----++----+---+------+--------------------+-----+-----+
|     |     |             +3.3V |      |   |  1 || 2  |   |      | +5V                |     |     |
|   2 |   8 | GPIO 2    SDA   1 |   IN | 1 |  3 || 4  |   |      | +5V                |     |     |
|   3 |   9 | GPIO 3    SCL   1 |   IN | 1 |  5 || 6  |   |      | GND  0V            |     |     |
|   4 |   7 | GPIO 4    GPCLK 0 |   IN | 1 |  7 || 8  | 0 | ALT5 | GPIO 14    TXD   0 | 15  | 14  |
|     |     |           GND  0V |      |   |  9 || 10 | 1 | ALT5 | GPIO 15    RXD   0 | 16  | 15  |
|  17 |   0 |           GPIO 17 |   IN | 0 | 11 || 12 | 1 | IN   | GPIO 18    PWM   0 | 1   | 18  |
|  27 |   2 |           GPIO 27 |   IN | 0 | 13 || 14 |   |      | GND  0V            |     |     |
|  22 |   3 |           GPIO 22 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO 23            | 4   | 23  |
|     |     |             +3.3V |      |   | 17 || 18 | 0 | IN   | GPIO 24            | 5   | 24  |
|  10 |  12 | GPIO 10 SPIO_MOSI | ALT0 | 0 | 19 || 20 |   |      | GND  0V            |     |     |
|   9 |  13 | GPIO  9 SPIO_MISO | ALT0 | 0 | 21 || 22 | 0 | IN   | GPIO 25            | 6   | 25  |
|  11 |  14 | GPIO 11 SPIO_SCLK | ALT0 | 0 | 23 || 24 | 1 | OUT  | GPIO 08 SPIO CE0 N | 10  | 8   |
|     |     |           GND  0V |      |   | 25 || 26 | 1 | OUT  | GPIO 07 SPIO CE1 N | 11  | 7   |
|   0 |  30 | GPIO  0   SDA   0 |   IN | 1 | 27 || 28 | 1 | IN   | GPIO  1    SCL   0 | 31  | 1   |
|   5 |  21 | GPIO  5           |   IN | 1 | 29 || 30 |   |      | GND  0V            |     |     |
|   6 |  22 | GPIO  6           |   IN | 1 | 31 || 32 | 0 | OUT  | GPIO 12      PWM 0 | 26  | 12  |
|  13 |  23 | GPIO 13           |   IN | 0 | 33 || 34 |   |      | GND  0V            |     |     |
|  19 |  24 | GPIO 19           |   IN | 0 | 35 || 36 | 0 | IN   | GPIO 16            | 27  | 16  |
|  26 |  25 | GPIO 26           |   IN | 0 | 37 || 38 | 0 | IN   | GPIO 20            | 28  | 20  |
|     |     |           GND  0V |      |   | 39 || 40 | 0 | IN   | GPIO 21            | 29  | 21  |
+-----+-----+-------------------+------+---+----++----+---+------+--------------------+-----+-----+

```

---

## Fan and LED Setup Diagram

```
+------------------------------RED------------------------------------+
|  +---------------------------BLACK--------------------------------+ |
|  |                                                                | |
|  |              +3.3V (1)  [.] [.] (2)  +5V                     ,,| |,,
|  |  GPIO 2    SDA   1 (3)  [.] [.] (4)  +5V -------RED------+   | LED |
|  |  GPIO 3    SCL   1 (5)  [.] [.] (6)  GND  0V --BLACK--+  |   '''''''
|  |  GPIO 4    GPCLK 0 (7)  [.] [.] (8)  TXD   1          |  |
|  +----------- GND  0V (9)  [.] [.] (10) RXD   1          |  +-------------------+
+---- GPIO 17           (11) [.] [.] (12) GPIO  1 ------+  |   ,,,,,,,            |
      GPIO 27           (13) [.] [.] (14) GND  0V       |  +---| N T |            |
      GPIO 22           (15) [.] [.] (16) GPIO 23       +------| P R |            |
                  +3.3V (17) [.] [.] (18) GPIO 24          +---| N A |            |
      GPIO 10 SPIO_MOSI (19) [.] [.] (20) GND              |   |   N |            |
      GPIO  9 SPIO_MISO (21) [.] [.] (22) GPFS3            |   '''''''            |
      GPIO 11 SPIO_SCLK (23) [.] [.] (24) MOSI1            +-----BLACK----|'''''''''|
                GND  0V (25) [.] [.] (26) MISO1                           |   FAN   |
      GPIO  0   SDA   0 (27) [.] [.] (28) SCLK1                           |         |
      GPIO  5           (29) [.] [.] (30) GND                             '''''''''''
      GPIO  6           (31) [.] [.] (32) GPFS6
      GPIO 13   PWM   1 (33) [.] [.] (34) GND
      GPIO 19           (35) [.] [.] (36) GPFS8
      GPIO 26           (37) [.] [.] (38) GPFS9
                GND  0V (39) [.] [.] (40) GPFS10
```

---

## GPIO Abbreviations

- **GND:** Ground
- **SDA:** Serial Data Line
- **SCL:** Serial Clock Line
- **TXD:** Transmit Data
- **RXD:** Receive Data
- **GPCLK:** General Purpose Clock
- **GPFS:** General Purpose Function Select
- **MOSI:** Master Out, Slave In
- **MISO:** Master In, Slave Out
- **SCLK:** Serial Clock
- **GPIO:** General Purpose Input/Output
- **SPIO:** Special Purpose Input/Output

---


