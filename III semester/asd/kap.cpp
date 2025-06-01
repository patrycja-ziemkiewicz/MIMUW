#include <bits/stdc++.h>

using namespace std;

int dist(vector<int> x, vector<int> y) {
    return min(abs(x[0] - y[0]), abs(x[1] - y[1]));
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    // Kazdy ma swoj id, x, y
    // Sasiadow wyrazam parą id, dlugosc sciezki
    vector<vector<pair<int, int>>> neighbours(n, vector<pair<int, int>>(4));
    vector<vector<int>> sorted_x(n, vector<int>(3)), sorted_y(n, vector<int>(3));


    for (int i = 0; i < n; ++i) {
        int x, y;
        cin >> x >> y;
        sorted_x[i] = {x, y, i};
        sorted_y[i] = {y, x, i};
    }

    sort(sorted_x.begin(), sorted_x.end());
    sort(sorted_y.begin(), sorted_y.end());

    for (int i = 0; i < n; ++i) {
        int f = i + 1, l = i - 1;
        if (f == n) f = i;
        if (l == -1) l = i;
        neighbours[sorted_x[i][2]][0] = {dist(sorted_x[i], sorted_x[l]), sorted_x[l][2]};
        neighbours[sorted_x[i][2]][1] = {dist(sorted_x[i], sorted_x[f]), sorted_x[f][2]};
        neighbours[sorted_y[i][2]][2] = {dist(sorted_y[i], sorted_y[l]), sorted_y[l][2]};
        neighbours[sorted_y[i][2]][3] = {dist(sorted_y[i], sorted_y[f]), sorted_y[f][2]};
    }

    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    vector<int> paths(n, INT_MAX);
    paths[0] = 0;
    pq.emplace(0, 0);
    while(!pq.empty()) {
        pair<int, int> s = pq.top();
        pq.pop();
        if (s.first > paths[s.second]) continue;
        for (pair<int, int> edge : neighbours[s.second]) {
            if (paths[s.second] + edge.first < paths[edge.second]) {
                paths[edge.second] = paths[s.second] + edge.first;
                pq.emplace(paths[edge.second], edge.second);
            }
        }

    }

    cout << paths[n - 1];


    return 0;
}
