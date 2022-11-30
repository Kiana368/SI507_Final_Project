
import json
import requests
import csv
import pandas as pd
import sqlite3

class Movie:
    def __init__(self, json):
        self.name = json['title']
        self.runtime = json['runtimeStr']
        self.genres = json['genres'].split(', ')
        self.contentRating = json['contentRating']
        self.rating = json['imDbRating']
        self.votes = json['imDbRatingVotes']
        self.stars = json['stars'].split(', ')
        self.plotSummary = json['plot_summary']
        self.plotSynopsis = json['plot_synopsis']
        self.image = json['image']
        self.year = json['year']
        self.imdb_id = json['id']

class Source:
    def __init__(self, source_type, name):
        self.source_type = source_type
        self.name = name
        self.connectedTo = []

    def addNeighbor(self, movie_id):
        self.connectedTo.append(movie_id)
        
    def getType(self):
        return self.source_type
        
    def getName(self):
        return self.name

    def getConnections(self):
        return self.connectedTo


def create_genre_source(movie_genre):
    ''' Create the genre source node using the data from the database
    
    Parameters
    ----------
    movie_genre: string
        the name of the genre

    Returns
    -------
    genre_sn: Source object
        A genre-type 'Source' object
    movies: dict
        A dict which contains the details of the movies.
    '''
    # connect to database
    conn = sqlite3.connect('sijuntao_si507_final_project.db')
    c = conn.cursor()
    c.execute(''' SELECT * FROM Genre ''')
    
    # create DataFrame using the table in database
    data_columns = []
    for i in c.description:
        data_columns.append(i[0])
    data = c.fetchall()
    frame = pd.DataFrame(data,columns = data_columns)
    frame = frame[frame['plot_synopsis'].str.len()>0].reset_index().drop(columns = ['index'])
    
    # create the dict which contains the movie details
    movies = {}
    for i in range(0, len(frame)):
        temp = frame.loc[i].to_dict()
        movies[temp['id']] = temp
        
    # create movie objects
    movie_objs = []
    for key in movies.keys():
        movie_obj = Movie(movies[key])
        movie_objs.append(movie_obj)

    # create genre source node
    genre_sn = Source("Genre", movie_genre)
    for obj in movie_objs:
        if movie_genre in obj.genres:
            genre_sn.addNeighbor(obj.imdb_id)
    return genre_sn, movies

def create_rating_source(rating_type, rating_name):
    ''' Create the rating source node using the data from the database
    
    Parameters
    ----------
    rating_type: int
        the number which indicates the type of the rating
            1: >=8
            2: >=7 <8
            3: >=6 <7
            4: >=5 <6
            5: <5
    rating_name: string
        the requirement of the movies in terms of rating

    Returns
    -------
    rating_sn: Source object
        A rating-type 'Source' object
    movies: dict
        A dict which contains the details of the movies.
    '''
    # connect to database
    conn = sqlite3.connect('sijuntao_si507_final_project.db')
    c = conn.cursor()
    c.execute(''' SELECT * FROM Rating ''')
    
    # create DataFrame using the table in database
    data_columns = []
    for i in c.description:
        data_columns.append(i[0])
    data = c.fetchall()
    frame = pd.DataFrame(data,columns = data_columns)
    frame = frame[frame['plot_synopsis'].str.len()>0].reset_index().drop(columns = ['index'])
    
    # create the dict which contains the movie details
    movies = {}
    for i in range(0, len(frame)):
        temp = frame.loc[i].to_dict()
        movies[temp['id']] = temp
        
    # create movie objects
    movie_objs = []
    for key in movies.keys():
        movie_obj = Movie(movies[key])
        movie_objs.append(movie_obj)
    
    # create rating source node
    rating_sn = Source('Rating', rating_name)
    for obj in movie_objs:
        if rating_type == 1:
            if obj.rating >= 8:
                rating_sn.addNeighbor(obj.imdb_id)
        elif rating_type == 2:
            if obj.rating>=7 and obj.rating<8:
                rating_sn.addNeighbor(obj.imdb_id)
        elif rating_type == 3:
            if obj.rating>=6 and obj.rating<7:
                rating_sn.addNeighbor(obj.imdb_id)
        elif rating_type == 4:
            if obj.rating>=5 and obj.rating<6:
                rating_sn.addNeighbor(obj.imdb_id)
        else:
            if obj.rating<5:
                rating_sn.addNeighbor(obj.imdb_id)
    return rating_sn, movies

def create_voting_source(voting_type, movie_voting):
    ''' Create the rating source node using the data from the database
    
    Parameters
    ----------
    voting_type: int
        the number which indicates the type of the voting
            1: >= 800000
            2: >=600000 <800000
            3: >=400000 <600000
            4: >=200000 <400000
            5: <200000
    voting_name: string
        the requirement of the movies in terms of voting

    Returns
    -------
    voting_sn: Source object
        A voting-type 'Source' object
    movies: dict
        A dict which contains the details of the movies.
    '''
    # connect to database
    conn = sqlite3.connect('sijuntao_si507_final_project.db')
    c = conn.cursor()
    c.execute(''' SELECT * FROM Voting ''')
    
    # create DataFrame using the table in database
    data_columns = []
    for i in c.description:
        data_columns.append(i[0])
    data = c.fetchall()
    frame = pd.DataFrame(data,columns = data_columns)
    frame = frame[frame['plot_synopsis'].str.len()>0].reset_index().drop(columns = ['index'])
    
    # create the dict which contains the movie details
    movies = {}
    for i in range(0, len(frame)):
        temp = frame.loc[i].to_dict()
        movies[temp['id']] = temp
        
    # create movie objects
    movie_objs = []
    for key in movies.keys():
        movie_obj = Movie(movies[key])
        movie_objs.append(movie_obj)
    
    # create voting source node
    voting_sn = Source("Voting", movie_voting)
    for obj in movie_objs:
        if voting_type == 1:
            if obj.votes >= 800000:
                voting_sn.addNeighbor(obj.imdb_id)
        elif voting_type == 2:
            if obj.votes>=600000 and obj.votes<800000:
                voting_sn.addNeighbor(obj.imdb_id)
        elif voting_type == 3:
            if obj.votes>=400000 and obj.votes<600000:
                voting_sn.addNeighbor(obj.imdb_id)
        elif voting_type == 4:
            if obj.votes>=200000 and obj.votes<400000:
                voting_sn.addNeighbor(obj.imdb_id)
        else:
            if obj.rating<200000:
                voting_sn.addNeighbor(obj.imdb_id)
    return voting_sn, movies


def generate_graph(sn, movies):
    ''' Create the graph with the given source node
    
    Parameters
    ----------
    sn: 'Source' object
        A 'Source' object which is used as source node to generate a graph
    movies: dict
        A dict which stores the information of movies. key is the imdb_id and value is the movie details

    Returns
    -------
    graph: dict
        A dict which contains the graph of the source node
    '''
    graph = {}
    graph['source_type'] = sn.source_type
    graph['name'] = sn.name
    graph['nodes'] = {}
    for movie_id in sn.getConnections():
        graph['nodes'][movie_id] = movies[movie_id]
    return graph

# if __name__=="__main__":
#     rating_sn, movies = create_rating_source(1, "rates over 8")
#     rating_graph = generate_graph(rating_sn, movies)
#     len(rating_graph['nodes'])

