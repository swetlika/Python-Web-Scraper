"""
The graph is a representation of the Wikipedia scraped data
where the vertices = movies and actors. There is an edge between an actor an a movie if the actor worked in that movie, with the weight of that edge being the amount the actor made from that movie. There is also an edge from an actor to another actor if they worked on the same movie, with the edge weight being 0.
"""

import operator
from Vertex import Vertex

class Graph:
    def __init__(self):
        self.vertices_dictionary = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vertices_dictionary.values())

    '''
    adds vertex to graph
    if vertex is a movie: (movie_title, release year, True)
    if vertex is an actor: (actor name, actor age, False)
    '''
    def add_vertex(self, name, info, type_is_movie):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(name, info, type_is_movie)
        self.vertices_dictionary[name] = new_vertex
        return new_vertex

    '''
    :param name
    returns vertex from graph
    '''
    def get_vertex(self, v):
        if v in self.vertices_dictionary:
            return self.vertices_dictionary[v]
        else:
            return None

    '''
    adds an edge between two vertices in the graph
    if movie to actor edge, edge weight is the income the actor got from that movie
    if actor to actor edge, edge weight is just 0
    '''
    def add_edge(self, frm, frm_year, frm_type_is_movie, to, to_year, to_type_is_movie, weight=0):
        if frm not in self.vertices_dictionary:
            self.add_vertex(frm, frm_year, frm_type_is_movie)
        if to not in self.vertices_dictionary:
            self.add_vertex(to, to_year, to_type_is_movie)

        self.vertices_dictionary[frm].add_neighbor(self.vertices_dictionary[to], weight)
        self.vertices_dictionary[to].add_neighbor(self.vertices_dictionary[frm], weight)

    '''
    returns all vertices currently in the graph
    '''
    def get_vertices(self):
        return self.vertices_dictionary.keys()

    '''
    Find how much a movie has grossed
    :param movie: name of movie
    :return: total gross income of a movie
    '''
    def get_gross_income(self, movie):
        gross_income = 0
        v = self.get_vertex(movie)

        # add all the individual actor incomes from that movie to get total
        for w in v.get_neighbors():
            if v.get_weight(w) > 0:
                gross_income += w.get_weight(v)

        return gross_income

    '''
    List which movies an actor has worked in
    :param: name of movie
    :return: list of actors that acted in the given movie
    '''
    def get_actors_by_movie(self, movie):
        actors = []
        v = self.get_vertex(movie)
        for w in v.get_neighbors():
            actors.append(w.get_id())

        return actors

    '''
    List which actors worked in a movie
    :param: name of actor
    :return: list of all movies the actor acted in
    '''
    def get_movies_by_actor(self, actor):
        movies = []
        v = self.get_vertex(actor)
        for w in v.get_neighbors():
            if v.get_weight(w) > 0:
                movies.append(w.get_id())

        return movies


    '''
    List all the movies for a given year
    :param: string year
    :return: list of all movies released in the given year
    '''
    def get_movies_by_year(self, year):
        movies = []
        vertices = self.get_vertices()
        for vertex in vertices:
            v = self.get_vertex(vertex)
            if v.get_type() == True:
                if v.get_info() == year:
                    movies.append(vertex)

        return movies

    '''
    List all the actors for a given year
    :param: string year
    :return: list of all actors who acted in movies released in the given year
    '''
    def get_actors_by_year(self, year):
        movies = self.get_movies_by_year(year)
        actors = []
        for movie in movies:
            curr_actors = self.get_actors_by_movie(movie)
            for actor in curr_actors:
                if actor not in actors:
                    actors.append(actor)
        return actors

    '''
    List the top X actors with the most total grossing value
    :param: int x
    :return: list of highest x grossing income actors
    '''
    def get_top_x_paid_actors(self, x):
        incomes = {}
        vertices = self.get_vertices()

        # for each movie, get all actors and add their incomes to the dictionary
        for vertex in vertices:
            v = self.get_vertex(vertex)
            if v.get_type() == True:
                curr_actors = self.get_actors_by_movie(v.get_id())
                for c in curr_actors:
                    actor_vertex = self.get_vertex(c)
                    if c not in incomes:
                        incomes[c] = actor_vertex.get_weight(v)
                    else:
                        incomes[c] += actor_vertex.get_weight(v)


        # sort the dictionary in reverse to get the highest values first
        incomes = sorted(incomes.items(), key=lambda f: (f[1],f[0]), reverse=True)
        incomes = [item[0] for item in incomes]

        # return the first x values
        return incomes[:x]

    '''
    List the oldest X actors
    :param: int x
    :return: list of oldest actors
    '''
    def get_oldest_x_actors(self, x):
        ages = {}
        vertices = self.get_vertices()

        # for each movie, get all actors and add their ages to the dictionary
        for vertex in vertices:
            v = self.get_vertex(vertex)
            if v.get_type() == False:
                c = v.get_id()
                ages[c] = int(v.get_info())

        # sort the dictionary in reverse to get the highest values first
        ages = sorted(ages.items(), key=lambda f: (f[1],f[0]), reverse=True)

        # return the first x values
        return ages[:x]