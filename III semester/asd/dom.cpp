#include <bits/stdc++.h>

using namespace std;

void create_masks(long long value, vector<long long> &next_dp, int row, int k, int mask,
                  vector<vector<int>> &tab, int col, int next_mask, int n) {
    next_dp[next_mask] = max(next_dp[next_mask], value);
    for (int r = row; r < k; ++r) {

        if ((mask & (1 << r)) == 0) {
            if (r < k - 1 && (mask & (3 << r)) == 0)  {
                int sum = tab[r][col] + tab[r + 1][col];
                if (sum > 0) {
                    create_masks(value + sum, next_dp, r + 2, k, mask, tab, col, next_mask, n);
                }
            }
            if (col < n - 1) {
                int sum = tab[r][col] + tab[r][col + 1];
                if (sum > 0) {
                    int mask2 = next_mask | (1 << r);
                    create_masks(sum + value, next_dp, r + 1, k, mask, tab, col, mask2, n);
                }
            }
        }
    }
}

int main() {
    int n, k, size;
    cin >> n >> k;
    size = 1 << k;

    vector<vector<int>> tab(k, vector<int> (n));
    vector<long long> current_dp(size, -1);
    vector<long long> next_dp(size, -1);

    for (int i = 0; i < k; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> tab[i][j];
        }
    }

    current_dp[0] = 0;

    for (int j = 0; j < n; ++j) {
        for (int i = size - 1; i >= 0; --i) {
            if (current_dp[i] >= 0) {
                create_masks(current_dp[i], next_dp, 0, k, i, tab, j, 0, n);
            }
        }
        current_dp = next_dp;
        fill(next_dp.begin(), next_dp.end(), -1);
    }

    cout << current_dp[0];

    return 0;
}

