#include "headers/normalize.h"
using namespace std;

// OPTIMIZATION: Pass variable by reference
vector< vector<float> > normalize(vector< vector <float> > &grid) {

  	// OPTIMIZATION: Avoid declaring and defining 				// intermediate variables that are not needed.
	float total = 0.0;
	int i;
	int j;
	for (i = 0; i < grid.size(); i++){
		for (j=0; j< grid[i].size(); j++){
			total += grid[i][j];
		}
	}
  
	vector<float> newRow;
	vector< vector<float> > newGrid;

	for (int y=0; y<grid.size(); y++){
    	newRow.clear();
    	for (int x=0; x<grid[0].size(); x++){
        	newRow.push_back(grid[y][x]/total);
        }
    	newGrid.push_back(newRow);
    }
      

	return newGrid;
}
