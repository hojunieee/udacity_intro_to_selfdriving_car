import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I
    
def dot_product(vector_one, vector_two):
        result =0
        for i in range(len(vector_one)):
            result+=vector_one[i]*vector_two[i]
        return result 

    
    
    
        
class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 

    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        else:
            return (self[0][0] * self[1][1])-(self[0][1] * self[1][0])

        
        
    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
            
        sum=0
        for i in range(len(self)):
            sum+=self[i][i]
        return sum

    
    
    def inverse(self):
        inverse = []
        
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
            
            if det(self)==0:
                raise(NotImplementedError, "This matrix does not have an inverse")
            else:
                a = self[0][0]
                b = self[0][1]
                c = self[1][0]
                d = self[1][1]
            
                factor = 1 / (a * d - b * c)
            
                inverse = [[d, -b],[-c, a]]
            
                for i in range(len(inverse)):
                    for j in range(len(inverse[0])):
                        inverse[i][j] = factor * inverse[i][j]
        return inverse


    
    def T(self):
        matrix_transpose = []
        for x in range(self.w):
            matrix_transpose_row=[]
            for y in range(self.h):
                matrix_transpose_row.append(self[y][x])
            matrix_transpose.append(matrix_transpose_row)
        return matrix_transpose

        
        
        
        
    def is_square(self):
        return self.h == self.w

    
    
    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    
    
    def __repr__(self):
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    
    
    def __add__(self,other):

        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        
        ans=[]
        for y in range(self.h):
            row=[]
            for x in range(self.w):
                row.append(self[y][x]+other[y][x])
            ans.append(row)
        return ans

    
    
    def __neg__(self):
        ans=[]
        return self.g * -1
    
    
    
    def __sub__(self, other):
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be subtracted if the dimensions are the same") 
        else:
            return __add__(self,__neg__(other)
              
    def __mul__(self, other):
        if self.w != other.h:
            raise (ValueError,"Matrices can only be multiplied if the both matrix are same height") 
                           
        product = []
        Tother=T(other)
    
        for y in range(len(self)):
            row=[]
            for x in range(len(Tother)):
                a=dot_product(self[y],Tother[x])
                row.append(a)
            product.append(row)
        return product
                           
                           
        
    def __rmul__(self, other):
        if isinstance(other, numbers.Number):
            pass
            return self.g * other
