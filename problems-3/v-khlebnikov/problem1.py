import unittest


class Table:
    def __init__(self, table):
        self._table = table

    def __str__(self):
        return str(self._table)

    def __eq__(self, other):
        if not isinstance(other, Table):
            return False
        return self._table == other._table

    def tail(self, n):
        if n < 0:
            raise ValueError("Argument must be positive")
        return Table(self._table[-n:])

    def head(self, n):
        if n < 0:
            raise ValueError("Argument must be positive")
        return Table(self._table[:n])

    def get_rows(self, indexes):
        return Table([self._table[i] for i in indexes])

    def __get_column(self, n):
        return [row[n] for row in self._table]

    def get_columns(self, indexes):
        return Table([self.__get_column(i) for i in indexes])

    def join_by_rows(self, other):
        if not isinstance(other, Table):
            return False
        return Table(self._table + other._table)

    def join_by_columns(self, other):
        if not isinstance(other, Table):
            return False
        new_table = Table([row + other_row for (row, other_row) in zip(self._table, other._table)])
        new_table._table += other._table[len(self._table):] if len(other._table) > len(self._table) else self._table[
                                                                                                         len(other._table):]
        return new_table


class TestTable(unittest.TestCase):
    def test_tail(self):
        self.assertEqual(Table([[4, 5, 6], [7, 8, 9]]), Table([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).tail(2))

    def test_head(self):
        self.assertEqual(Table([[1, 2, 3], [4, 5, 6]]), Table([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).head(2))

    def test_get_rows(self):
        self.assertEqual(Table([[1, 2, 3], [7, 8, 9]]), Table([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).get_rows([0, 2]))

    def test_get_columns(self):
        self.assertEqual(Table([[1, 4, 7], [3, 6, 9]]), Table([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).get_columns([0, 2]))

    def test_join_by_rows(self):
        self.assertEqual(Table([[1, 2], [3, 4], [5, 6], [7, 8]]),
                         Table([[1, 2], [3, 4]]).join_by_rows(Table([[5, 6], [7, 8]])))

    def test_join_by_columns(self):
        self.assertEqual(Table([[1, 2, 5, 6], [3, 4, 7, 8]]),
                         Table([[1, 2], [3, 4]]).join_by_columns(Table([[5, 6], [7, 8]])))

    def test_join_by_columns_with_different_dimensions(self):
        self.assertEqual(Table([[1, 2, 5, 6], [3, 4, 7, 8, 9], [1, 2, 3]]),
                         Table([[1, 2], [3, 4], [1, 2, 3]]).join_by_columns(Table([[5, 6], [7, 8, 9]])))


if __name__ == '__main__':
    unittest.main()
