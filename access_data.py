import json
import requests
import pandas as pd


# IMDB API key:  k_66b27k2j
# TMDB API key:  ab73627f9c3987b1a25b1d8d74950754
# OMDB API key:  a8c49e75

if __name__=="__main__":
    # get the primary movies data using IMDB API
    base_url_imdb = 'https://imdb-api.com/API/AdvancedSearch/'
    imdb_params = { 
                "apiKey": "k_66b27k2j",
                "title_type": "feature,tv_movie,short&release_date",
                "release_date": "2010-01-01,2017-01-01",
                "count": 250,
                }
    imdb_response = requests.get(base_url_imdb, imdb_params)

    imdb_params1 = { 
                "apiKey": "k_66b27k2j",
                "title_type": "feature,tv_movie,short&release_date",
                "release_date": "2010-01-01,2017-01-01",
                "count": 250,
                "sort": "num_votes,desc"
                }
    imdb_response1 = requests.get(base_url_imdb, imdb_params1)


    imdb_raw = imdb_response.json()["results"] + imdb_response1.json()["results"]
    imdb_data = []
    for i in imdb_raw:
        if(i not in imdb_data):
            imdb_data.append(i)

    with open('data/movies.json', 'w+') as output_file:
        json.dump(imdb_data, output_file, indent=4, sort_keys=True)


    # get the detailed movies data by combining the primary movies data with the dataset obatined from Kaggle
    pri_data = pd.read_json("data/movies.json")
    reviews = pd.read_json("data/IMDB_movie_details.json", lines= True)

    det_data = pd.merge(pri_data, reviews[['movie_id','plot_summary','plot_synopsis']],left_on = 'id',right_on = 'movie_id')
    det_data = det_data.drop(columns = ['movie_id'])

    final = {}
    for i in range(0, len(det_data)):
        temp = det_data.loc[i].to_dict()
        final[temp['id']] = temp

    with open('data/movies.json', 'w+') as output_file:
        json.dump(final, output_file, indent=4, sort_keys=True)