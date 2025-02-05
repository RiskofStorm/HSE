#include <iostream>

using namespace std;
 

string str;
 
int main() {
	cin >> str;
	str[0] = toupper((unsigned char) str[0]);
	cout << str;
	return 0;
}