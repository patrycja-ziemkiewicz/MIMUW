#include <iostream>
#include <cmath>

using namespace std;

int find_max_id(int* tab, int id, int parity, int n) {
    while (id != n && tab[id] % 2 != parity) 
        id++;
            
    return  id;
}

long long* create_prefix_sum(int n, int* tab) {
    long long* prefix_sum = new long long[n + 1];
    long long sum = 0;
    int max_even = find_max_id(tab, 0, 0, n), max_odd = find_max_id(tab, 0, 1, n), min_even = -1, min_odd = -1; 
    

    prefix_sum[0] = -1;
    for (int i = 0; i < n; i++) {
        sum += tab[i];
        if (tab[i] % 2 == 0) {
            min_even = i;
            max_even = find_max_id(tab, i + 1, 0, n);
        }
        else {
            min_odd = i;
            max_odd = find_max_id(tab, i + 1, 1, n);
        }
        if (sum % 2 == 0) {
            long long odd_to_even = -1, even_to_odd = -1;
            if (max_odd != n && min_even != -1) 
                even_to_odd = tab[min_even] - tab[max_odd];
            if (max_even != n && min_odd != -1) 
                odd_to_even = tab[min_odd] - tab[max_even];

            if (odd_to_even == -1 && even_to_odd == -1)
                prefix_sum[i + 1] = -1;
            else if (odd_to_even == -1 || even_to_odd == -1)
                prefix_sum[i + 1] = sum - max(odd_to_even, even_to_odd);
            else 
                prefix_sum[i + 1] = sum - min(odd_to_even, even_to_odd); 
        } 
        else {
            prefix_sum[i + 1] = sum;
        }  
        
    }

}

int main() {
    int n;
    cin >> n;
    int* tab = new int[n];
    
    for (int i = 0; i < n; i++) {
         cin >> tab[n - i - 1];
    }

    long long* suffix_sum = create_prefix_sum(n, tab);
        
    int input_size;
    cin >> input_size;
    for (int i = 0; i < input_size; i++) {
        int number_of_products;
        cin >> number_of_products;
        cout << suffix_sum[number_of_products] << endl;
    }
    
    delete[] tab;
    delete[] suffix_sum;
    
    return 0;
}
