#include <bits/stdc++.h>

using namespace std;

int p, k, val;

int find_size (int n) {
    int size = 1;
    while (size < n) {
        size <<= 1;
    }
    return size;
}

void push(int v, int l, int r, vector<int> &tree, vector<int> &tree2, int len) {
    if (tree2[v] != -1) {
        tree2[l] = tree2[v];
        tree2[r] = tree2[v];

        tree[l] = tree2[v] * len;
        tree[r] = tree2[v] * len;
    }
    tree2[v] = -1;

}

void update(vector<int> &tree, vector<int> &tree2, int a, int b, int v) {
    if (k < a || p > b)
        return;
    else if (a >= p && k >= b) {
        tree[v] = val * (b - a + 1);
        tree2[v] = val;
    }
    else {
        int l = v << 1, r = (v << 1) + 1, mid = (a + b) / 2;

        push(v, l, r, tree, tree2, mid - a + 1);

        update(tree, tree2, a, mid, l);
        update(tree, tree2, mid + 1, b, r);

        tree[v] = tree[l] + tree[r];
        tree2[v] = -1;


    }
}

//not used function, but if useful in other types of tasks with interval tree
int query(vector<int>& tree, vector<int>& tree2, int a, int b, int v) {
    if (k < a || p > b)
        return 0;
    else if (a >= p && k >= b) {
        return tree[v];
    }
    else {
        int l = v << 1, r = (v << 1) + 1, mid = (a + b) / 2;

        push(v, l, r, tree, tree2, mid);

        return query(tree, tree2, a, mid, l) + query(tree, tree2, mid + 1, b, r);
    }
}

int main() {
    int n, m;
    cin >> n >> m;
    int size = find_size(n);

    vector<int> tree(size << 1, 0);
    vector<int> tree2(size << 1, -1);

    for (int i = 0; i < m; ++i) {
        char c;
        cin >> p >> k >> c;
        if (c == 'B')
            val = 1;
        else
            val = 0;
        update(tree, tree2, 1, size, 1);
        p = 1, k = size;
        cout << tree[1] << endl;
    }

    return 0;
}

