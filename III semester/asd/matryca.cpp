#include <iostream>
#include <cmath>

using namespace std;

int main() {
    int min_length = 1000000, current_length = 0, n = 0;
    char last_letter, current_letter = '*';
    bool are_the_same = true;

    while (current_letter == '*') {
        cin.get(current_letter); 
        n++;
    }
    last_letter = current_letter;
    while (current_letter != EOF && current_letter != '\n') {
        if (current_letter != '*' && current_letter != last_letter) {
            min_length = min(min_length, current_length);
            last_letter = current_letter;
            current_length = 0;
            are_the_same = false;
        }
        else if (current_letter != '*'){
            current_length = 0;
        }
        else {
            current_length++;
        }
        n++;
        cin.get(current_letter);
    }
    if (n == 0)
        cout << n - 1 << endl;
    else if (are_the_same)
        cout << 1 << endl;
    else cout << n - min_length - 1 << endl;
    

    return 0;
}