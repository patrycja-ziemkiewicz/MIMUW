#include <iostream>
#include <cmath>

#define BILLION 1000000000;
using namespace std;

int add_end(int* configuration_count, int right, int left, int new_end, bool if_start) {
    int result = 0;
    if (left > new_end == if_start) {
        result += configuration_count[0];
        result %= BILLION;
    }
    if (right > new_end == if_start) {
        result += configuration_count[1];
        result %= BILLION;
    }
    return result;
}

int main() {
    int n; 
    cin >> n;
    if (n >= 2) {
        int *numbers = new int[n];
        for (int i = 0; i < n; i++)
            cin >> numbers[i];

        int **configuration_count = new int* [n - 1];
        for (int i = 0; i < n - 1; i++) {
            configuration_count[i] = new int[2];
        }

        // First loop for 2
        for(int i = 0; i < n - 1; i++) {
            if (numbers[i] < numbers[i + 1]) {
                configuration_count[i][0] = 1;
                configuration_count[i][1] = 1;
            }
            else {
                configuration_count[i][0] = 0;
                configuration_count[i][1] = 0;
            }  
        }

        for (int i = 2; i < n; i++) {
            for (int j = 0; j + i < n; j++) {
                configuration_count[j][1] = add_end(configuration_count[j], numbers[j], numbers[j + i - 1], numbers[j + i], false);
                configuration_count[j][0] = add_end(configuration_count[j + 1], numbers[j + 1], numbers[j + i], numbers[j], true);
            }
        }
        int result = configuration_count[0][0] + configuration_count[0][1];
        result %= BILLION;
        cout << result;

        for (int i = 0; i < n - 1; i++) 
            delete[] configuration_count[i];
        
        delete[] configuration_count;
        delete[] numbers;
    }
    else {
        cout << 1;
    }

    return 0;
}