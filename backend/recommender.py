from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from ast import literal_eval
import pandas as pd
import numpy as np

metadata = pd.read_csv("DATASETS/movies_metadata.csv")
ratings = pd.read_csv("DATASETS/ratings.csv")
credits = pd.read_csv("DATASETS/credits.csv")
keywords = pd.read_csv("DATASETS/keywords.csv")
metadata = metadata.iloc[0:10000, :]

keywords["id"] = keywords["id"].astype("int")
credits["id"] = credits["id"].astype("int")
metadata["id"] = metadata["id"].astype("int")
metadata = metadata.merge(credits, on="id")
metadata = metadata.merge(keywords, on="id")


features = ["cast", "crew", "keywords", "genres"]
for feature in features:
    metadata[feature] = metadata[feature].apply(literal_eval)


def get_director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return np.nan


def get_list(x):
    if isinstance(x, list):  # checking to see if the input is a list or not
        names = [i["name"] for i in x]  # if we take a look at the data, we find that
        # the word 'name' is used as a key for the names actors,
        # the actual keywords and the actual genres

        # Check if more than 3 elements exist. If yes, return only first three.
        # If no, return entire list. Too many elements would slow down our algorithm
        # too much, and three should be more than enough for good recommendations.
        if len(names) > 3:
            names = names[:3]
        return names

    return []


metadata["director"] = metadata["crew"].apply(get_director)

features = ["cast", "keywords", "genres"]
for feature in features:
    metadata[feature] = metadata[feature].apply(get_list)

metadata[["title", "cast", "director", "keywords", "genres"]].head()


def clean_data(x):
    if isinstance(x, list):
        # cleaning up spaces in the data
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        # Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ""


# Apply clean_data function to your features.
features = ["cast", "keywords", "director", "genres"]

for feature in features:
    metadata[feature] = metadata[feature].apply(clean_data)


def create_soup(x):
    return (
        " ".join(x["keywords"])
        + " "
        + " ".join(x["cast"])
        + " "
        + x["director"]
        + " "
        + " ".join(x["genres"])
    )


metadata["soup"] = metadata.apply(create_soup, axis=1)


def get_genres():
    genres = input(
        "What Movie Genre are you interested in (if multiple, please separate them with a comma)? [Type 'skip' to skip this question] "
    )
    genres = " ".join(["".join(n.split()) for n in genres.lower().split(",")])
    return genres


def get_actors():
    actors = input(
        "Who are some actors within the genre that you love (if multiple, please separate them with a comma)? [Type 'skip' to skip this question] "
    )
    actors = " ".join(["".join(n.split()) for n in actors.lower().split(",")])
    return actors


def get_directors():
    directors = input(
        "Who are some directors within the genre that you love (if multiple, please separate them with a comma)? [Type 'skip' to skip this question] "
    )
    directors = " ".join(["".join(n.split()) for n in directors.lower().split(",")])
    return directors


def get_keywords():
    keywords = input(
        "What are some of the keywords that describe the movie you want to watch, like elements of the plot, whether or not it is about friendship, etc? (if multiple, please separate them with a comma)? [Type 'skip' to skip this question] "
    )
    keywords = " ".join(["".join(n.split()) for n in keywords.lower().split(",")])
    return keywords


def get_searchTerms():
    searchTerms = []
    genres = get_genres()
    if genres != "skip":
        searchTerms.append(genres)

    actors = get_actors()
    if actors != "skip":
        searchTerms.append(actors)

    directors = get_directors()
    if directors != "skip":
        searchTerms.append(directors)

    keywords = get_keywords()
    if keywords != "skip":
        searchTerms.append(keywords)

    return searchTerms


def make_recommendation(metadata=metadata, searchTerms=["skip"] * 4):
    new_row = metadata.iloc[-1, :].copy()
    new_row.iloc[-1] = " ".join(searchTerms)  # adding the input to our new row
    print(searchTerms)
    metadata = metadata.append(new_row)
    count = CountVectorizer(stop_words="english")
    count_matrix = count.fit_transform(metadata["soup"])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    sim_scores = list(enumerate(cosine_sim2[-1, :]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    ranked_titles = []
    for i in range(1, 11):
        indx = sim_scores[i][0]
        ranked_titles.append(
            [metadata["title"].iloc[indx], metadata["imdb_id"].iloc[indx]]
        )

    return ranked_titles


# print(make_recommendation())
