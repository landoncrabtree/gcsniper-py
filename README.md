# gcsniper-py
A Minecraft username sniper that supports giftcards, written with Python.

## Usage:
1. Download `gcsniper-py` via `git clone https://github.com/landoncrabtree/gcsniper-py.git`.
2. Install dependencies via `pip install -r requirements.txt`.
3. Run the program via `python3 sniper.py` or `py sniper.py`.
4. Enter the desired username.
5. Enter the bearer token (See below on how to find it.)
6. Enter a snipe delay (See below on how to use it.)

## Finding Microsoft Bearer Token
First, you will need to create a Microsoft account if you have not done so already. Once created, visit https://www.minecraft.net/en-us/login?return_url=/en-us/profile/redeem and redeem the gift card you have. When prompted to create your profile, do **not** fill it out. Rather, exit the page. This will create a Microsoft account with the redeemed gift card, and thus, you can snipe onto it. If you create a profile, you will not be able to pre-name snipe.

1. Login to the Microsoft account at https://www.minecraft.net/en-us/profile/
2. Navigate to Developer Tools (Inspect Element)
3. Find the bearer_token in the Storage tab.
![Storage Tab](https://i.imgur.com/3fsq3TJ.png)

## Finding a snipe delay
Snipe-delay is the time (in ms) that the program will send a request *before* the name drops. If the name drops at 12:00:00.000, and you chose an offset of 1000, the sniper will send a request at 11:59:59.000 (one second before 12:00). Start with a delay off 100, and go from there. If you notice the requests are being received after drop-time, increase your delay. If they are being received before drop-time, decrease your delay. It is trial and error to find a good delay. Important factors to consider: Your machine's ping to the Minecraft API and the amount of other users who will be trying to snipe the username.

1. Test Minecraft API Ping: `curl -o /dev/null -s -w 'Total: %{time_total}s\n'  https://api.minecraftservices.com`
