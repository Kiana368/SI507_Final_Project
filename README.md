# SI507 Final Project

## Introduction & Instructions

This project aims to build a movie searching system. Based on the genre, rating and	voting requirement the	 user	 given,	the	 system	 can	 display the preferred	movies between	 2010-2017. The	 details of	 the	 selected	movie and the tweets	related	to	that	movie can be shown according to the user's choice.

**1. How to get API Keys:**
- Get the IMDB API key here:[ https://imdb-api.com/API](https://imdb-api.com/API). Register an account and apply a key. Then the API key will be sent by email.
- Get the Twitter API key here: [https://developer.twitter.com/en/portal/products/elevated](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api). 
    - Sign up for Twitter Developer Portal
    - Create and name your project
    - Save your keys & tokens

**2. Steps before running the code:**
- Replace the IMDB API key with your keys in access_data.py
- Replace the Twitter keys & tokens in main.py
- Run the 3 python files in order:
    `python access_data.py`
    `python store_data.py`
    `python process_data.py`


**3. How to interact with this program:**
- Run the file: `python main.py`
- Enjoy the movie search by inputting your query and interactive option in the command-line tool



## Required packages and software:
**Packages:**
- webbrowser
- sqlite3
- Plotly
- tweepy
- pandas
- requests

**Software:**
- Chrome Web Browser
