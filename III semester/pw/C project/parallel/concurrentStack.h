// stack.h
#pragma once

#include "common/sumset.h"
#include "nonrecursive/n_stack.h"
#include <stddef.h> // Dla size_t

#define MAX_STACK_SIZE 100 // t <= 64 wiec nigdy nie przekroczymy

typedef struct {
    const Sumset* a;
    const Sumset* b;
    int id;
} sumset_pair;

typedef struct sharedStack {
    sumset_pair data[MAX_STACK_SIZE];
    size_t size;  
     
    Sumset* sumsets[MAX_STACK_SIZE];     
} shared_stack;

void init_shared_stack(shared_stack* stack);

void push(n_stack* stack, shared_stack* s);

void pop(shared_stack* s, Sumset** tab, sumset_pair* pair);

void destroy(shared_stack* s);

int is_empty(shared_stack* s);