import webbrowser
import sqlite3
import json
import pandas as pd
import plotly.graph_objects as go
import tweepy
import process_data as pro_d


def get_genre_list():
    ''' Get the genre list that the user can select to query
    
    Parameters
    ----------
    None

    Returns
    -------
    genre_list: list
        A list which contains all the genres that can select from
    '''
    # connect to database
    conn = sqlite3.connect('sijuntao_si507_final_project.db')
    c = conn.cursor()
    c.execute(''' SELECT genres FROM Genre ''')
    
    # create the dataframe using the table in database
    data_columns = []
    for i in c.description:
        data_columns.append(i[0])
    data = c.fetchall()
    frame = pd.DataFrame(data,columns = data_columns)
    
    # get the genre list
    frame['genres'] = frame['genres'].str.split(', ')
    frame = frame.explode('genres')
    return list(frame['genres'].unique())


def display_result(search_q, graph, num = 5):
    '''
    Display basic information of mavies based on search query
    
    Parameters
    ----------
    search_q: string
        the search query
    graph: dict
        the graph that stores the corresponding movies
    num: int
        the num of movies returned in the id_list
    
    Returns
    -------
    id_list: list
        A list which contains the searched movies' ids
    '''
    print('\n')
    i = 1
    top = list(graph['nodes'].keys())[0:num]
    id_list = []
    for key in top:
        print(i, graph['nodes'][key]['title'], '('+str(graph['nodes'][key]['year'])+')')
        id_list.append(key)
        i += 1
    print('\n')
    return id_list


def valid_YN(user_input):
    '''
    Check the validation of user input
    
    Parameters
    ----------
    user_input: user's input
    
    Returns
    -------
    string: "yes", "no" or "invalid"
    '''
    if user_input.lower() == "yes" or user_input.lower() == "y":
        return "yes"
    elif user_input.lower() == "no" or user_input.lower() == "n":
        return "no"
    else:
        return "invalid"


def check_detail_info(search_q, id_list, graph):
    '''
    let user choose to check specific moive information
    or all of the moive information
    
    Parameters
    ----------
    search_q: string
        the search query
    id_list: list
        the list that contains selected movie id in graph
    graph: dict
        the graph that contains the detailed information of the movies
    
    Returns
    -------
    None
    '''
    user_choice = input("\nWould you like to view detailed information?\nReply the index of moive or 'all' to view. Reply 'no' to next step: ")
#     user_choice = 'all'

    while True:
        if user_choice == 'no':
            return
        else:
            see_synopsis = input("\nWould you like to see detailed plot synopsis? (Y/N): ")
            while valid_YN(see_synopsis) == "invalid":
                see_synopsis = input("\nWould you like to see detailed plot synopsis? (Y/N): ")
            see_synopsis = valid_YN(see_synopsis)
        
            if user_choice == 'all':
                display_detail(search_q, id_list, graph, see_synopsis)
            else:
                display_detail(search_q, [id_list[int(user_choice)-1]], graph, see_synopsis)
        
        # check if the user want to see other search results' information
        user_choice = input("\nWould you like to view other search results' detailed information?\nReply the index of moive or 'all' to view. Reply 'no' to next step: ")


