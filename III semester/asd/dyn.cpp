#include <algorithm>
#include <iostream>
using namespace std;


// Template class representing a node in the AVL tree
template <typename T> class AVLNode {
public:
    T key; // The value of the node
    AVLNode* left; // Pointer to the left child
    AVLNode* right; // Pointer to the right child
    int count; // Number of left sons
    int height; // Height of the node in the tree
    int size; // Size of the node

    // Constructor to initialize a node with a given key
    AVLNode(T k, int s)
        : key(k)
        , left(nullptr)
        , right(nullptr)
        , height(1)
        , count(0)
        , size(s)
    {
    }
};

// Template class representing the AVL tree
template <typename T> class AVLTree {
private:
    // Pointer to the root of the tree
    AVLNode<T>* root;

    // function to get the height of a node
    int height(AVLNode<T>* node)
    {
        if (node == nullptr)
            return 0;
        return node->height;
    }

    // function to get the balance factor of a node
    int balanceFactor(AVLNode<T>* node)
    {
        if (node == nullptr)
            return 0;
        return height(node->left) - height(node->right);
    }

    // function to perform a right rotation on a subtree
    AVLNode<T>* rightRotate(AVLNode<T>* y)
    {
        AVLNode<T>* x = y->left;
        AVLNode<T>* T2 = x->right;

        // Perform rotation
        x->right = y;
        y->left = T2;

        y->count -= x->count + x->size;

        // Update heights
        y->height
            = max(height(y->left), height(y->right)) + 1;
        x->height
            = max(height(x->left), height(x->right)) + 1;

        // Return new root
        return x;
    }

    // function to perform a left rotation on a subtree
    AVLNode<T>* leftRotate(AVLNode<T>* x)
    {
        AVLNode<T>* y = x->right;
        AVLNode<T>* T2 = y->left;

        y->left = x;
        x->right = T2;

        y->count += x->count + x->size;
        // Update heights
        x->height
            = max(height(x->left), height(x->right)) + 1;
        y->height
            = max(height(y->left), height(y->right)) + 1;

        // Return new root
        return y;
    }

    // function to insert a new key into the subtree rooted
    // with node

    AVLNode<T>* insert(AVLNode<T>* node, T key, int index, int size)
    {
        // Perform the normal BST insertion
        if (node == nullptr)
            return new AVLNode<T>(key, size);

        int left = node->count + 1, right = node->count + node->size;
        if (index <= left) {
            node->left = insert(node->left, key, index, size);
            node->count += size; // Zwiększamy liczbę elementów w lewym poddrzewie
        } else if (index > right){
            node->right = insert(node->right, key, index - right, size);

        }
        // When we have to split vertex
        else {
            AVLNode<T>* new_node = new AVLNode<T>(key, size);

            new_node->left = insert(node->left, node->key, left, index - left);
            new_node->right = insert(node->right, node->key, 1, node->size - index + left);
            new_node->count = node->count + index - left;
            node = new_node;
        }

        // Update height of this ancestor node
        node->height = 1
                       + max(height(node->left),
                             height(node->right));

        // Get the balance factor of this ancestor node
        int balance = balanceFactor(node);

        // If this node becomes unbalanced, then there are 4
        // cases
        if (balance > 1) {
            // Left left case
            if (balanceFactor(node->left) > 0) {
                return rightRotate(node);
            }
            else {
                // Left right case
                node->left = leftRotate(node->left);
                return rightRotate(node);
            }
        }

        if (balance < -1) {
            // Right left case
            if (balanceFactor(node->right) > 0) {
                node->right = rightRotate(node->right);
                return leftRotate(node);
            }
            // Right right case
            else {
                return leftRotate(node);
            }
        }

        return node;
    }

    T get(AVLNode<T>* node, int index)
    {
        if (node == nullptr)
            return -1;
        int left = node->count + 1, right = node->count + node->size;
        if (index < left) {
            return get(node->left, index);
        }
        else if (index > right){
            return get(node->right, index - right);
        }
        else {
            return node->key;
        }

    }

public:
    // Constructor to initialize the AVL tree
    AVLTree()
        : root(nullptr)
    {
    }

    // Function to insert a key into the AVL tree
    void insert(T key, int index, int size) { root = insert(root, key, index, size); }

    // Function to search for a key in the AVL tree
    T get(int index) {return get(root, index);}

};


int main()
{
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    AVLTree<int> avl;

    int m, w = 0, n = 0;
    cin >> m;

    for(int i = 0; i < m; ++i) {
        char operation_type;
        cin >> operation_type;
        if (operation_type == 'i') {
            int j, x, k;
            cin >> j >> x >> k;

            j = (j + w) % (n + 1);
            avl.insert(x, j + 1, k);

            n += k;
        }
        else {
            int j;
            cin >> j;
            j = (j + w) % n;
            w = avl.get(j + 1);
            cout << w << endl;

        }
    }

    return 0;
}
