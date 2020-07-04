import logging
import os
import sqlite3

import

logger = logging.getLogger(__package__)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DB(metaclass=Singleton):

    conn = None

    def __init__(self):
        db_path = os.path.join(os.getenv("DATA_DIR"), "rpg.db")
        self.conn = sqlite3.connect(db_path)

        try:
            self.init()

        except Exception as e:
            logger.error('Failed to initialize database: ' + repr(e))
            raise e

    def __del__(self):
        self.conn.close()


    def init(self):
        logger.info('Initializing database...')
        c = self.conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS Games
                     (game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      chat_id INTEGER NOT NULL,
                      active BOOLEAN DEFAULT TRUE)''')

        c.execute('''CREATE INDEX idx_games_chat_id_active
                     ON Games (chat_id, active)''')

        c.execute('''CREATE TABLE IF NOT EXISTS Characters
                     (character_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      game_id INTEGER NOT NULL,
                      user_id INTEGER NOT NULL,
                      user_name TEXT,
                      role TEXT,
                      character_name TEXT,
                      active BOOLEAN DEFAULT TRUE)''')

        c.execute('''CREATE INDEX idx_characters_game_id_user_id
                     ON Characters (game_id, user_id)''')

        c.execute('''CREATE TABLE IF NOT EXISTS Contents
                     (content_id INTEGER PRIMARY_KEY AUTOINCREMENT
                      game_id INTEGER NOT NULL,
                      character_id INTEGER,
                      container TEXT,
                      key TEXT,
                      description TEXT,
                      value INTEGER)''')

        self.conn.commit()

    def do_game_start(self, chat_id, admin_id, admin_name):
        if self.is_game_running(chat_id):
            raise GameRunningError

        self.do_player_add(chat_id, admin_id, Role.MASTER, admin_name)

    def do_game_end(self, chat_id):
        c = self.conn.cursor()
        c.execute('''DELETE FROM Players
                     WHERE chat_id = ?''',
                  (chat_id,))
        c.execute('''DELETE FROM Contents
                     WHERE chat_id = ?''',
                  (chat_id,))
        self.conn.commit()

    def is_game_running(self, chat_id):
        c = self.conn.cursor()
        query = c.execute('''SELECT 1
                             FROM Players
                             WHERE chat_id = ?''',
                          (chat_id,))
        result = query.fetchone()
        return result is not None

    def get_game_players(self, chat_id):
        if not self.is_game_running(chat_id):
            raise GameNotRunningError

        c = self.conn.cursor()
        query = c.execute('''SELECT chat_id, user_id, role, user_name
                             FROM Players
                             WHERE chat_id = ?''',
                          (chat_id,))
        return [Player(*player) for player in query.fetchall()]

    def do_player_add(self, chat_id, user_id, role, user_name):
        c = self.conn.cursor()
        c.execute('''INSERT OR REPLACE INTO Players(chat_id, user_id, role, user_name)
                     VALUES (?, ?, ?, ?)''',
                  (chat_id, user_id, role, user_name,))
        self.conn.commit()

    def get_player_role(self, chat_id, user_id):
        if not self.is_game_running(chat_id):
            raise GameNotRunningError

        c = self.conn.cursor()
        query = c.execute('''SELECT role
                             FROM Players
                             WHERE chat_id = ?
                             AND user_id = ?''',
                          (chat_id, user_id,))
        result = query.fetchone()
        if result is None:
            raise PlayerNotInGameError
        return result[0]

    def get_player_name(self, chat_id, user_id):
        if not self.is_game_running(chat_id):
            raise GameNotRunningError

        c = self.conn.cursor()
        query = c.execute('''SELECT user_name
                             FROM Players
                             WHERE chat_id = ?
                             AND user_id = ?''',
                          (chat_id, user_id,))
        result = query.fetchone()
        if result is None:
            raise PlayerNotInGameError
        return result[0]

    def is_game_master(self, chat_id, user_id):
        return self.get_player_role(chat_id, user_id) == Role.MASTER.value



    def add_default_items(self, user_id, chat_id):
        self.update_item(chat_id, user_id, 'general', 'description', 'Describe your character in a few words.', False)
        self.update_item(chat_id, user_id, 'general', 'fatepoints', '3', False)
        self.update_item(chat_id, user_id, 'general', 'refresh', '3', False)
        self.update_item(chat_id, user_id, 'general', 'stress2', 'Inactive', False)
        self.update_item(chat_id, user_id, 'general', 'stress4', 'Inactive', False)
        self.update_item(chat_id, user_id, 'general', 'stress6', 'Inactive', False)
        self.update_item(chat_id, user_id, 'stunts', '1', 'Set this to your first stunt.', False)
        self.update_item(chat_id, user_id, 'aspects', 'highconcept', 'Set this to your high concept.', False)
        self.update_item(chat_id, user_id, 'aspects', 'trouble', 'Your character\'s trouble.', False)
        self.update_item(chat_id, user_id, 'aspects', '1', 'Set this to your first aspect.', False)
        self.update_item(chat_id, user_id, 'approaches', 'careful', '0', False)
        self.update_item(chat_id, user_id, 'approaches', 'clever', '0', False)
        self.update_item(chat_id, user_id, 'approaches', 'flashy', '0', False)
        self.update_item(chat_id, user_id, 'approaches', 'forceful', '0', False)
        self.update_item(chat_id, user_id, 'approaches', 'quick', '0', False)
        self.update_item(chat_id, user_id, 'approaches', 'sneaky', '0', False)


    def update_item(self, chat_id, user_id, container, key, change, replace_only):

        c = self.conn.cursor()
        query = c.execute('''SELECT value
                             FROM Contents
                             WHERE chat_id=?
                             AND user_id=?
                             AND container=?
                             AND key=?''',
                          (chat_id, user_id, container, key,))
        result = query.fetchone()
        if result is None:
            oldvalue = None
            if replace_only:
                return oldvalue, None
        else:
            oldvalue = result[0]

        if (oldvalue is None or oldvalue.isdigit()) \
                and (change.isdigit() or (change[0] in ['+', '-'] and change[1:].isdigit())):
            if oldvalue is None:
                oldvalue = 0
            else:
                oldvalue = int(oldvalue)
            if change[0] == '+':
                newvalue = oldvalue + int(change[1:])
            elif change[0] == '-':
                newvalue = oldvalue - int(change[1:])
            else:
                newvalue = int(change)
        else:
            newvalue = change

        c.execute('''INSERT OR REPLACE INTO Contents(chat_id, user_id, container, key, value)
                     VALUES (?, ?, ?, ?, ?)''',
                  (chat_id, user_id, container, key, newvalue,))
        self.conn.commit()
        return oldvalue, newvalue

    def add_to_list(self, chat_id, user_id, container, description):
        """
        description: the new item description
        """
        c = self.conn.cursor()
        query = c.execute('''SELECT MAX(key)
                             FROM Contents
                             WHERE chat_id=?
                             AND user_id=?
                             AND container=?''',
                          (chat_id, user_id, container,))
        new = query.fetchone()[0] + 1
        c.execute('''INSERT OR REPLACE INTO Contents(chat_id, user_id, container, key, value)
                     VALUES (?, ?, ?, ?, ?)''',
                  (chat_id, user_id, container, new, description,))
        self.conn.commit()

    def get_item_value(self, chat_id, user_id, container, key):
        c = self.conn.cursor()
        query = c.execute('''SELECT value
                             FROM Contents
                             WHERE chat_id=?
                             AND user_id=?
                             AND container=?
                             AND key=?''',
                          (chat_id, user_id, container, key,))
        result = query.fetchone()
        if result is None:
            return None
        return result[0]

    def delete_item(self, chat_id, user_id, container, key):
        c = self.conn.cursor()
        query = c.execute('''SELECT value
                             FROM Contents
                             WHERE chat_id=?
                             AND user_id=?
                             AND container=?
                             AND key=?''',
                          (chat_id, user_id, container, key,))
        result = query.fetchone()
        if result is None:
            return None
        oldvalue = result[0]
        c.execute('''DELETE
                     FROM Contents
                     WHERE chat_id=?
                     AND user_id=?
                     AND container=?
                     AND key=?''',
                  (chat_id, user_id, container, key,))
        self.conn.commit()
        return oldvalue

    def get_items(self, chat_id, user_id):
        c = self.conn.cursor()
        contents = {}
        query = c.execute('''SELECT container, key, value
                             FROM Contents
                             WHERE chat_id=?
                             AND user_id=?''',
                          (chat_id, user_id,))
        for row in query.fetchall():
            if row[0] not in contents:
                contents[row[0]] = {}
            contents[row[0]][row[1]] = row[2]
        return contents
