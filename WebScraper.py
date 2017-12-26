from Vertex import Vertex
from Graph import Graph
import requests
from bs4 import BeautifulSoup
import re
import datetime
import logging
import json


'''
gets all the movies from Wikipedia's List of Highest Grossing Films
:returns a list of movie tuples in the form (movie title, movie wikipedia url, gross income, release year)
'''
def get_wikipedia_movies():
    # start the logging
    logging.info('Starting get_wikipedia_movies() ' + str(datetime.datetime.now()))
    url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"

    # check if url is valid
    try:
        req = requests.get(url)
    except:
        logging.error("get_wikipedia_movies requests failed!")

    soup = BeautifulSoup(req.content, 'lxml')
    table_classes = {"class": ["sortable", "plainrowheaders"]}
    tables = soup.findAll("table", table_classes)

    # this will store all the movies scraped
    movie_collection = []

    movie_title = None
    movie_url = None
    gross_income = None
    movie_release_year = None

    logging.info('get_wikipedia_movies() first table search ' + str(datetime.datetime.now()))

    # first table in wikipedia page
    for i, table in enumerate(tables[0].findAll("tr")):
        if i > 0:
            cells = table.findAll(["th", "td"])
            if len(cells) > 1 and cells[2]:
                gross_income_text = cells[3].get_text()
                if gross_income_text != '':
                    gross_income = float(re.sub("[^0-9]", "", gross_income_text))
                else:
                    gross_income = 0
                movie_release_year = cells[4].get_text()
                get_i = cells[2].find('i')
                if get_i:
                    movie_title = get_i.find('a')['title']
                    movie_url = 'https://en.wikipedia.org' + get_i.find('a')['href']

                if movie_title and movie_url and gross_income and movie_release_year:
                    logging.info('adding ' + movie_title + ' to movie collection ' + str(datetime.datetime.now()))
                    movie_collection.append((movie_title, movie_url, gross_income, movie_release_year))

    logging.info('get_wikipedia_movies() second table search' + str(datetime.datetime.now()))
    # second table in wikipedia page
    for i, table in enumerate(tables[2].findAll("tr")):
        if i > 0:
            cells = table.findAll(["th", "td"])
            if len(cells) > 1 and cells[1]:
                cell_text = cells[2].get_text()
                if "♠" in cell_text:
                    ok = cell_text.split("♠")
                    if len(ok) == 2:
                        gross_income_text = ok[1]
                        if gross_income_text != '':
                            gross_income = float(re.sub("[^0-9]", "", gross_income_text))
                        else:
                            gross_income = 0
                if len(cells[0].get_text()) <= 4:
                    movie_release_year = cells[0].get_text()
                get_i = cells[1].find('i')
                if get_i:
                    movie_title = get_i.find('a')['title']
                    movie_url = 'https://en.wikipedia.org' + get_i.find('a')['href']
                if movie_title and movie_url and gross_income and movie_release_year:
                    logging.info('adding ' + movie_title + ' to movie collection ' + str(datetime.datetime.now()))
                    movie_collection.append((movie_title, movie_url, gross_income, movie_release_year))
                else:
                    logging.warning("movie attribute empty")

    logging.info('Finished get_wikipedia_movies() ' + str(datetime.datetime.now()))
    return list(set(movie_collection))


'''
Finds all the actors from the highest grossing films wikipedia page
by visiting each movie's url and scraping the infobox for the cast
:return List of (actors, income from given movie)
'''
def actors_list(movie_url, gross_income):
    actors = []
    try:
        response = requests.get(movie_url)
    except:
        logging.error("actors_list requests failed!")

    soup = BeautifulSoup(response.text, 'lxml')

    infobox = soup.find('table', class_='infobox vevent')
    if infobox:
        stars = infobox.find('th', text='Starring')
        stars = stars.next_sibling.next_sibling

        # i will store the rank of the actor
        i = 1
        for star in stars.find_all('a'):
            actor = star.get_text()

            # higher ranked actors will get a larger amount of the income
            income = int(gross_income) / (2 * i)

            actor_url = 'https://en.wikipedia.org' + star['href']
            age = actor_age(actor_url)
            logging.info('adding ' + actor + ' to graph ' + str(datetime.datetime.now()))
            actors.append((actor, income, age))
            i += 1

    return actors

'''
helper function for the actors_list()
to visit the actor's wikipedia url and scrape the age
'''
def actor_age(actor_url):
    age = '0'

    try:
        response = requests.get(actor_url)
        soup = BeautifulSoup(response.text, 'lxml')
        born = soup.find('span', class_='noprint ForceAgeToShow')
        if born:
            age = str(int(re.sub("[^0-9]", "", born.get_text())))
    except:
        logging.error("actor_age requests failed!")

    return age

'''
Create a graph of all the data scraped
vertices are the movies and actors
a movie has edges to each of its cast members
an actor has an edge to another actor he/she worked with
'''
def createGraph(movie_collection):
    logging.info('Starting creating graph ' + str(datetime.datetime.now()))

    g = Graph()

    for movie_item in movie_collection:
        # movie = tuple of (movie_title, movie_url, gross_income, movie_release_year)
        movie_title = movie_item[0]
        movie_url = movie_item[1]
        gross_income = movie_item[2]
        movie_release_year = movie_item[3]

        # add movie vertex to graph
        # type_is_movie is True since this is a movie
        g.add_vertex(movie_title, movie_release_year, True)

        # get list of the cast of the movie
        actors = actors_list(movie_url, gross_income)

        for actor_item in actors:
            # actor = tuple of (actor name, income from that movie, age)
            actor = actor_item[0]
            actor_income = actor_item[1]
            actor_age = actor_item[2]

            if actor_age == 0:
                break

            # add actor to graph
            # type_is_movie is False since this is an actor
            if actor not in g.get_vertices():
                g.add_vertex(actor, actor_age, False)

            # add edge from actor to the movie
            # weight = income actor earned from movie
            g.add_edge(actor, actor_age, False, movie_title, movie_release_year, True, actor_income)

            # create edge from actor to rest of movie's cast
            # weight = 0 for actor to actor edges
            for edge_actor_item in actors:
                if edge_actor_item[0] != actor_item[0]:
                    edge_actor = edge_actor_item[0]
                    edge_age = edge_actor_item[2]

                    g.add_edge(actor, actor_age, False, edge_actor, edge_age, False, 0)

    logging.info('Finished creating graph ' + str(datetime.datetime.now()))
    return g


'''
Creates a json file from the graph
'''
def create_json(graph):
    graph_data = {}

    graph_vertices = graph.get_vertices()
    for v in graph_vertices:
        vertex = graph.get_vertex(v)
        vertex_neighbors = {}
        temp = vertex.get_neighbors()
        for neighbor in temp:
            vertex_neighbors[neighbor.get_id()] = vertex.get_weight(neighbor)

        vertex_info = [vertex.get_info(), vertex_neighbors]
        graph_data[v] = {'neighbors': vertex_info}

    with open('graph_json.json', 'w') as outfile:
        json.dump(graph_data, outfile, sort_keys=True, indent=4)


def main():
    logging.basicConfig(filename='wikipedia_scraping.log', level=logging.DEBUG)
    logging.debug('This message should go to the log file')

    movies = get_wikipedia_movies()
    graph = createGraph(movies)
    create_json(graph)



if __name__ == '__main__':
    main()  