import mysql.connector as conn
from mysql.connector import Error
from views.greske import Greske
# Connect to database


class Database:
    con = None

    def __init__(self):
        try:
            self.con = conn.connect(host='localhost', database='oprema', user='root', password='UrLe19023009')
        except Error as e:
            Greske("Greska prilikom povezivanja na bazu", e)

    def select(self, tablename, select_columns, order=None):
        if order is None:
            query_select = "SELECT {1} from {0}".format(tablename, select_columns)
        else:
            query_select = "SELECT {1} from {0} ORDER by {2}".format(tablename, select_columns, order)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_between(self, tablename, select_columns, column_name, datum_od, datum_do, order=None):
        if order is None:
            query_select = "SELECT {1} from {0} WHERE {2} BETWEEN '{3}' AND '{4}'".format(tablename, select_columns, column_name, datum_od, datum_do)
        else:
            query_select = "SELECT {1} from {0} WHERE {2} BETWEEN '{3}' AND '{4}' ORDER by {2}".format(tablename, select_columns, column_name, datum_od, datum_do, order)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_where(self, tablename, select_columns, condition, value, order=None):
        if order is None:
            query_select = "SELECT {1} from {0} WHERE {2} = '{3}'".format(tablename, select_columns, condition, value)
        else:
            query_select = "SELECT {1} from {0} WHERE {3} = '{4}' ORDER by {2}".format(tablename, select_columns, order, condition, value)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_where_two_conditions(self, tablename, select_columns, condition1, value1, condition2, value2, order=None):
        if order is None:
            query_select = "SELECT {1} from {0} WHERE {2} = '{3}' and {4} = '{5}'".format(tablename, select_columns, condition1, value1, condition2, value2)
        else:
            query_select = "SELECT {1} from {0} WHERE {3} = '{4}' and {5} = '{6}' ORDER by {2}".format(tablename, select_columns, order, condition1, value1, condition2, value2)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_condition(self, tablename, select_columns, condition, order=None):
        if order is None:
            query_select = "SELECT {1} from {0} WHERE {2}".format(tablename, select_columns, condition)
        else:
            query_select = "SELECT {1} from {0} WHERE {2} ORDER by {3}".format(tablename, select_columns, condition, order)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_count(self, tablename, where_column, value, where_column2=None, value2=None):
        if where_column2 is None:
            query_select_count = "SELECT COUNT(*) FROM {0} WHERE {1} = '{2}'".format(tablename, where_column, value)
        else:
            query_select_count = "SELECT COUNT(*) FROM {0} WHERE {1} = '{2}' and {3} = '{4}'".format(tablename, where_column, value, where_column2, value2)
        cursor = self.con.cursor()
        cursor.execute(query_select_count)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_count_numbers(self, tablename, select_column, where_column, value, where_column2=None, value2=None):
        if where_column2 is None:
            query_select_count = "SELECT COUNT({1}) FROM {0} WHERE {2} = {3}".format(tablename, select_column, where_column, value)
        else:
            query_select_count = "SELECT COUNT(*) FROM {0} WHERE {1} = {2} and {3} = '{4}'".format(tablename, where_column, value, where_column2, value2)
        cursor = self.con.cursor()
        cursor.execute(query_select_count)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_count_tree_conditions(self, tablename, where_column, value, where_column2, value2, where_column3, value3):
        query_select_count = "SELECT COUNT(*) FROM {0} WHERE {1} = '{2}' and {3} = '{4}' and {5} = '{6}'".format(tablename, where_column, value, where_column2, value2, where_column3, value3)
        cursor = self.con.cursor()
        cursor.execute(query_select_count)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_sum_group(self, tablenames, select_columns, condition, value, group, order=None):
        if order is None:
            query_select_sum = "SELECT {1} from {0} WHERE {2} = {3} group by {4}".format(tablenames, select_columns, condition, value, group)
        else:
            query_select_sum = "SELECT {1} from {0} WHERE {2} = {3} group by {4} ORDER by {5}".format(tablenames, select_columns, condition, value, group, order)
        cursor = self.con.cursor()
        cursor.execute(query_select_sum)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_sum(self, tablename, select_where, condition, value):
        query_select_sum = "SELECT {1} from {0} WHERE {2} = {3}".format(tablename, select_where, condition, value)
        cursor = self.con.cursor()
        cursor.execute(query_select_sum)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def insert(self, tablename, schema, value):
        # ako vrednost value ima samo jednu kolonu, onda mora da se ukloni zarez na kraju tupla (npr. tabela nalozi)
        if len(value) == 1:
            values = str(value)[:-2] + str(value)[-1]
        else:
            values = value
        query_insert = "INSERT INTO {0} ({1}) VALUES {2}".format(tablename, schema, values)
        cursor = self.con.cursor()
        cursor.execute(query_insert)
        self.con.commit()
        cursor.close()
        self.con.close()

    def update(self, tablename, set_condition, filter_condition):
        query_update = "UPDATE {0} SET {1} WHERE {2}".format(tablename, set_condition, filter_condition)
        cursor = self.con.cursor()
        cursor.execute(query_update)
        self.con.commit()
        cursor.close()
        self.con.close()

    def delete(self, tablename, delete_condition):
        query_delete = "DELETE FROM {0} WHERE {1}".format(tablename, delete_condition)
        cursor = self.con.cursor()
        cursor.execute(query_delete)
        self.con.commit()
        cursor.close()
        self.con.close()

    def join(self, tablenames, select_columns, condition, value, condition2, value2, order=None):
        if order is None:
            query_select = "SELECT {1} from {0} WHERE (({2}='{3}') AND ({4}={5}))".format(tablenames, select_columns, condition, value, condition2, value2)
        else:
            query_select = "SELECT {1} from {0} WHERE (({2}='{3}') AND ({4}={5})) ORDER by {6}".format(tablenames, select_columns, condition, value, condition2, value2, order)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_last(self, tablename, select_columns, condition, value):
        query_select = "SELECT {1} from {0} WHERE {2} = {3}".format(tablename, select_columns, condition, value)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_last_from_table(self, tablename, kolona):
        query_select = "SELECT MAX({1}) FROM {0}".format(tablename, kolona)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_last_record_from_table(self, tablename, id_tabele):
        query_select = "SELECT * FROM {0} ORDER BY {1} DESC LIMIT 1".format(tablename, id_tabele)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_before_last_from_table(self, tablename, kolona):
        query_select = "select datum_amortizacije from ({0}) order by {1} DESC LIMIT 1,1".format(tablename, kolona)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_exists(self, tablename, condition, value):
        query_select = "SELECT EXISTS(SELECT * FROM {0} WHERE {1} LIKE '{2}%') ".format(tablename, condition, value)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_like(self, tablename, condition, value):
        query_select = "SELECT * FROM {0} WHERE {1} LIKE '{2}%' ".format(tablename, condition, value)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_in(self, tablename, condition, value):
        if type(value) == tuple:
            query_select = "SELECT * FROM {0} WHERE {1} in {2}".format(tablename, condition, value)  # ako je niz vrednosti ne idu zagrade posto niz vec ima zagrade
        else:
            query_select = "SELECT * FROM {0} WHERE {1} in ({2})".format(tablename, condition, value)  # ako je samo jedna vrednost konta onda idu zagrade
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_distinct(self, select_columns, iz_tabele,  join1, join2, where_condition, order_by, nivo=None):
        if nivo is None:
            query_select = "SELECT DISTINCT konto.oznaka, {0} FROM {1} join {2} join {3} WHERE {4} GROUP BY konto.oznaka ORDER BY {5}".format(select_columns, iz_tabele, join1, join2, where_condition, order_by)
        else:
            query_select = "SELECT DISTINCT LEFT(konto.oznaka, {5}), {0} FROM {1} join {2} join {3} WHERE {4} GROUP BY LEFT(konto.oznaka, {5}) ORDER BY {6}".format(select_columns, iz_tabele,  join1, join2, where_condition, nivo, order_by)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_distinct_two_left_join(self, select_columns, iz_tabele,  join1, join2, where_condition, group_by, order_by):
        query_select = "SELECT {0} FROM {1} left join {2} left join {3} WHERE {4} GROUP BY {5} ORDER BY {6}".format(select_columns, iz_tabele, join1, join2, where_condition, group_by, order_by)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_where_join(self, select_columns, iz_tabele,  join1, where_condition, order_by, join2=None):
        if join2 is None:
            query_select = "SELECT {0} FROM {1} join {2} WHERE {3} ORDER BY {4}".format(select_columns, iz_tabele, join1, where_condition, order_by)
        else:
            query_select = "SELECT {0} FROM {1} join {2} join {3} WHERE {4} ORDER BY {5}".format(select_columns, iz_tabele, join1, join2, where_condition, order_by)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_where_tree_join(self, select_columns, iz_tabele,  join1, where_condition, order_by, join2, join3):
        query_select = "SELECT {0} FROM {1} join {2} join {3} join {4} WHERE {5} ORDER BY {6}".format(select_columns, iz_tabele, join1, join2, join3, where_condition, order_by)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_where_four_join(self, select_columns, iz_tabele,  join1, where_condition, order_by, join2, join3, join4):
        query_select = "SELECT {0} FROM {1} join {2} join {3} join {4} join {5} WHERE {6} ORDER BY {7}".format(select_columns, iz_tabele, join1, join2, join3, join4, where_condition, order_by)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_where_five_join(self, iz_tabele, select_columns, join1, join2, join3, join4, join5, condition):
        query_select = "SELECT {0} FROM {1} join {2} join {3} join {4} join {5} join {6} WHERE {7}".format(select_columns, iz_tabele, join1, join2, join3, join4, join5, condition)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_where_six_join(self, iz_tabele, select_columns, join1, join2, join3, join4, join5, join6, condition):
        query_select = "SELECT {0} FROM {1} join {2} join {3} join {4} join {5} join {6} join {7} WHERE {8}".format(select_columns, iz_tabele, join1, join2, join3, join4, join5, join6, condition)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_distinct_pojavljivanje(self, select_columns, iz_tabele):
        query_select = "SELECT DISTINCT {0} FROM {1}".format(select_columns, iz_tabele)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_distinct_izvrsenje(self, select_columns, iz_tabele,  join1, join2, where_condition, order_by, nivo):
        query_select = "SELECT DISTINCT LEFT(konto.oznaka, {5}) as oznaka, {0} FROM {1} join {2} join {3} WHERE {4} GROUP BY LEFT(konto.oznaka, {5}) ORDER BY {6}".format(select_columns, iz_tabele,  join1, join2, where_condition, nivo, order_by)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_sum_group_join(self, tablenames, select_columns, condition, join, group, order=None):
        if order is None:
            query_select_group_join = "SELECT {1} from {0} join {3} WHERE {2} group by {4}".format(tablenames, select_columns, condition, join, group)
        else:
            query_select_group_join = "SELECT {1} from {0} join {3} WHERE {2} group by {4} ORDER by {5}".format(tablenames, select_columns, condition, join, group, order)
        cursor = self.con.cursor()
        cursor.execute(query_select_group_join)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_where_join_group(self, select_columns, iz_tabele,  join1, where_condition, order_by, group, join2=None):
        if join2 is None:
            query_select = "SELECT {0} FROM {1} join {2} WHERE {3} GROUP BY {5} ORDER BY {4}".format(select_columns, iz_tabele, join1, where_condition, order_by, group)
        else:
            query_select = "SELECT {0} FROM {1} join {2} join {3} WHERE {4} GROUP BY {6} ORDER BY {5}".format(select_columns, iz_tabele, join1, join2, where_condition, order_by, group)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_join(self, iz_tabele, select_columns, join, order_by):
        query_select = "SELECT {1} FROM {0} join {2} ORDER BY {3}".format(iz_tabele, select_columns, join, order_by)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat

    def select_two_join(self, iz_tabele, select_columns, join1, join2, order_by):
        query_select = "SELECT {1} FROM {0} join {2} join {3} ORDER BY {4}".format(iz_tabele, select_columns, join1, join2, order_by)
        cursor = self.con.cursor()
        cursor.execute(query_select)
        rezultat = cursor.fetchall()
        cursor.close()
        self.con.close()
        return rezultat
