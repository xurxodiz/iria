import json
from enum import Enum

from modules.rpgdb import *

class SituationType(Enum):
    WHERE_NOW = 0
    WHAT_BROUGHT = 1
    HOW_WORSE = 2


def init(conn):
    c = conn.conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Facets
                 (facet_id INTEGER PRIMARY KEY,
                  expansion INTEGER,
                  code TEXT,
                  name TEXT,
                  careful INTEGER,
                  clever INTEGER,
                  flashy INTEGER,
                  forceful INTEGER,
                  quick INTEGER,
                  sneaky INTEGER,
                  stunt_name TEXT,
                  stunt_description TEXT,
                  quote TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS CharacterFacets
                 (character_id INTEGER,
                  facet_id INTEGER,
                  PRIMARY KEY (character_id, facet_id),
                  FOREIGN KEY (character_id) REFERENCES Characters(character_id),
                  FOREIGN KEY (facet_id) REFERENCES Facets(facet_id)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Situations
                 (situation_id INTEGER PRIMARY KEY,
                  expansion INTEGER,
                  type INTEGER,
                  draw INTEGER,
                  description TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS GameSituations
                 (game_id INTEGER,
                  situation_id INTEGER,
                  PRIMARY KEY (game_id, situation_id),
                  FOREIGN KEY (game_id) REFERENCES Games(game_id),
                  FOREIGN KEY (situation_id) REFERENCES Situations(situation_id)''')

    json_path = os.path.join(os.getenv("DATA_DIR"), "inmf", "facets.json")

    with open(json_path) as json_file:
        json_data = json.load(json_file)
        for facet in json_data:
            c.execute('''INSERT OR REPLACE INTO Facets(
                          expansion,
                          code,
                          name,
                          careful,
                          clever,
                          flashy,
                          forceful,
                          quick,
                          sneaky,
                          stunt_name,
                          stunt_description,
                          quote
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (
                          facet['expansion'],
                          facet['code'],
                          facet['name'],
                          facet['careful'],
                          facet['clever'],
                          facet['flashy'],
                          facet['forceful'],
                          facet['quick'],
                          facet['sneaky'],
                          facet['stunt_name'],
                          facet['stunt_description'],
                          facet['quote']
                      ))

    json_path = os.path.join(os.getenv("DATA_DIR"), "inmf", "situations.json")

    with open(json_path) as json_file:
        json_data = json.load(json_file)
        for situation in json_data:
            c.execute('''INSERT OR REPLACE INTO Situations(
                          expansion,
                          type,
                          draw,
                          description
                        ) VALUES (?, ?, ?, ?)''',
                      (
                          situation['expansion'],
                          situation['type'],
                          situation['draw'],
                          situation['description'],
                      ))
    c.commit()

def get_random_facet():
    c = Conn().conn.cursor()
    query = c.execute('''SELECT *
                         FROM Facets
                         ORDER BY RANDOM()
                         LIMIT 1''')
    return query.fetchone()

def get_random_situation(type):
    c = Conn().conn.cursor()
    query = c.execute('''SELECT *
                         FROM Situations
                         WHERE type = ?
                         ORDER BY RANDOM()
                         LIMIT 1''',
                      (type,))
    return query.fetchone()

def get_random_situation_exclude(type, ids_not):
    c = Conn().conn.cursor()
    query = c.execute('''SELECT *
                         FROM Situations
                         WHERE type = ?
                         AND situation_id IS NOT IN ?
                         ORDER BY RANDOM()
                         LIMIT 1''',
                      (type, ids_not,))
    return query.fetchone()

def do_assign_situation(game_id, situation_id):
    c = Conn().conn.cursor()
    c.execute('''INSERT OR REPLACE INTO GameSituations(
                  game_id, situation_id
                ) VALUES (?, ?)''',
              (game_id, situation_id,))
    c.commit()

def do_game_start(game_id):
    where_now = get_random_situation(SituationType.WHERE_NOW)
    do_assign_situation(game_id, where_now['situation_id'])

    what_brought = get_random_situation(SituationType.WHAT_BROUGHT)
    do_assign_situation(game_id, what_brought['situation_id'])

    how_worse = get_random_situation(SituationType.HOW_WORSE)
    if how_worse['draw'] == 1:
        how_worse2 = get_random_situation_exclude(SituationType.HOW_WORSE, [how_worse['situation_id']])
        how_worse3 = get_random_situation_exclude(SituationType.HOW_WORSE, [how_worse['situation_id'],
                                                                            how_worse2['situation_id']])
        do_assign_situation(game_id, how_worse2['situation_id'])
        do_assign_situation(game_id, how_worse3['situation_id'])
    else:
        do_assign_situation(game_id, how_worse['situation_id'])
