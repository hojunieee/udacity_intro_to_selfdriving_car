#include <iostream>
#include <vector>
using namespace std;
typedef vector < vector <float> > matrix;

vector<double> p(5,0.2);

vector<string> world(5);
world[0]='green';
world[1]='red';
world[2]='red';
world[3]='green';
world[4]='green';

vector<string> measurements(2);
measurements[0]='red';
measurements[1]='green';

vector<int> motions(2,1);

double pHit = 0.6;
double pMiss = 0.2;
double pExact = 0.8;
double pOvershoot = 0.1;
double pUndershoot = 0.1;
