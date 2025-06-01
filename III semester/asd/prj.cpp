#include<bits/stdc++.h>
using namespace std;



int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int m, n, k;
    cin >> n >> m >> k;

    vector<int> number_of_edges(n, 0), values(n);
    vector<vector<int>> edges(n);

    for (int i = 0; i < n; ++i)
        cin >> values[i];

    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;
        number_of_edges[a - 1]++;
        edges[b - 1].push_back(a - 1);
    }

    auto cmp = [](pair<int, int> left, pair<int, int> right) {
        return left.first > right.first; // smaller pair.first comes first
    };
    priority_queue<pair<int, int>, vector<pair<int, int>>, decltype(cmp)> pq(cmp);

    for (int i = 0; i < n; ++i) {
        if (number_of_edges[i] == 0)
            pq.push({values[i], i});
    }

    for (int i = 0; i < k - 1; ++i) {
        pair<int, int> vertex = pq.top();
        int val = vertex.first, index = vertex.second;
        pq.pop();
        for (int id : edges[index]) {
            number_of_edges[id]--;
            values[id] = max(values[id], val);
            if (number_of_edges[id] == 0)
                pq.push({values[id], id});

        }
    }

    cout << pq.top().first;

    return 0;
}