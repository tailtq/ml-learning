import sqlite3


class DBPersistenceUtils:
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name

    def find(self):
        con = self._generate_connection()

        cur = con.cursor()
        cur.execute(f"SELECT * FROM {self.table_name}")
        # get data
        batch_values = cur.fetchall()

        # get columns name
        columns = list(map(lambda x: x[0], cur.description))

        cur.close()
        con.close()

        # combine columns and values
        result = [dict(zip(columns, values)) for values in batch_values]

        return result

    def find_one(self, row_id: int):
        """
        Find a row by its id
        :param rowid:
        :return:
        """
        con = self._generate_connection()

        cur = con.cursor()
        cur.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", [row_id])
        # get data
        values = cur.fetchone()

        # get columns name
        columns = list(map(lambda x: x[0], cur.description))

        cur.close()
        con.close()

        if not values:
            return None

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
        query = f"INSERT INTO {self.table_name}({columns}) VALUES ({question_mark})"

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

    def delete(self, row_id) -> int:
        con = self._generate_connection()

        cur = con.cursor()
        cur.execute(f"DELETE FROM {self.table_name} WHERE id = ?", [row_id])
        con.commit()

        total_rows = cur.rowcount

        cur.close()
        con.close()

        return total_rows

    def delete_by_condition(self, conditions: dict, operator: str = 'and') -> int:
        new_conditions = f" {operator} ".join([f"{column} = {value}" for column, value in conditions.items()])

        con = self._generate_connection()

        cur = con.cursor()
        cur.execute(f"DELETE FROM {self.table_name} WHERE {new_conditions}")
        con.commit()

        total_rows = cur.rowcount

        cur.close()
        con.close()

        return total_rows

    def _generate_connection(self):
        return sqlite3.connect(self.database_name)
