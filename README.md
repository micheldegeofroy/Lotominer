# BTCLOTO Bitcoin Solo Miner on Raspberry Pi 4

## V2 (2025)

**by Michel de Geofroy**

This script provides a basic setup for running a Bitcoin solo miner on a Raspberry Pi 4.

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

- Check bot security
- Option for solo pool mining (no need for a full node)
- Option to add/remove watch-only wallet on node
- Change BTC wallet bot function
- Flash lights if wallet changes
- Send alert if external HD is nearly full
- Send message if BTC mined
- Change monitored address function

---

## GPIO Pinout for Raspberry Pi 4

```
GPIO READALL

+-----+-----+-------------------+------+---+---Pi 4B--+---+------+--------------------+-----+-----+
| BCM | wPi |        Name       | Mode | V | Physical | V | Mode |         Name       | wPi | BCM |
+-----+-----+-------------------+------+---+----++----+---+------+--------------------+-----+-----+
[...Full GPIO table as provided above...]
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


