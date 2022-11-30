import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import json
import urllib3
import sqlite3
urllib3.disable_warnings()

def create_genre_table(movies):
    ''' Create the genre table in the database using the accessed data stored in the file
    
    Parameters
    ----------
    movies: string
        the name of file in which the accessed data is stored

    Returns
    -------
    None
    '''
    # process the original data
    movies_T = pd.read_json(movies)
    movies = pd.DataFrame(movies_T.values.T,columns=movies_T.index,index=movies_T.columns)
    movies['year'] = movies['description'].str[-5:-1]
    
    # get genre table data
    movies_genre = movies.drop(columns = ['description','metacriticRating','starList','plot'])
    
    # create genre table in the database
    conn = sqlite3.connect('sijuntao_si507_final_project.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Genre (imDbRating, imDbRatingVotes, contentRating, genres, id, image, plot_summary, plot_synopsis, runtimeStr, stars, title, year)')
    
    genres_data = []
    movies_genre = movies_genre.reset_index()
    for i in range(0,len(movies_genre)):
        genres_data.append((movies_genre.loc[i,"imDbRating"], movies_genre.loc[i,"imDbRatingVotes"], movies_genre.loc[i,"contentRating"], movies_genre.loc[i,"genres"], movies_genre.loc[i,"id"], movies_genre.loc[i,"image"], movies_genre.loc[i,"plot_summary"], movies_genre.loc[i,"plot_synopsis"], movies_genre.loc[i,"runtimeStr"], movies_genre.loc[i, "stars"],  movies_genre.loc[i, "title"], int(movies_genre.loc[i, "year"])))
    
    c.executemany('INSERT INTO Genre VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', genres_data)
    conn.commit()

def create_voting_table(movies):
    ''' Create the voting table in the database using the accessed data stored in the file
    
    Parameters
    ----------
    movies: string
        the name of file in which the accessed data is stored

    Returns
    -------
    None
    '''
    # process the original data
    movies_T = pd.read_json(movies)
    movies = pd.DataFrame(movies_T.values.T,columns=movies_T.index,index=movies_T.columns)
    movies['year'] = movies['description'].str[-5:-1]
    
    # get genre table data
    movies_voting = movies.drop(columns = ['description','genreList', 'metacriticRating','starList'])
    movies_voting = movies_voting.sort_values('imDbRatingVotes')

    # create genre table in the database
    conn = sqlite3.connect('sijuntao_si507_final_project.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Voting (genres, imDbRating, contentRating, id, imDbRatingVotes, image, plot_summary, plot_synopsis, runtimeStr, stars, title, year)')
    
    voting_data = []
    movies_voting = movies_voting.reset_index()
    for i in range(0,len(movies_voting)):
        voting_data.append((movies_voting.loc[i,"genres"], movies_voting.loc[i,"imDbRating"], movies_voting.loc[i,"contentRating"], movies_voting.loc[i,"id"], movies_voting.loc[i,"imDbRatingVotes"], movies_voting.loc[i,"image"], movies_voting.loc[i,"plot_summary"], movies_voting.loc[i,"plot_synopsis"], movies_voting.loc[i,"runtimeStr"], movies_voting.loc[i, "stars"],  movies_voting.loc[i, "title"], int(movies_voting.loc[i, "year"])))

    c.executemany('INSERT INTO Voting VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', voting_data)
    conn.commit()

def create_rating_table(movies):
    ''' Create the voting table in the database using the accessed data stored in the file
    
    Parameters
    ----------
    movies: string
        the name of file in which the accessed data is stored

    Returns
    -------
    None
    '''
    # process the original data
    movies_T = pd.read_json(movies)
    movies = pd.DataFrame(movies_T.values.T,columns=movies_T.index,index=movies_T.columns)
    movies['year'] = movies['description'].str[-5:-1]
    
    # get genre table data
    movies_rating = movies.drop(columns = ['description','genreList','starList','plot'])
    movies_rating = movies_rating.sort_values('imDbRating')

    # create genre table in the database
    conn = sqlite3.connect('sijuntao_si507_final_project.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Rating (genres,imDbRatingVotes,contentRating, id, imDbRating, image, metacriticRating, plot_summary,plot_synopsis, runtimeStr, stars, title, year)')
    
    rating_data = []
    movies_rating = movies_rating.reset_index()
    for i in range(0,len(movies_rating)):
        rating_data.append((movies_rating.loc[i,"genres"], movies_rating.loc[i,"imDbRatingVotes"], movies_rating.loc[i,"contentRating"], movies_rating.loc[i,"id"], movies_rating.loc[i,"imDbRating"], movies_rating.loc[i,"image"], movies_rating.loc[i,"metacriticRating"], movies_rating.loc[i,"plot_summary"],movies_rating.loc[i,"plot_synopsis"], movies_rating.loc[i,"runtimeStr"], movies_rating.loc[i, "stars"],  movies_rating.loc[i, "title"], int(movies_rating.loc[i, "year"])))

    c.executemany('INSERT INTO Rating VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', rating_data)
    conn.commit()

if __name__=="__main__":
    create_genre_table("data/movies.json")
    create_voting_table("data/movies.json")
    create_rating_table("data/movies.json")

