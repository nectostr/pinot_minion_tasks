# Collective repo for minions tasks for PINOT project
## 1. Youtube QoE data collection
Linux system required
### 1. Selenium-based watcher
#### Extensions
1. stats-fo-nerds collector in repo as "chrome_extension" crx-ed by link below
2. AddBlock should be loaded (I used the way to install extension on chrome in real pc and then copy folder)
See https://chrome.google.com/webstore/category/extensions and Adblock for Youtube™ and https://maketecheasier.com/download-save-chrome-extension/ 
#### Chrome driver
Installed from https://chromedriver.chromium.org/home
Added to bin folder
### 2. FastAPI data collector
Module that host API server and dumps data coming from extension in spec files
## 2. Pcap collection
Two functions that starts tcpdump util collection and stops it via name or previous generated id