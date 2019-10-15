import sqlite3

wordbook_of_conformity = { str: "text", float: "real", int: "integer"}

class DatatypeMissmatch(Exception):
    pass # можно выводить какой тип должен быть

class sqlitemodel:
    _DATABASE = "magicbase.db"    ###
    _TABLE = None   ###
    _FIELDS_MAPPING = None

    @classmethod
    def _connect(cls):
        return sqlite3.connect(cls._DATABASE)

    @classmethod
    def query(cls, query):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute(query)
        conn.commit()
        conn.close()

    @classmethod
    def _create_mapping(cls, pk):
        tables = cls.query("SELECT * FROM sqlite_master WHERE type='table'")
        table_names = [tables[1] for table in tables]
        if cls._TABLE not in table_names:
            columns_for_bd_table = ""
            for keys, val in cls._FIELDS_MAPPING.items():
                columns_for_bd_table += keys + " " + wordbook_of_conformity.get(val) + ","
            table_name = cls._TABLE
            sql_sentence = "CREATE TABLE " + table_name + " (" + columns_for_bd_table[0:-1] + ")"
            cls.query(sql_sentence)

    @classmethod
    def _update_mapping(cls, pk):
        values_from_mapping = " "
        for keys, val in cls._FIELDS_MAPPING():
            values_from_mapping += val + ","
        sql_sentence = "INSERT INTO " + cls._TABLE +  " VALUES (" + values_from_mapping[0:-1] + ")"
        cls.query(sql_sentence)

    @classmethod
    def _get_by_pk(cls, pk):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute(
            """
                SELECT * 
                FROM :table
                WHERE id = :pk
            """,
            {'table': cls._TABLE, 'pk': pk}
        )

        result = {}
        record = cur.fetchone()
        for idx, col in enumerate(cur.description):
            result[col] = record[idx]
        conn.close()
        return result

    @classmethod
    def _get_by_pk_mock(cls, *args):
        #вернуть словарь
        pass

    @classmethod
    def get_by_pk(cls, pk):
        record = cls._get_by_pk_mock(pk)
        obj = cls()
        obj.fill_data(record)   #problem here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return obj


class BasicModel(sqlitemodel):

    _DATABASE = "magicbase.db"
    _INNER_DATA ={}
    _FIELDS_MAPPING ={}  # ключ - имя поля: значение - тип данных

    def __init__(self, name = "Buba"):
        self.name = name
        """
         Basic Model existing in one exemplar?
        """
        pass

    def __getattr__(self, item):
        if item in self._FIELDS_MAPPING.keys():
            return None
        raise AttributeError      #ошибка доступа к аттрибуту объекта?

    def fill_data(self, data):
        """
        в качестве входных данных предоставляется словарь
        данные вносятся, если проходится проверка по типу
        """
        for key , val in data.items():
            if self._check_datatype_for_key(key,val):
                self.__dict__[key] = val


    def _check_datatype_for_key(self, key, val):
        key_type = self._FIELDS_MAPPING.get(key)
        if not key_type:
            return False
        if type(val) != key_type:
            raise DatatypeMissmatch("That field must have another datatyoe")
        return True

    def write_to_dict (self): #зачем повторно создавать словарь, где ключ это имя поля, а значение тип данных?
        inner_dict = {}
        for key in self._FIELDS_MAPPING:
            inner_dict[key] = getattr(self, key)
        return inner_dict

class Regular_User(BasicModel):
    _FIELDS_MAPPING = {
        "id": int,
        "email": str,
        "username": str,
        "password": str
    }
    _TABLE = "Regular_User"

#сущность которая хранит в себе пользователя и просмотренный фильм
class watched_films(BasicModel):
    _FIELDS_MAPPING = {
        "user_id": int,
        "film_id": int
    }
    _TABLE = "watched_films"

#сущность-таблица всех фильмов в бд с настроениями. Колонка настроений накопительная.
class FILMS_BLACKHOLE(BasicModel):
    _FIELDS_MAPPING = {
        "film_id": int,
        "film_name": str,
        "mood1": int,
        "mood2": int,
        "moodi": int,
    }
    _TABLE = "FILMS_BLACKHOLE"

class genre(BasicModel):
    _FIELDS_MAPPING = {
        "id": int,
        "genre_name": str
    }
    _TABLE = "genre"

#сущность которая хранит в себе фильм и его жанры
class FILMS_BLACKGOLE_with_genre(BasicModel):
    _FIELDS_MAPPING = {
        "film_id": int,
        "genre_id": int
    }
    _TABLE = "FILMS_BLACKGOLE_with_genre"

"промежуточный контейнер между пользователем и таблицей фильмов, делаем + к настроению фильма"
# class networking(BasicModel):
#     _FIELDS_MAPPING = {
#         "id": str,
#         "interests": str,
#         "mood": str
#         "chosen_films": #list_of_films_id
#     }


# class Reddit(BasicModel):
#     _FIELDS_MAPPING = {
#         "API": str,
#         "https": str,
#     }




something = Reqular_User("Baba")
something.fill_data({"id": "as5q5", "interests": "space", "mobster":"woobster"})
print(something.__dict__)