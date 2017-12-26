import WebScraper
import unittest

class TestStringMethods(unittest.TestCase):

    movies = WebScraper.get_wikipedia_movies()
    graph = WebScraper.createGraph(movies)

    # Find how much a movie has grossed
    # def test_get_gross_income(self):
    #     print(self.graph.get_gross_income('One Hundred and One Dalmatians'))


    # test which movies an actor has worked in
    def test_get_actors_by_movie(self):
        movie_title = "Harry Potter and the Philosopher's Stone (film)"
        actors = self.graph.get_actors_by_movie(movie_title)
        actual_actors = ['Daniel Radcliffe', 'Rupert Grint', 'Emma Watson', 'John Cleese', 'Robbie Coltrane', 'Warwick Davis', 'Richard Griffiths', 'Richard Harris', 'Ian Hart', 'John Hurt', 'Alan Rickman', 'Fiona Shaw', 'Maggie Smith', 'Julie Walters']


        self.assertEqual(sorted(actors), sorted(actual_actors))

    # test which actors worked in a movie
    def test_get_movies_by_actor(self):
        actor = "Alan Rickman"
        movies = self.graph.get_movies_by_actor(actor)
        actual_movies = ['Harry Potter and the Order of the Phoenix (film)', 'Harry Potter and the Goblet of Fire (film)', 'Harry Potter and the Deathly Hallows – Part 1', 'Harry Potter and the Chamber of Secrets (film)', "Harry Potter and the Philosopher's Stone (film)", 'Harry Potter and the Half-Blood Prince (film)', 'Harry Potter and the Deathly Hallows – Part 2']

        self.assertEqual(sorted(movies), sorted(actual_movies))


    # test which movies came out in the given year
    def test_get_movies_by_year(self):
        movies = self.graph.get_movies_by_year('2011')
        actual_movies = ['Transformers: Dark of the Moon', 'Pirates of the Caribbean: On Stranger Tides', 'Harry Potter and the Deathly Hallows – Part 2']

        self.assertEquals(sorted(movies), sorted(actual_movies))


    # test which actors acted in movies that came out in the given year
    def test_get_actors_by_year(self):
        actors = self.graph.get_actors_by_year('2011')
        actual_actors = ['Shia LaBeouf', 'Josh Duhamel', 'John Turturro', 'Tyrese Gibson', 'Rosie Huntington-Whiteley', 'Patrick Dempsey', 'Kevin Dunn', 'Julie White', 'John Malkovich', 'Frances McDormand', 'Johnny Depp', 'Penélope Cruz', 'Ian McShane', 'Kevin R. McNally', 'Geoffrey Rush', 'Daniel Radcliffe', 'Rupert Grint', 'Emma Watson', 'Helena Bonham Carter', 'Robbie Coltrane', 'Warwick Davis', 'Ralph Fiennes', 'Michael Gambon', 'John Hurt', 'Jason Isaacs', 'Gary Oldman', 'Alan Rickman', 'Maggie Smith', 'David Thewlis', 'Julie Walters']

        self.assertEquals(sorted(actors), sorted(actual_actors))

    def test_get_top_x_paid_actors(self):
        top_x = self.graph.get_top_x_paid_actors(10)
        actual_top_x = ['Arnold Schwarzenegger', 'Linda Hamilton', 'Robert Patrick', 'Daniel Radcliffe', 'Robert Downey Jr.', 'Johnny Depp', 'Emma Watson', 'Ian McKellen',  'Rupert Grint', 'Sam Worthington']


        self.assertListEqual(top_x, actual_top_x)


    # test the oldest x actors in the graph
    def test_get_oldest_x_actors(self):
        oldest = self.graph.get_oldest_x_actors(10)
        actual_oldest = [('Hugh Griffith', 105), ('Olivia de Havilland', 101), ('Angela Lansbury', 91), ('Rosemary Harris', 90), ('Robert Guillaume', 89), ('Estelle Harris', 89), ('Max von Sydow', 88), ('Cate Bauer', 88), ('Sean Connery', 87), ('Robert Wagner', 87)]

        self.assertEqual(oldest, actual_oldest)


if __name__ == '__main__':
    unittest.main()




