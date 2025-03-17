# Lotominer
Raspberry Pi 4 Solo CPU Bitcoin Miner With Telegram Bot
#
LotoMiner (aka BTCLOTORPI ) A Full Node CPU Solo Mineral Oil Cooled Bitcoin Miner running on a recycled old Raspberry Pi 4 and powered by an old solar array to power it when the sun shines in effect mining bitcoin with the sun. 

This type of mining isn’t novel by any means, and in fact it’s a style of mining is called “lottery mining” where contributing to a pool is omitted in favour of attempting to solve the entire block by pure random chance alone in the hopes that if it’s solved, the entire reward will be claimed by the owner of the device alone. 

Most would say "the probability of mining a block with a RPI 4 is zero" obviously these people don't understand​ that probability zero simply does not exist in this universe and should not confuse probability with possibility. 

In the case of this device at the current hash rate it has under a one-in-two-billion chance of mining a bitcoin block which is basically less chance of winning a lottery.

Some will say its simply wasting electricity which would be correct but in this case the RPI is powered by a solar array with a small battery only meant to give time to the RPI and bitcoind to shutdown when there is no sun and also not go into brown state. 

So the fixed recurring costs are the proportional cost of the internet connection and the electricity the router uses. 

One of the issues has been the device over heating so we decided to dump the RPI and the ssd directly into mineral oil which helps, we also aded a fan to circulate the mineral oil. 

We also added a telegram bot to be able to interact with it, check its sync state initially, check the space on the SSD left, the ability to backup the blockchain if we one day will need to upgrade the ssd and more. 

We also added led lights so that if it our destiny (We don't believe in free choice) to mine a bitcoin block with this contraption the led's would flash and I would receive a telegram bot message.

As closing words we are not into crypto we believe everything except Bitcoin is a shitcoin and that ETH is the mother asshole of all shitcoins as Ammous would say.

We see how mining pools and large corporate or even national actors are dangerously centralising Bitcoin so running a full bitcoin node is our small drop in the ocean to push back. 

To the Question: What are the chances of solo mining a bitcoin block with a raspberry pi 4?

DeepSeek Conclusion: 

The Raspberry Pi 4 would take ~81.7 billion years on average to solo mine a block—longer than the age of the universe (~13.8 billion years). This makes it statistically impossible to succeed. Even with thousands of Pis, the odds remain effectively zero. Bitcoin mining today requires specialized ASICs and participation in mining pools to earn rewards. 

Gork Conclusion: 

The chances of solo mining a Bitcoin block with a Raspberry Pi 4 are approximately 4 × 10⁻¹⁵ per block, meaning you’d expect to wait 4.75 billion years on average for success. This is so improbable that it’s effectively zero for practical purposes. Modern mining is dominated by ASICs with terahashes or petahashes per second, leaving general-purpose devices like the Raspberry Pi 4 infeasible for solo Bitcoin mining. Thus, while theoretically possible, the chances are astronomically small and not worth pursuing. 

Chatgpt Conclusion: 

Solo mining Bitcoin with a Raspberry Pi 4 is technically possible (you can run the mining software and attempt it), but it is for all practical purposes impossible to successfully mine a block. The expected time to find one block is on the order of billions of years, given the Pi’s hash rate versus the enormous Bitcoin network difficulty and hash power. It’s a fun experiment in theory or for educational purposes, but the probability of success is effectively zero. In practice, a Pi-based miner will never generate a block reward in any meaningful timeframe. 

My Conclusion: 

Even AI can not differentiate between chance and probability :) If this rig actually mines a block it will be because the universe conspire for it to be that way. 

If it happens we will take the funds and open a foundation to help children with cancer. 

In Perspective: 

Bitcoin: 

504 attempts/week (6 per hour * 12 * 7 the systems runs on the sun). Each attempt is 3e- 13. So 504 × 3e-13 = 1.512e-10. That's 0.00000001512% chance per week.

EuroMillions: 

1 in 139 million ≈ 7.19e-9, which is 0.000000719% per week. So the lottery is about 48 times more likely (7.19e-9 ÷ 1.512e-10 ≈ 47.5). 

Thus wining the lottery is only roughly 48 times more probable per week, cost much more money, profits the government (50% tax) does not support the Bitcoin network.


GPIO


