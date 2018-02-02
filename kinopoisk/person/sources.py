# -*- coding: utf-8 -*-
"""
Sources for Person
"""
from __future__ import unicode_literals

import re
from builtins import str
from lxml import html

from ..utils import KinopoiskPage, KinopoiskImagesPage, HEADERS


class PersonRoleLink(KinopoiskPage):
    """
    Parser person role info from career list
    """

    def parse(self, instance, element):
        from kinopoisk.movie import Movie
        note = element.xpath('.//span[@class="role"]/text()')[0].strip().split('...')
        role_name = None
        if len(note) > 1:
            role_name = self.prepare_str(note[1]).replace(', озвучка', '').replace('; короткометражка', '')
        movie = Movie()
        movie.parse('career_link', element)

        instance.name = role_name
        instance.movie = movie

        instance.set_source('role_link')


class PersonShortLink(KinopoiskPage):
    """
    Parser person info from short links
    """

    def parse(self, instance, content):
        link = re.compile(r'<a[^>]+href="/name/(\d+)/">(.+?)</a>').findall(content)
        if link:
            instance.id = self.prepare_int(link[0][0])
            instance.name = self.prepare_str(link[0][1])

        instance.set_source('short_link')


class PersonLink(KinopoiskPage):
    """
    Parser person info from links
    """

    def parse(self, instance, content):
        link = re.compile(r'<p class="name"><a[^>]+href="/name/(\d+)/[^"]*">(.+?)</a>').findall(content)
        if link:
            instance.id = self.prepare_int(link[0][0])
            instance.name = self.prepare_str(link[0][1])

        year = re.compile(r'<span class="year">(\d{4})</span>').findall(content)
        if year:
            instance.year_birth = self.prepare_int(year[0])

        otitle = re.compile(r'<span class="gray">(.*?)</span>').findall(content)
        if otitle:
            instance.name_en = self.prepare_str(otitle[0])

        instance.set_source('link')


class PersonMainPage(KinopoiskPage):
    """
    Parser of main person page
    """
    url = '/name/{id}/'

    def parse(self, instance, content):

        person_id = re.compile(r"<link rel=\"canonical\" href=\"https?://www.kinopoisk.ru/name/(\d+)/\" />").findall(
            content)
        if person_id:
            instance.id = self.prepare_int(person_id[0])

        name = re.compile(r'<h1 class="moviename-big" itemprop="name">(.+?)</h1>').findall(content)
        if name:
            instance.name = self.prepare_str(name[0])

        name_en = re.compile(r'<span itemprop="alternateName">([A-Z]\'?[- a-zA-Z]+)</span>').findall(content)
        if name_en:
            instance.name_en = self.prepare_str(name_en[0])

        content_info = re.compile(r'<tr\s*>\s*<td class="type">(.+?)</td>\s*<td[^>]*>(.+?)</td>\s*</tr>').findall(
            content)
        for name, value in content_info:
            if str(name) == 'дата рождения':
                year_birth = re.compile(r'<a href="/lists/m_act%5Bbirthday%5D%5Byear%5D/\d{4}/">(\d{4})</a>').findall(
                    value)
                if year_birth:
                    instance.year_birth = self.prepare_int(year_birth[0])

        # movies
        from kinopoisk.person import Role
        tree = html.fromstring(content)
        for element in tree.xpath('//div[@class="personPageItems"]/div[@class="item"]'):
            type = [t.get('data-work-type') for t in element.iterancestors()][0]
            role = Role()
            role.parse('role_link', element)

            instance.career.setdefault(type, [])
            instance.career[type].append(role)

        if instance.id:
            token = re.findall(r'xsrftoken = \'([^\']+)\'', content)
            obj_type = re.findall(r'objType: \'([^\']+)\'', content)
            if token and obj_type:
                response = self.request.get(instance.get_url('info', token=token[0], type=obj_type[0]), headers=HEADERS)
                response.connection.close()
                if response.content:
                    instance.information = response.content.decode('windows-1251', 'ignore').replace(
                        ' class="trivia"', '')

        instance.set_source('main_page')


class PersonPhotosPage(KinopoiskImagesPage):
    """
    Parser of person photos page
    """
    url = '/name/{id}/photos/'
    field_name = 'photos'
