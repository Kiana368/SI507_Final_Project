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

## Data Structure
All my data is stored as graph structures in separate JSON files from the different data source.

**Construct graph:**

In `process_data.py`, there are several classes and functions for constructing graphs.

- Class _Movie_: use the information of the movie to initialize an object of _Movie_. The details are stored in the attributes, such as _runtime_, _genres_, etc.
- Class _Source_: the source node of the graph, has functions _addNeighbor()_, _getType()_, _getName()_ and _getConnections()_. 
- Function _create_genre_source()_, _create_rating_source()_ and _create_voting_source()_: generate an instance of class _Source_ as the center node of the graph using the data stored in the database
- Function _generate_graph()_: generate a graph by connecting the instances of class _Movie_ to the previous generated center node 

**Graph storage:**
- `graph_cache.json`: JSON file contains detailed movie information stored in the graph structure. The graphs are created and cached according to the user input query
- `tweet_cache.json`: JSON file contains movie id and its relevant tweets, stored in the graph structure

**Read graph:**

In `main.py`, the json of the graphs are read from the cache in the main function.

- movie data: the json of the graphs which contains the movie data will be read from `graph_cache.json`. It will then be updated by adding a new graph if the user's query required.
- tweet data: the json of the graphs which contains the tweet data will be read from `tweet_cache.json`. It will be updated by adding the tweets for a newly searched movie.

## Interaction Instructions
To interact with this program, just simply run the main.py after finishing all the steps before running as described in README. 
1.	First, the program will ask users to enter the category they want to search through in the command window, choosing between “genres”, “ratings” and “votes”. 
2.	According to the category user type in, the further selection options will be given. For example, if the user chooses “genres”, then a list of genre names will be printed and user will need to choose one. After choosing, the names of 5 movies will be presented.
3.	The program will then ask users to choose which movie details to display and select between need spoiled content or not. After choosing, the detailed information of the selected movie will be presented in a HTML window opened in the browser. 
4.	Then, user can choose which data visualization to display. The program will prompt four options for user to choose, three for plotting the comparison of runtime, IMDb rating, and votes, one for presenting the relevant tweets for these movies. The visualizations are all presented in HTML windows opened in the browser.
5.	Finally, the program will ask if the users want to start a new search. If so, then go to Step 1 and repeat the workflow.
