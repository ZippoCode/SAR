import sys


class Sudoku:

    def __init__(self):
        self._grid = [[0 for x in range(9)] for y in range(9)]
        self._dim = 9

    def read_board(self):
        lines = open('board.txt', 'r').readlines()
        for i, line in enumerate(lines):
            line = line.strip().replace(",", "")
            for j, value in enumerate(line):
                self._grid[i][j] = int(value)

    def print_board(self):
        matrix_print = ""
        for i in range(9):
            for j in range(9):
                if j == 0:
                    matrix_print += "|"
                if j % 3 == 2:
                    matrix_print += str(self._grid[i][j]) + "|"
                else:
                    matrix_print += str(self._grid[i][j]) + " "
            if (i % 3 == 2):
                matrix_print += '\n' + "-" * 19 + '\n'
            else:
                matrix_print += '\n'
        print(matrix_print)

    def check_all(self):
        """
        Verifica che tutti i numeri in un determinato istante siano corretti.
        In particolare effettua una verifica prima sulla riga e sulla colonna
        e poi nella sottomatrice 3x3

        :return:
        """
        for row in range(9):
            for column in range(9):
                if self._grid[row][column] != 0:
                    okrc = self.check_value_row_column(row, column, self._grid[row][column])
                    oksub = self.check_submatrix(row, column, self._grid[row][column])
                    if not okrc or not oksub:
                        return False
        return True

    def check_value_row_column(self, r, c, v):
        """
        Restituisce False se il valore passato come input e' presente
        sulla stessa riga o sulla stessa colonna. Altrimenti restiuisce True

        :param r: int
        :param c: int
        :param v: int
        :return: bool
        """
        check_row = all([v != self._grid[r][i] or c == i for i in range(self._dim)])
        check_column = all([v != self._grid[i][c] or r == i for i in range(self._dim)])
        return check_row and check_column

    def check_submatrix(self, r, c, v):
        """
        Restituisce True se la sottomatrice 3x3 non contiene
        il valore passato in input. Altrimenti ritorna False

        :param r: int
        :param c: int
        :param v: int
        :return: bool
        """
        topr = 3 * int(r / 3)
        topc = 3 * int(c / 3)
        for i in range(topr, topr + 3):
            for j in range(topc, topc + 3):
                if self._grid[i][j] == v and r != i and c != j:
                    return False
        return True

    def find_void_cell(self):
        """
        Restituisce la tupla (riga, colonna) che corrisponde alla prima
        posizione disponibile per inserire un valore. Altrimenti
        viene restituito (-1,-1)

        :return:
        """
        for i in range(self._dim):
            for j in range(self._dim):
                if self._grid[i][j] == 0:
                    return i, j
        return -1, -1

    def solve(self, i=0, j=0):
        """
        Risolve il Sudoku

        :return:
        """
        i, j = self.find_void_cell()
        if i == -1:
            # Fine
            return True
        for value in range(1, 10):
            if self.check_value_row_column(i, j, value) and self.check_submatrix(i, j, value):
                self._grid[i][j] = value
                sudoku.print_board()
                if self.solve(i, j):
                    return True
                self._grid[i][j] = 0

    def read_input(self):
        """
        Legge un valore in input e se non e' presente un'altro numero
        lo scrive sulla matrice

        :return: void
        """
        number = int(input(">>: "))
        row = int(input("row>> "))
        column = int(input("column>> "))
        if self._grid[row][column] == 0:
            self._grid[row][column] = number


if __name__ == '__main__':
    sudoku = Sudoku()
    matrix = sudoku.read_board()
    sudoku.solve()