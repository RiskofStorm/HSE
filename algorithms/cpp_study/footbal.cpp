#include <iostream>
#include <string>
#include <set>
#include <algorithm>

using namespace std;

string gamers;
int zeroes;
int ones;
string ret_val = "NO";

int main(){
   cin >> gamers;

   for (char c: gamers){
        if (string{c} == "0"){
            zeroes ++;
            if(zeroes == 7){cout << "YES"; return 0;}
            
        } else {zeroes=0;}
        
        if (string{c} == "1"){
            ones ++;
            if(ones == 7){cout << "YES"; return 0;}
        }else {ones=0;}
    }
    cout << "NO"; return 0;
}