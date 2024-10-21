#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int n, m;
    cin >> n;
    cin >> m;
    vector <long long> labels(n, 0);

    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n / 2; j++) {
            int person;
            cin >> person;
            labels[--person] <<= 1;
            labels[person]++;
        }
        for (int j = 0; j < n / 2; j++) {
            int person;
            cin >> person;
            labels[--person] <<= 1;
        }
    }  
    sort(labels.begin(), labels.end());
    
    int lcs = 0;
    int curretn_lenght = 1;
    for(int i = 1; i < n; i++) {
        if (labels[i - 1] == labels[i]) 
            curretn_lenght++;
        else 
            curretn_lenght = 1;
        lcs = max(lcs, curretn_lenght);
    }
    
    cout << lcs;

    return 0;
}