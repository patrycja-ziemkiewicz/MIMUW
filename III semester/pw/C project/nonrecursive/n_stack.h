// stack.h
#pragma once

#include "common/sumset.h"
#include <stddef.h> // Dla size_t
#include <stdlib.h>

typedef struct {
    const Sumset* a;
    const Sumset* b;
    int id;
    bool firstTime;
} SumsetP;

typedef struct n_stack {
    SumsetP* data;    // Dynamicznie alokowana tablica par.
    size_t size;  
    size_t start;
    Sumset* sumsets;     // Aktualny rozmiar stosu (liczba elementów).
} n_stack;


static inline void nStack_init(n_stack* stack, int d);

static inline void nStack_start(n_stack* stack, const Sumset* a, const Sumset* b, int id);

static inline void nStack_push(n_stack* stack, const Sumset* a, const Sumset* b, int id);

static inline SumsetP nStack_top(n_stack* stack);

static inline void nStack_pop(n_stack* stack);

static inline void nStack_swap(n_stack* stack);

static inline void nStack_change_id(n_stack* stack, int id);

static inline int nStack_is_empty(const n_stack* stack);

static inline int nStack_size(const n_stack* stack);

static inline void nStack_destroy(n_stack* stack);

static inline void nStack_init(n_stack* stack, int d) {
    stack->data = (SumsetP*)malloc((d * d) * sizeof(SumsetP));
    stack->sumsets = (Sumset*)malloc((d * d) * sizeof(Sumset));
    if (!stack->data || !stack->sumsets) {
        exit(1);
    }
    stack->size = 0;
    stack->start = 0;
    
}

static inline void nStack_start(n_stack* stack, const Sumset* a, const Sumset* b, int id) {
    stack->data[0].a = a;
    stack->data[0].b = b;
    stack->data[0].id = id;
    stack->data[stack->size].firstTime = true;
    stack->size = 1;
    stack->start = 0;
}


static inline void nStack_push(n_stack* stack, const Sumset* a, const Sumset* b, int id) {
    sumset_add(&stack->sumsets[stack->size], a, id);
    stack->data[stack->size].id = id;
    stack->data[stack->size].b = b;
    stack->data[stack->size].firstTime = true;
    stack->data[stack->size].a = &stack->sumsets[stack->size];
    stack->size++;
    
}

static inline void nStack_swap(n_stack* stack) {
    SumsetP* top = &stack->data[stack->size - 1];
    const Sumset* tmp = top->a;
    top->a = top->b;
    top->b = tmp;
    top->id = top->a->last;
}

// Zdejmuje parę Sumsetów ze stosu.
// Zwraca 1 w przypadku sukcesu, 0 jeśli stos jest pusty.
static inline SumsetP nStack_top(n_stack* stack) {
    SumsetP result = stack->data[stack->size - 1];

    return result;
}

static inline SumsetP nStack_first(n_stack* stack) {
    SumsetP result = stack->data[stack->start];
    stack->start++;

    return result;
}

static inline void nStack_pop(n_stack* stack) {
    stack->size--;
}

static inline void nStack_change_id(n_stack* stack, int id) {
    stack->data[stack->size - 1].id = id;
    stack->data[stack->size - 1].firstTime = false;
}

// Sprawdza, czy stos jest pusty.
// Zwraca 1 jeśli pusty, 0 w przeciwnym razie.
static inline int nStack_is_empty(const n_stack* stack) {
    return stack->size - stack->start == 0;
}

static inline int nStack_size(const n_stack* stack) {
    return stack->size - stack->start;
}

// Niszczy stos i zwalnia całą przydzieloną pamięć.
static inline void nStack_destroy(n_stack* stack) {
    free(stack->data);
    free(stack->sumsets);
    stack->data = NULL;
    stack->size = 0;
    
}