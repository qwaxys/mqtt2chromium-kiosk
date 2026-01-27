# mqtt2chromium-kiosk

Write Armbian_23.08.0-trunk_Bananapi_bookworm_current_6.1.37_xfce_desktop.img to SD card

Go through setup

I used en_IE.UTF-8 and Timezone Europe/Brussels

You should now be logged into the desktop.

Go to Applications -> Settings -> Power Manager

On the tab Display, set everything to Never.

sudo nano /etc/lightdm/lightdm.conf
Find 
```
#autologin-user=
#autologin-user-timeout=0
```
Uncomment both and set it to your username.

sudo apt update && sudo apt upgrade

sudo apt install chromium

