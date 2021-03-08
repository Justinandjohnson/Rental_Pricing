#!/bin/bash

# sudo apt-get update
# sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4

# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo apt install ./google-chrome-stable_current_amd64.deb

# sudo rm google-chrome-stable_current_amd64.deb


grome=$(google-chrome --version | awk '{print $3}')
echo $grome

eval "chromedriver --version"


link1="https://chromedriver.storage.googleapis.com/"
echo $link1
link2="/chromedriver_linux64.zip"
echo $link2
vers="$grome"
echo $vers
concat_link="$link1$vers$link2"
echo $concat_link

# google-chrome --version | grep -iE "[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}" 

# this website returns latest webdriver version:
# https://chromedriver.storage.googleapis.com/LATEST_RELEASE


wget $concat_link
# unzip chromedriver_linux64.zip
# sudo mv chromedriver /usr/bin/chromedriver
# sudo chown root:root /usr/bin/chromedriver
# sudo chmod +x /usr/bin/chromedriver
