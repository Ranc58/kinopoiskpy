# -*- coding: utf-8 -*-
# flake8: noqa: E501
from __future__ import unicode_literals

from kinopoisk.person import Person
from .base import BaseTest


class PersonTest(BaseTest):
    def test_person_manager_with_one_result(self):
        persons = Person.objects.search('Гуальтиеро Якопетти')
        self.assertEqual(len(persons), 1)

        p = persons[0]
        self.assertEqual(p.id, 351549)
        self.assertEqual(p.name, 'Гуалтьеро Якопетти')
        self.assertEqual(p.year_birth, 1919)
        self.assertEqual(p.name_en, 'Gualtiero Jacopetti')

    def test_person_manager_with_many_results(self):
        persons = Person.objects.search('malkovich')
        self.assertGreater(len(persons), 1)

        p = persons[0]
        self.assertEqual(p.id, 24508)
        self.assertEqual(p.name, 'Джон Малкович')
        self.assertEqual(p.year_birth, 1953)
        self.assertEqual(p.name_en, 'John Malkovich')

    def test_person_main_page_source(self):
        p = Person(id=6245)
        p.get_content('main_page')
        self.assertEqual(p.id, 6245)
        self.assertEqual(p.name, 'Джонни Депп')
        self.assertEqual(p.year_birth, 1963)
        self.assertEqual(p.name_en, 'Johnny Depp')
        self.assertGreater(len(p.information), 50)

        # career
        self.assertGreaterEqual(len(p.career['actor']), 86)
        self.assertGreaterEqual(len(p.career['producer']), 7)
        self.assertGreaterEqual(len(p.career['director']), 3)
        self.assertGreaterEqual(len(p.career['writer']), 1)
        self.assertGreaterEqual(len(p.career['hrono_titr_male']), 12)
        self.assertGreaterEqual(len(p.career['himself']), 124)

        self.assertEqual(p.career['actor'][0].movie.title, 'Потаскун')
        self.assertEqual(p.career['actor'][0].movie.title_en, 'The Libertine')

        self.assertEqual(p.career['actor'][1].movie.title, 'Человек-невидимка')
        self.assertEqual(p.career['actor'][1].movie.title_en, 'The Invisible Man')
        self.assertEqual(p.career['actor'][1].name, 'Dr. Griffin')

        self.assertEqual(p.career['actor'][4].movie.title, 'Шерлок Гномс')
        self.assertEqual(p.career['actor'][4].movie.title_en, 'Gnomeo & Juliet: Sherlock Gnomes')
        self.assertEqual(p.career['actor'][4].movie.year, 2018)
        self.assertEqual(p.career['actor'][4].name, 'Sherlock Gnomes')  # voice

        self.assertGreaterEqual(p.career['actor'][6].movie.rating, 6.82)
        self.assertGreaterEqual(p.career['actor'][6].movie.votes, 42661)
        self.assertGreaterEqual(p.career['actor'][6].movie.imdb_rating, 6.70)
        self.assertGreaterEqual(p.career['actor'][6].movie.imdb_votes, 70581)

        self.assertEqual(p.career['actor'][7].name, 'Abel')  # short

    def test_person_photos_page_source(self):
        p = Person(id=8217)
        p.get_content('photos')
        self.assertGreaterEqual(len(p.photos), 11)

    def test_person_repr(self):
        instance = Person(name='Чарльз Чаплин', name_en='Charles Chaplin', year_birth='1950')
        self.assertEqual(instance.__repr__(), 'Чарльз Чаплин (Charles Chaplin), 1950')
