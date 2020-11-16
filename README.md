# ATX Housing and Rental Pricing

These scripts scrape the web for rental and housing information for analysis as price predictions and forecasting.

<br>

# Setting up the environment the first time

Complications always arise when setting this up for the first time. <br>
So I'm going to *attempt* to standardize this somewhat for me.

Current config under test: 
Windows10pro_prerelease200911-1500 running on WSL2

<br>
<br>

## Need to install an X11 graphical monitor on windows. 
Them Interents recommended [VcXsrv](https://sourceforge.net/projects/vcxsrv/) [Video Instruction](https://www.youtube.com/watch?v=4SZXbl9KVsw) [full writeup](https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/)

install scripts were automated in <code> -install_all.sh</code>

Also have to update firewall permission to allow VcXsrv


## to install the google chrome webdiver ##
## (these steps are likely no longer needed *ignore*)
Step 1 – Add Google Chrome PPA

First, add (if not added already) the Google Chrome repository on your system using the following command. While using PPA to our system we also receive the latest updates whenever you check for system updates.

<code> wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - </code>

Next, create a PPA file for Google chrome on your system by running command:

<code> sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' </code>

Step 2 – Install or Upgrade Google Chrome

After adding the Google Chrome repository in our system use following commands to install the latest Google Chrome stable release. If you already have installed an older version, It will upgrade the currently installed version with the recent stable version.

<code> sudo apt-get update
sudo apt-get install google-chrome-stable </code>