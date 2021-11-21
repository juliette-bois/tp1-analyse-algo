# Code C++ traduit en Python : https://www.lama.univ-savoie.fr/pagesmembres/tavenas/Materiel_online/minCouplage.cpp

import time
import sys


class Simplex:
    def __init__(self, matrix, b, c, standard_form):
        """
        :param matrix: 2D array of float
        :type matrix:
        :param b: array of float
        :type b:
        :param c: array of float
        :type c:
        :param standard_form:
        :type standard_form: bool
        :return:
        :rtype:
        """
        self.minimum = 0
        self.isUnbounded = False
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.A = [[0.0 for col in range(self.cols)] for row in range(self.rows)]
        self.B = [0.0] * len(b)
        self.C = [0.0] * len(c)
        self.base = [0] * self.rows

        if standard_form:
            for i in range(self.rows):  # pass A[][] values to the metrix
                for j in range(self.cols):
                    self.A[i][j] = matrix[i][j]
            for i in range(self.rows):  # pass b[] values to the B vector
                self.B[i] = b[i]
                self.base[i] = i
            for i in range(self.cols):  # pass c[] values to the B vector
                self.C[i] = c[i]
            for i in range(self.rows):
                pivot = -self.C[i]
                for j in range(self.rows, self.cols):
                    self.C[j] += pivot * self.A[i][j]
                self.minimum += pivot * self.B[i]
        else:
            Astart = [[0.0 for col in range(self.cols + self.rows)] for row in range(self.rows)]  # std::vector <std::vector<float>> Astart(rows, std::vector<float>(rows+cols, 0))
            Bstart = [1.0] * self.rows  # std::vector<float> Bstart(rows,1)
            Cstart = [0.0] * (self.cols + self.rows)  # std::vector<float> Cstart(rows+cols,0)
            for i in range(self.rows):
                Astart[i][i] = 1
                for j in range(self.cols):
                    Astart[i][self.rows + j] = matrix[i][j]
                Cstart[i] = -1
            for i in range(self.rows):  # pass b[] values to the B vector
                Bstart[i] = b[i]

            simplexStart = Simplex(Astart, Bstart, Cstart, True)  # Simplex simplexStart(Astart,Bstart,Cstart,True)
            simplexStart.CalculateSimplex()
            if simplexStart.minimum > 0.1:
                print('Error : the matching is impossible. ', simplexStart.minimum)
            else:
                for i in range(self.rows):  # pass A[][] values to the metrix
                    for j in range(self.cols):
                        self.A[i][j] = simplexStart.A[i][j + self.rows]
                for i in range(self.rows):  # pass b[] values to the B vector
                    self.B[i] = simplexStart.B[i]
                    self.base[i] = simplexStart.base[i] - self.rows
                for i in range(self.cols):  # pass c[] values to the B vector
                    self.C[i] = c[i]
                for i in range(self.rows):
                    pivot = -self.C[self.base[i]]
                    for j in range(self.cols):
                        self.C[j] += pivot * self.A[i][j]
                    self.minimum += pivot * self.B[i]

    def simplexAlgorithmCalculationStep(self):
        """
        :return:
        :rtype: bool
        """
        # check whether the table is optimal,if optimal no need to process further
        if self.checkOptimality() is True:
            return True

        # find the column which has the pivot.The least coefficient of the objective function(C array).
        pivotColumn = self.findPivotColumn()  # int

        # find the row with the pivot value.The least value item's row in the B array
        pivotRow = self.findPivotRow(pivotColumn)  # int

        if self.isUnbounded is True:
            print('Error unbounded')
            return True

        # form the next table according to the pivot value
        self.doPivoting(pivotRow, pivotColumn)
        self.base[pivotRow] = pivotColumn

        return False

    def checkOptimality(self):
        """
        :return:
        :rtype: bool
        """
        # if the table has further positive constraints,then it is not optimal
        for i in range(len(self.C)):
            if self.C[i] > 0:
                return False
        return True

    def doPivoting(self, pivotRow, pivotColumn):
        """
        :param pivotRow:
        :type pivotRow: int
        :param pivotColumn:
        :type pivotColumn: int
        :return: void
        :rtype:
        """
        pivotValue = self.A[pivotRow][pivotColumn]  # float : gets the pivot value

        # set the row values that has the pivot value divided by the pivot value and put into new row
        for k in range(self.cols):
            self.A[pivotRow][k] = self.A[pivotRow][k] / pivotValue

        self.B[pivotRow] = self.B[pivotRow] / pivotValue

        # process the other coefficients in the A array by subtracting and the ones in B
        for m in range(self.rows):
            # ignore the pivot row as we already calculated that
            if m != pivotRow:
                for p in range(self.cols):
                    if p != pivotColumn:
                        self.A[m][p] = self.A[m][p] - (self.A[m][pivotColumn] * self.A[pivotRow][p])
                self.B[m] = self.B[m] - (self.A[m][pivotColumn] * self.B[pivotRow])
                self.A[m][pivotColumn] = 0

        self.minimum = self.minimum - (self.C[pivotColumn] * self.B[pivotRow])  # set the minimum step by step

        # process the C array
        for i in range(self.cols):
            if i != pivotColumn:
                self.C[i] = self.C[i] - (self.C[pivotColumn] * self.A[pivotRow][i])

        self.C[pivotColumn] = 0

    # print the current A array
    def print(self):
        """
        :return: void
        :rtype:
        """
        print('A = ')
        for i in range(self.rows):
            for j in range(self.cols):
                sys.stdout.write(str(self.A[i][j]) + ' ')
            print('')
        print('B = ')
        for i in range(self.rows):
            sys.stdout.write(str(self.B[i]) + ' ')
        print('C = ')
        for i in range(self.cols):
            sys.stdout.write(str(self.C[i]) + ' ')
        print('')
        print('minimum =', self.minimum)

    # find the least coefficients of constraints in the objective function's position
    def findPivotColumn(self):
        """
        :return:
        :rtype: int
        """
        location = 0
        maxm = self.C[0]  # float

        for i in range(1, len(self.C), 1):
            if self.C[i] > maxm:
                maxm = self.C[i]
                location = i

        return location

    # find the row with the pivot value.The least value item's row in the B array
    def findPivotRow(self, pivotColumn):
        """
        :param pivotColumn:
        :type pivotColumn: int
        :return:
        :rtype: int
        """
        nonpositiveValueCount = 0
        result = sys.float_info.max  # float
        location = 0

        for i in range(self.rows):
            if self.A[i][pivotColumn] > 0:
                if (self.B[i] / self.A[i][pivotColumn]) < result:
                    result = self.B[i] / self.A[i][pivotColumn]
                    location = i
            else:
                nonpositiveValueCount += 1
        # checking the unbound condition if all the values are negative ones
        if nonpositiveValueCount == self.rows:
            self.isUnbounded = True

        return location

    def CalculateSimplex(self):  # return void
        """
        :return: void
        :rtype:
        """
        while not self.simplexAlgorithmCalculationStep():
            time.sleep(0)

    def printSimplex(self, output_file_name):
        """
        :param output_file_name:
        :type output_file_name: str
        :return: void
        :rtype:
        """
        with open(output_file_name, 'w+', encoding='UTF-8') as file0:
            file0.write(str(int(self.minimum)) + '\n')
            acc = 0
            for i in range(self.rows):  # (int i=0; i<rows; ++i):
                for j in range(i + 1, self.rows, 1):  # (int j=i+1; j<rows; ++j):
                    for k in range(self.rows):  # (int k=0; k<rows; ++k):
                        if self.B[k] > 0.9 and self.base[k] == acc:
                            file0.write(str(i) + ' ' + str(j) + '\n')
                    acc += 1

    @staticmethod
    def computeFile(input_file_name, output_file_name):
        # input_file_name = "input_graph"
        # output_file_name = "output_matching"

        # Open the files for reading and for writing
        with open(input_file_name, 'r+', encoding='UTF-8') as fileI:
            n = int(fileI.readline().rstrip())
            rowSizeA = n

            v = int(n * (n - 1) / 2)
            colSizeA = v

            A = [[0 for col in range(colSizeA)] for row in range(rowSizeA)]  # std::vector < std::vector < float >> A(rowSizeA, std::vector < float > (colSizeA, 0))
            B = [1.0] * rowSizeA  # std::vector < float > B(rowSizeA, 1)
            C = [0.0] * colSizeA  # std::vector < float > C(colSizeA, 0)

            trash = 0.0  # float
            acc = 0  # int
            for i in range(n):  # (int i {0}; i < n; ++i):
                line = fileI.readline().rstrip().split(' ')
                for j in range(n):  # (int j {0}; j < n; j++):
                    if i >= j:
                        trash = float(line[j])
                    if i < j:
                        C[acc] = float(line[j])
                        C[acc] = -C[acc]
                        A[i][acc] = 1
                        A[j][acc] = 1
                        acc += 1
        simplex = Simplex(A, B, C, False)
        simplex.CalculateSimplex()
        simplex.printSimplex(output_file_name)
