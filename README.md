# LEA Berlin Appointments

This script continuously search for LEA (Immigration Office) Berlin and sends a telegram notifications


## Install Python and chromium
```
sudo apt-get install python3 python3-pip chromium-chromedriver
```


## Install Dependencies
```
pip3 install selenium telegram-send BeautifulSoup4 chime

```


## Some modifications, as per requirements

### 1. Fix preferred days and months
Edit as per 
```
acceptable_dates = [
    '1', '4','5','6','7','8','9','10',
    '11','12', '13','14','15','16','17','18','19','20'
    '21','22','23','24','25','26','27','28','29','30',
    ]

    acceptable_months = ['July', 'August' ]
```

### 2. Telegram Notifications
Notifications can be received on Telegram by the steps in the following link:

see [How to Write a Telegram Bot to Send Messages with Python](https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580)


In case of error `telegram-send: command not found`
```
sudo pip3 install telegram-send
```


## Run
```
./lea.py

```

## Credit | Inspiration
1. [How I got a residency appointment thanks to Python, Selenium and Telegram](https://rogs.me/2020/08/how-i-got-a-residency-appointment-thanks-to-python-selenium-and-telegram/)


## Note
It solved my issue and worthy to share. 
I am not Python programmer, so MR / PR / feedback is welcome :)