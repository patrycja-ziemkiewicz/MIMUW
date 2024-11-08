#include <bits/stdc++.h>

using namespace std;

#define M 1000000000

int find_size (int n) {
    int size = 1;
    while (size < n) {
        size <<= 1;
    }
    return size;
}

void add(vector<int> tree, int value, int id, int n) {
    id += n - 1;
    while (id != 0) {
        tree[id] += value;
        tree[id] %= M;
        id >>= 1;
    }
}


int query(int a, int b, vector<int> tree, int n) {
    if (a > b)
        return 0;
    long long sum = 0;
    a += n - 1;
    b += n - 1;
    sum += tree[a];
    if (a != b)
        sum += tree[b];
    while ((a >> 1) != (b >> 1)) {
        if (a % 2 == 0)
            sum += tree[a + 1] ;
        if (b % 2 == 1)
            sum += tree[b - 1] ;
        sum %= M;
        a >>= 1;
        b >>= 1;
    }
    return sum;
}

int main() {
    int n, k;
    cin >> n;
    cin >> k;

    int size = find_size(n);
    vector<vector<int>> trees(k, vector<int>(size));


    for (int i = 0; i < n; i++) {
        int id;
        cin >> id;
        for (int j = 0; j < k; j++) {
            int value;
            if (j == 0)
                value = 1;
            else
                value = query(id + 1, n, trees[j - 1], size);
            add(trees[j], value, id, size);
        }
    }

    cout << query(1, n, trees[k - 1], size);

    return 0;
}
