//TODO: Write a function that receives two integer matrices and outputs
// the sum of the two matrices. Then in your main() function, input a few
// examples to check your solution. Output the results of your function to 
// cout. You could even write a separate function that prints an arbitrarily 
// sized matric to cout.

#include <iostream>
#include <vector>
using namespace std;
typedef vector < vector <float> > matrix;

matrix sumM(matrix M1, matrix M2);
void matrixprint(matrix inputmatrix);

int main(){
    matrix matrix1 (5, vector <float> (3, 2));
	matrix matrix2 (5, vector <float> (3, 26));
	
	matrix result = sumM(matrix1,matrix2);
	matrixprint(result);
	return 0;
}



matrix sumM(matrix M1, matrix M2){
    matrix resultM (M1.size(),M1[0]);

    for (int row=0;row<M1.size();row++){
        for (int column=0;column<M1[0].size();column++){
            resultM[row][column] = M1[row][column] + M2[row][column];
        }
    }
    
    return resultM;
}



void matrixprint(matrix inputmatrix) {
	for (int row = 0; row < inputmatrix.size(); row++) {
		for (int column = 0; column < inputmatrix[0].size(); column++) {
			cout << inputmatrix[row][column] << " ";
		}
		cout << endl;
	}
}
