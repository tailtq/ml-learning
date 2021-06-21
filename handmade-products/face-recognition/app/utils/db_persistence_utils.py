import sqlite3


class DBPersistenceUtils:
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name

    def find(self):
        pass

    def find_one(self, rowid: int):
        """
        Find a row by its id
        :param rowid:
        :return:
        """
        con = self._generate_connection()

        cur = con.cursor()
        cur.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", [rowid])
        # get data
        values = cur.fetchone()

        # get columns name
        columns = list(map(lambda x: x[0], cur.description))

        cur.close()
        con.close()

        # combine columns and values
        result = dict(zip(columns, values))

        return result

    def create(self, values: dict):
        """
        Insert value to table
        :param values: All of the data that the row has
        :return: (int) the id of the created row
        """
        con = self._generate_connection()

        # generate query string
        columns = list(values.keys())
        question_mark = ["?"] * len(columns)

        columns = ", ".join(columns)
        question_mark = ", ".join(question_mark)
        query = f"insert into {self.table_name}({columns}) values ({question_mark})"

        # execute query and get newest id
        cur = con.cursor()
        cur.execute(query, tuple(values.values()))
        con.commit()

        row_id = cur.lastrowid

        cur.close()
        con.close()

        return row_id

    def update(self):
        pass

    def delete(self):
        pass

    def _generate_connection(self):
        return sqlite3.connect(self.database_name)