def display_detail(search_q, id_list, graph, see_synopsis):
    '''
    Display basic information of mavies based on search result
    
    Parameters
    ----------
    search_q: string
        the search query
    id_list: list
        the list that contains selected movie id in graph
    graph: dict
        the graph that contains the detailed information of the movies
    see_synopsis: string
        whether the user want to see the detailed plot synopsis
    
    Returns
    -------
    None
    '''

    print("Directed to the detailed information page...\n")

    text = '''
    <html>
    <body>
    <ol>
    '''
    
    for id in id_list:
        summary = graph['nodes'][id]['plot_summary'] if id in graph['nodes'].keys() else "Not Available"
        synopsis = graph['nodes'][id]['plot_synopsis'] if id in graph['nodes'].keys() else "Not Available"
        try:
            if(see_synopsis == 'yes'):
                text += '''
                <h2><li>
                    {title} ({Year})</h2>
                    <br>
                    <img src={img_url} style="float: center; height: 550px; width: 400px;">
                    <br>
                    <p><b>Runtime:</b> {Runtime}</p>
                    <p><b>Genre:</b> {Genre}</p>
                    <p><b>Actors:</b> {Actors}</p>
                    <p><b>Content Rating:</b> {contentRating}</p>
                    <p><b>IMDB Rating Votes:</b> {imDbRatingVotes}</p>
                    <p><b>IMDB Rating:</b> {imdbRating}</p>
                    <p><b>Plot Summary:</b> {plot_summary}</p>
                    <p><b>Plot Synopsis:</b> {plot_synopsis}</p>
                    <br></br>
                </li>
                '''.format(
                    title = graph['nodes'][id]['title'],
                    Year = graph['nodes'][id]['year'],
                    img_url = graph['nodes'][id]['image'], 
                    Runtime = graph['nodes'][id]['runtimeStr'],
                    Genre = graph['nodes'][id]['genres'],
                    Actors = graph['nodes'][id]['stars'],
                    contentRating = graph['nodes'][id]['contentRating'],
                    imDbRatingVotes = graph['nodes'][id]['imDbRatingVotes'],
                    imdbRating = graph['nodes'][id]['imDbRating'],
                    plot_summary = summary,
                    plot_synopsis = synopsis,
                )
            else:
                text += '''
                <h2><li>
                    {title} ({Year})</h2>
                    <br>
                    <img src={img_url} style="float: center; height: 550px; width: 400px;">
                    </br>
                    <p><b>Runtime:</b> {Runtime}</p>
                    <p><b>Genre:</b> {Genre}</p>
                    <p><b>Actors:</b> {Actors}</p>
                    <p><b>Content Rating:</b> {contentRating}</p>
                    <p><b>IMDB Rating Votes:</b> {imDbRatingVotes}</p>
                    <p><b>IMDB Rating:</b> {imdbRating}</p>
                    <p><b>Plot Summary:</b> {plot_summary}</p>
                    <br></br>
                </li>
                '''.format(
                    title = graph['nodes'][id]['title'],
                    Year = graph['nodes'][id]['year'],
                    img_url = graph['nodes'][id]['image'], 
                    Runtime = graph['nodes'][id]['runtimeStr'],
                    Genre = graph['nodes'][id]['genres'],
                    Actors = graph['nodes'][id]['stars'],
                    contentRating = graph['nodes'][id]['contentRating'],
                    imDbRatingVotes = graph['nodes'][id]['imDbRatingVotes'],
                    imdbRating = graph['nodes'][id]['imDbRating'],
                    plot_summary = summary,
                )
        except:
            continue


    text += '''
    </ol>
    </body>
    </html>
    '''

    file = open("result/detail_info.html","w")
    file.write(text)
    file.close()

    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open("result/detail_info.html")


def display_plots(key, plot_name, id_list, graph):
    '''
    based on user selected key plot the corresponding visualization
    
    Parameters
    ----------
    key: string
        the plot type
    plot_name: string
        name for the plot
    id_list: list
        the list that contains selected movie id in graph
    graph: dict
        the graph that contains the detailed information of the movies
    
    Returns
    -------
    None
    '''
    all = []
    items = []
    movies = []

    for movie_id in id_list:
        movie_identity = graph['nodes'][movie_id]['title'] + " (" + str(graph['nodes'][movie_id]['year']) + ")"
        if key == "Runtime":
            all.append([int(graph['nodes'][movie_id]['runtimeStr'].split()[0]), movie_identity])
            all.sort()
        elif key == "imdbRating":
            imdbRating = float(graph['nodes'][movie_id]['imDbRating'])
            all.append([imdbRating, movie_identity])
            all.sort()
        else:
            imdbVotes = int(graph['nodes'][movie_id]['imDbRatingVotes'])
            all.append([imdbVotes, movie_identity])
            all.sort()

    items = [item[0] for item in all]
    movies = [item[1] for item in all]
    
    bar_data = go.Bar(x=movies, y=items)
    basic_layout = go.Layout(title=plot_name)
    fig = go.Figure(data=bar_data, layout=basic_layout)

    fig.write_html('result/'+ plot_name + ".html", auto_open=True)


