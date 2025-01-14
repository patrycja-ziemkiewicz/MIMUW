#include <stdlib.h>
#include <string.h>

#include "common/sumset.h"
#include "nonrecursive/n_stack.h"
#include"concurrentStack.h"



void init_shared_stack(shared_stack* stack) {
    stack->size = 0;
    // Statyczne tablice są już zainicjalizowane, nie trzeba alokować pamięci.
}

int depth(const Sumset* s)
{
    int depth = 1;
    while(s->prev != NULL){
        depth++;
        s = s->prev;
    }
    return depth;
}

void push(n_stack* stack, shared_stack* s)
{
    SumsetP top_pair = nStack_first(stack);
    const Sumset* a = top_pair.a;
    const Sumset* b = top_pair.b;
    int id = top_pair.id;
    int len_a = depth(a);
    int len_b = depth(b);
    Sumset* copy_of_sumsets = malloc((len_a + len_b) * sizeof(Sumset));
    if (!copy_of_sumsets) {
        exit(1);
    }

    // Deep copie
    const Sumset* n_a = a;
    const Sumset* n_b = b;
    for (int i = 0; i < len_a; ++i) {
        copy_of_sumsets[i] = *n_a;
        n_a = n_a->prev;
    }
    for (int i = 0; i < len_b; ++i) {
        copy_of_sumsets[len_a + i] = *n_b;
        n_b = n_b->prev;
    }

    for (int i = 0; i < len_a - 1; ++i) {
        copy_of_sumsets[i].prev = &copy_of_sumsets[i + 1];
    }

    for (int i = 0; i < len_b - 1; ++i) {
        copy_of_sumsets[len_a + i].prev = &copy_of_sumsets[len_a + i + 1];
    }

    s->data[s->size].b = &copy_of_sumsets[len_a];
    s->data[s->size].id = id;
    s->data[s->size].a = &copy_of_sumsets[0];
    s->sumsets[s->size] = copy_of_sumsets;
    s->size++;

}

void pop(shared_stack* s, Sumset** tab, sumset_pair* pair) {
    *tab = s->sumsets[s->size - 1];
    *pair = s->data[s->size - 1];
    s->size--;
}

int is_empty(shared_stack* s) {
    return s->size == 0;
}

void destroy(shared_stack* s) {
    for (int i = 0; i < s->size; ++i) {
        free(s->sumsets[i]);
    }
}