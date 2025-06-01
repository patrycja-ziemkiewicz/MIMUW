#include <bits/stdc++.h>

using namespace std;

struct treeV{
    int firstValue;
    int lastValue;
    int lastSub;
    int firstSub;
    int Sub;
    bool longest;


};

int p, k, val, maxSum, currentSum, currentLeft;

int find_size (int n) {
    int size = 1;
    while (size < n) {
        size <<= 1;
    }
    return size;
}

void push(int v, int l, int r, vector<treeV> &tree, vector<int> &tree2) {

    tree2[l] += tree2[v];
    tree2[r] += tree2[v];

    tree[l].lastValue += tree2[v];
    tree[r].lastValue += tree2[v];
    tree[l].firstValue += tree2[v];
    tree[r].firstValue += tree2[v];

    tree2[v] = 0;

}

void update(vector<treeV> &tree, vector<int> &tree2, int a, int b, int v) {
    if (k < a || p > b)
        return;
    else if (a >= p && k >= b) {
        tree[v].lastValue += val;
        tree[v].firstValue += val;
        tree2[v] += val;
    }
    else {
        int l = v << 1, r = (v << 1) + 1, mid = (a + b) / 2;

        push(v, l, r, tree, tree2);

        update(tree, tree2, a, mid, l);
        update(tree, tree2, mid + 1, b, r);

        tree[v].firstValue = tree[l].firstValue;
        tree[v].lastValue = tree[r].lastValue;
        tree[v].Sub = max(tree[l].Sub, tree[r].Sub);
        tree[v].firstSub = tree[l].firstSub;
        tree[v].lastSub = tree[r].lastSub;
        if (tree[l].lastValue <= tree[r].firstValue) {
            tree[v].Sub = max(tree[v].Sub, tree[l].lastSub + tree[r].firstSub);
            if (tree[l].longest)
                tree[v].firstSub += tree[r].firstSub;
            if (tree[r].longest)
                tree[v].lastSub += tree[l].lastSub;
            tree[v].longest = (tree[l].longest && tree[r].longest);
        }
        else {
            tree[v].longest = false;
        }

        tree2[v] = 0;


    }
}

void query(vector<treeV>& tree, vector<int>& tree2, int a, int b, int v) {
    if (k < a || p > b)
        return;
    else if (a >= p && k >= b) {
        maxSum = max(maxSum, tree[v].Sub);
        if (currentLeft <= tree[v].firstValue) {
            currentSum += tree[v].firstSub;
            maxSum = max(maxSum, currentSum);
            if (!tree[v].longest)
                currentSum = tree[v].lastSub;
        }
        else {
            currentSum = tree[v].lastSub;
        }
        currentLeft = tree[v].lastValue;

    }
    else {
        int l = v << 1, r = (v << 1) + 1, mid = (a + b) / 2;

        push(v, l, r, tree, tree2);

        query(tree, tree2, a, mid, l);
        query(tree, tree2, mid + 1, b, r);
    }
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    int s, m;
    cin >> s >> m;
    int size = find_size(s);

    int n = (size << 1); // rozmiar drzewa binarnego (liczba węzłów)

    vector<treeV> tree(n);
    vector<int> tree2((size << 1) - 1, 0);

    // Inicjowanie danych
    for (int i = 1; i < n; ++i) {
        int level = static_cast<int>(std::log2(i)); // Obliczanie poziomu węzła
        int subSize = size >> level; // Sub = size / (2^level)

        tree[i].firstValue = 1;
        tree[i].lastValue = 1;
        tree[i].lastSub = subSize;
        tree[i].firstSub = subSize;
        tree[i].Sub = subSize;
        tree[i].longest = true;
    }

    for (int i = 0; i < m; ++i) {
        char c;
        cin >> c >> p >> k;
        if (c == 'N') {
            cin >> val;
            update(tree, tree2, 1, size, 1);
        }
        else {
            maxSum = 0, currentSum = 0, currentLeft = 0;
            query(tree, tree2, 1, size, 1);
            cout << maxSum << endl;
        }

    }


    return 0;
}