def get_tweets(id_list, graph):
    '''
    get the popular tweets for the selected moive data based on user's choice
    
    Parameters
    ----------
    id_list: list
        the list that contains selected movie id in graph
    graph: dict
        the graph that contains the detailed information of the movies
    
    Returns
    -------
    tweet_content: dict
        the dict which stores the tweets for the movies. key: movie_id, value: tweets
    '''
    # these will be in your Twitter develop api page
    # https://developer.twitter.com/en/portal/products/elevated

    # API key
    consumer_key="cH6UD66SHtvUsqnXx0NTYsZoH"
    consumer_secret="hiK9BTxdCYzGae3RQNjd9UCS7lgsmZdqkxZNQXCbGk8lR96lOw"
    access_token_key="1570516091084091392-0G9hOSzJcg3rvSco4gfxOpJQWRo1tQ"
    access_token_secret="n7Z3z6525SNnbnPTZ6VMGfccPCos2RGO6XqDceFvTBD55"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)
    
    # load cache
    try:
        tweet_file = open('data/tweet_cache.json', 'r')
        tweet_cache = json.loads(tweet_file.read())
        tweet_file.close()
    except:
        tweet_cache = {}
    

    # search for movie-related tweets
    tweet_content = {}
    for movie_id in id_list:
        # if cached, directly load
        if movie_id in tweet_cache.keys():
            tweet_content[movie_id] = tweet_cache[movie_id]
        else:
            # if not cached, then use API
            tweet_content[movie_id] = []
            tt = api.search_tweets("movie AND "+ str(graph['nodes'][movie_id]['title']), tweet_mode="extended")
            temp = [i.full_text for i in tt]
            for j in temp:
                if j not in tweet_content[movie_id]:
                    tweet_content[movie_id].append(j)
            tweet_cache[movie_id] = tweet_content[movie_id]
    
    # update cache
    with open('data/tweet_cache.json', 'w+') as tweet_file:
        json.dump(tweet_cache, tweet_file, indent=4)
    
    return tweet_content


def display_tweets(tweet_content, graph):
    '''
    display the popular tweets for the selected moive data based on user's choice
    
    Parameters
    ----------
    tweet_content: dict
        a dict that saves the tweets related to each user selected movies
    graph: dict
        the graph that contains the detailed information of the movies
    
    Returns
    -------
    None
    '''
    # see tweets in html
    print("Directed to the tweets information page...\n")

    text = '''
    <html>
    <body>
    <ol>
    '''
    
    for id in tweet_content.keys():
        movie_tweets = ''
        i = 1
        for tweet in tweet_content[id]:
            movie_tweets += ('<br>' + str(i) + '. ' + tweet + '</br>')
            i += 1
        try:
            text += '''
             <h2><li>
                {title} ({Year})</h2>
                <p><b>Related Tweets:</b></p>
                <p>{Tweet_content}</p>
                <br></br>
                </li>
                '''.format(
                    title = graph['nodes'][id]['title'],
                    Year = graph['nodes'][id]['year'],
                    Tweet_content = movie_tweets, 
                )
        except:
            continue


    text += '''
    </ol>
    </body>
    </html>
    '''

    file = open("result/tweets_info.html","w")
    file.write(text)
    file.close()

    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open("result/tweets_info.html")


def visualize(id_list, graph):
    '''
    plot the selected moive data visualization based on user's choice
    
    Parameters
    ----------
    id_list: list
        the list that contains selected movie id in graph
    graph: dict
        the graph that contains the detailed information of the movies
    
    Returns
    -------
    None
    '''

    user_choice = input('''
    Please choose the data visualization:
        1. Run Time
        2. IMDB Rating
        3. IMDB Votes \n
    Your Choice: ''')

    while not (user_choice.isnumeric() and 1 <= int(user_choice) and int(user_choice) <= 3):
        user_choice = input('''
    Please choose the data visualization:
        1. Run Time
        2. IMDB Rating
        3. IMDB Votes
    Your Choice: ''')

    print("Directed to data visualization now...")

    if user_choice == '1':
        # runtime
        display_plots('Runtime', 'Movie Run Time', id_list, graph)
    elif user_choice == '2':
        # imdbVotes
        display_plots('imdbRating', 'IMDB Movie Rating', id_list, graph)
    else:
        # rating ranking
        display_plots('imdbVotes', 'IMDB Movie Votes', id_list, graph)