GPIO READALL
+-----+-----+-------------------+------+---+---Pi 4B--+---+------+--------------------+-----+-----+
| BCM | wPi |        Name       | Mode | V | Physical | V | Mode |         Name       | wPi | BCM |
+-----+-----+-------------------+------+---+----++----+---+------+--------------------+-----+-----+
#  |     |     |             +3.3V |      |   |  1 || 2  |   |      | +5V                |     |     |
#  |   2 |   8 | GPIO 2    SDA   1 |   IN | 1 |  3 || 4  |   |      | +5V                |     |     |
#  |   3 |   9 | GPIO 3    SCL   1 |   IN | 1 |  5 || 6  |   |      | GND  0V            |     |     |
#  |   4 |   7 | GPIO 4    GPCLK 0 |   IN | 1 |  7 || 8  | 0 | ALT5 | GPIO 14    TXD   0 | 15  | 14  |
#  |     |     |           GND  0V |      |   |  9 || 10 | 1 | ALT5 | GPIO 15    RXD   0 | 16  | 15  |
#  |  17 |   0 |           GPIO 17 |   IN | 0 | 11 || 12 | 1 | IN   | GPIO 18    PWM   0 | 1   | 18  |
#  |  27 |   2 |           GPIO 27 |   IN | 0 | 13 || 14 |   |      | GND  0V            |     |     |
#  |  22 |   3 |           GPIO 22 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO 23            | 4   | 23  |
#  |     |     |             +3.3V |      |   | 17 || 18 | 0 | IN   | GPIO 24            | 5   | 24  |
#  |  10 |  12 | GPIO 10 SPIO_MOSI | ALT0 | 0 | 19 || 20 |   |      | GND  0V            |     |     |
#  |   9 |  13 | GPIO  9 SPIO_MISO | ALT0 | 0 | 21 || 22 | 0 | IN   | GPIO 25            | 6   | 25  |
#  |  11 |  14 | GPIO 11 SPIO_SCLK | ALT0 | 0 | 23 || 24 | 1 | OUT  | GPIO 08 SPIO CE0 N | 10  | 8   |
#  |     |     |           GND  0V |      |   | 25 || 26 | 1 | OUT  | GPIO 07 SPIO CE1 N | 11  | 7   |
#  |   0 |  30 | GPIO  0   SDA   0 |   IN | 1 | 27 || 28 | 1 | IN   | GPIO  1    SCL   0 | 31  | 1   |
#  |   5 |  21 | GPIO  5           |   IN | 1 | 29 || 30 |   |      | GND  0V            |     |     |
#  |   6 |  22 | GPIO  6           |   IN | 1 | 31 || 32 | 0 | OUT  | GPIO 12      PWM 0 | 26  | 12  |
#  |  13 |  23 | GPIO 13           |   IN | 0 | 33 || 34 |   |      | GND  0V            |     |     |
#  |  19 |  24 | GPIO 19           |   IN | 0 | 35 || 36 | 0 | IN   | GPIO 16            | 27  | 16  |
#  |  26 |  25 | GPIO 26           |   IN | 0 | 37 || 38 | 0 | IN   | GPIO 20            | 28  | 20  |
#  |     |     |           GND  0V |      |   | 39 || 40 | 0 | IN   | GPIO 21            | 29  | 21  |
#  +-----+-----+-------------------+------+---+----++----+---+------+--------------------+-----+-----+

#
#  DIAGRAM FOR FAN AND LED SETUP
#  +------------------------------RED------------------------------------+
#  |  +---------------------------BLACK--------------------------------+ |
#  |  |                                                                | |
#  |  |              +3.3V (1)  [.] [.] (2)  +5V                     ,,| |,,
#  |  |  GPIO 2    SDA   1 (3)  [.] [.] (4)  +5V -------RED------+   | LED |
#  |  |  GPIO 3    SCL   1 (5)  [.] [.] (6)  GND  0V --BLACK--+  |   '''''''
#  |  |  GPIO 4    GPCLK 0 (7)  [.] [.] (8)  TXD   1          |  |
#  |  +----------- GND  0V (9)  [.] [.] (10) RXD   1          |  +-------------------+
#  +---- GPIO 17           (11) [.] [.] (12) GPIO  1 ------+  |   ,,,,,,,            |
#        GPIO 27           (13) [.] [.] (14) GND  0V       |  +---| N T |            |
#        GPIO 22           (15) [.] [.] (16) GPIO 23       +------| P R |            |
#                    +3.3V (17) [.] [.] (18) GPIO 24          +---| N A |            |
#        GPIO 10 SPIO_MOSI (19) [.] [.] (20) GND              |   |   N |            |
#        GPIO  9 SPIO_MISO (21) [.] [.] (22) GPFS3            |   '''''''            |
#        GPIO 11 SPIO_SCLK (23) [.] [.] (24) MOSI1            +-----BLACK----|'''''''''|
#                  GND  0V (25) [.] [.] (26) MISO1                           |   FAN   |
#        GPIO  0   SDA   0 (27) [.] [.] (28) SCLK1                           |         |
#        GPIO  5           (29) [.] [.] (30) GND                             '''''''''''
#        GPIO  6           (31) [.] [.] (32) GPFS6
#        GPIO 13   PWM   1 (33) [.] [.] (34) GND
#        GPIO 19           (35) [.] [.] (36) GPFS8
#        GPIO 26           (37) [.] [.] (38) GPFS9
#                  GND  0V (39) [.] [.] (40) GPFS10
#
# NOTES
#
# "GND  0V" stands for "Ground"
# "SDA"     stands for "Serial Data Line"
# "SCL"     stands for "Serial Clock Line"
# "TXD"     stands for "Transmit Data"
# "RXD"     stands for "Receive Data"
# "GPCLK"   stands for "General Purpose Clock"
# "GPFS"    stands for "General Purpose Function Select"
# "MOSI"    stands for "Master Out, Slave In"
# "MISO"    stands for "Master In, Slave Out"
# "SCLK"    stands for "Serial Clock"
# "GPIO"    stands for "General Purpose Input, Output"
# "SPIO"    stands for "Special Purpose Input, Output"

