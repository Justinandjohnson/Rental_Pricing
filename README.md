# ATX Housing and Rental Pricing
A tool for scraping rental and housing prices for making models, analysis and forecasts.

# Contents
* [Logic](#Logic)
* [Issues](#Need-to-install-an-X11-graphical-monitor-on-windows)
* [X server](#)
* [Chrome WebDriver](#Chrome-WebDriver)
* [X server](#)
* [TODO](#TODO)


# Logic 
For each city instantiate a crawler that
1) Finds urls for each listing
2) Scrapes each url
3) Save relivent information
4) Model and visualize the data


# X Server 
I've played with the following two options (not the focus of this repo)
## VcXsrv
[VcXsrv](https://sourceforge.net/projects/vcxsrv/) 
[Video-Instruction](https://www.youtube.com/watch?v=4SZXbl9KVsw) 
[full-writeup](https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/)

install scripts were automated into 
```bash 
install_all.sh
```
Also have to update firewall permission to allow VcXsrv

## x410
Also plays well with Windows 10, availible in app store, need to update firewall permissions as well
<br>

# Chrome WebDriver
[Web Instruction](https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/)

```
sudo apt-get update
sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```
Get the version, match this to the Chrome WebDriver
```
google-chrome --version
```
Install the corresponding WebDriver
```
wget https://chromedriver.storage.googleapis.com/<chrome version>/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```
<br></br>
# Chrome WebDriver Updates
Step 1 – Add Google Chrome PPA
```
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
````
Step 2 - create a PPA file for Google chrome on your system by running command:
```
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
```
Step 3 – Install or Upgrade Google Chrome
``` 
sudo apt-get update
sudo apt-get install google-chrome-stable 
```
# TODO

* [ ] Create exception for reCaptcha
* [ ] Add visuals
* [ ] Clean common repo
* [ ] Add Housing details
* [ ] Refactor
* [ ] Add more resources Zillow, etc.