if __name__ == '__main__':
    while True:
    # load the graph data from the cache
        try:
            graph_file = open('data/graph_cache.json', 'r')
            graph_cache = json.loads(graph_file.read())
            graph_file.close()
        except:
            graph_cache = {}
    
        # let user choose search type
        search_type = input("How do you want to search for movies?\nEnter the number you want to search through -- 1: Genre, 2: Rating, 3: Voting: ")
        if search_type == '1':
            # get the genre list
            genre_list = get_genre_list()
        
            # prompt for user search query
            print('\nThe genres you can select to query are as follows: ')
            print('\n'.join(genre_list))
            search_q = input("\nEnter the query to search: ")
        
            # get the genre graph
            if ('Genre'+' - '+ search_q) in graph_cache.keys():
                # if graph data is already in cache
                graph = graph_cache['Genre'+' - '+ search_q]
            else:
                # if not, create the graph
                genre_sn, movies = pro_d.create_genre_source(search_q)
                graph = pro_d.generate_graph(genre_sn, movies)
                graph_cache['Genre'+' - '+ search_q] = graph
    
        elif search_type == '2':
            # get the rating list
            rating_list = {1: 'rating >= 8', 2: '7 <= rating < 8', 3: '6 <= rating < 7', 4: '5 <= rating < 6', 5: 'rating < 5'}
        
            # prompt for user search query
            print('\nThe ratings you can select to query are as follows: ')
            print('''
                1: rating >= 8
                2: 7 <= rating < 8
                3: 6 <= rating < 7
                4: 5 <= rating < 6
                5: rating < 5''')
            search_q = input("\nEnter the number of the category you want to search: ")
        
            # get the genre graph
            if ('Rating'+' - '+ rating_list[int(search_q)]) in graph_cache.keys():
                # if graph data is already in cache
                graph = graph_cache['Rating'+' - '+ rating_list[int(search_q)]]
            else:
                # if not, create the graph
                rating_sn, movies = pro_d.create_rating_source(int(search_q), rating_list[int(search_q)])
                graph = pro_d.generate_graph(rating_sn, movies)
                graph_cache['Rating'+' - '+ rating_list[int(search_q)]] = graph
    
        else:
            # get the voting list
            voting_list = {1: 'voting >= 800000', 2: '600000 <= rating < 800000', 3: '400000 <= voting <600000', 4: '200000 <= voting < 400000', 5: 'voting < 200000'}
        
            # prompt for user search query
            print('\nThe voting you can select to query are as follows: ')
            print('''
                1: voting >= 800000
                2: 600000 <= voting < 800000
                3: 400000 <= voting < 600000
                4: 200000 <= voting < 400000
                5: voting < 200000''')
            search_q = input("\nEnter the number of the category you want to search: ")
        
            # get the genre graph
            if ('Voting'+' - '+ voting_list[int(search_q)]) in graph_cache.keys():
                # if graph data is already in cache
                graph = graph_cache['Voting'+' - '+ voting_list[int(search_q)]]
            else:
                # if not, create the graph
                voting_sn, movies = pro_d.create_voting_source(int(search_q), voting_list[int(search_q)])
                graph = pro_d.generate_graph(voting_sn, movies)
                graph_cache['Voting'+' - '+ voting_list[int(search_q)]] = graph
    
        # update cache
        with open('data/graph_cache.json', 'w+') as graph_file:
            json.dump(graph_cache, graph_file, indent=4)
    
        # display basic information (interactive command line prompt)
        id_list = display_result(search_q, graph, 5)
    
        # check detailed information: cast, image, actors ...
        check_detail_info(search_q, id_list, graph)
    
        # let user choose if to visualize the data
        vis = input("\nWould you like to visualize the information? (Y/N): ")
        while True:
            while valid_YN(vis) == "invalid":
                vis = input("\nWould you like to visualize the information? (Y/N): ")
            vis = valid_YN(vis)
        
            if vis == "yes":
                visualize(id_list, graph)
            else:
                break
            vis = input("\nWould you like to see other visualized information? (Y/N): ")
    
        # let user choose if to see the tweets
        see_tweet = input("\nWould you like to see the tweets about the movies?\nReply the index of moive or 'all' to see. Reply 'no' to next step: ")
        while True:
            if see_tweet == 'all':
                tweets_content = get_tweets(id_list, graph)
                display_tweets(tweets_content, graph)
            elif see_tweet == 'no':
                break
            else:
                tweets_content = get_tweets([id_list[int(see_tweet)-1]], graph)
                display_tweets(tweets_content, graph)
            see_tweet = input("\nWould you like to see the tweets about other movies?\nReply the index of moive or 'all' to see. Reply 'no' to next step: ")
    
        # let use choose if to start another search
        new_search = input("\nWould you want to start a new search? (Y/N): ")
        while valid_YN(new_search) == "invalid":
            new_search = input("\nWould you want to start a new search? (Y/N): ")
        new_search = valid_YN(new_search)
    
        if new_search == "yes":
            continue
        else:
            break

    print("\nGoodbye!\n")
