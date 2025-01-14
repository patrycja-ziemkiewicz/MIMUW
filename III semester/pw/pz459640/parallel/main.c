#include <stddef.h>
#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <string.h>

#include "common/io.h"
#include "common/sumset.h"
#include "common/err.h"
#include "nonrecursive/n_stack.h"
#include "concurrentStack.h"



InputData input_data;
Solution best_solution;

typedef struct global_stack {
    shared_stack stack;
    int n_waiting;
    bool finished;
    int n_threads;
    Solution best_solution;
    pthread_mutex_t mutex;
    pthread_cond_t waiting;
} global_stack;

void g_stack_init(global_stack* s)
{
    ASSERT_ZERO(pthread_mutex_init(&s->mutex, NULL));
    ASSERT_ZERO(pthread_cond_init(&s->waiting, NULL));
    s->n_waiting = 0;
    s->finished = false;
    s->n_threads = input_data.t;
    solution_init(&s->best_solution);
    init_shared_stack(&s->stack);
}

void g_stack_destroy(global_stack* s)
{
    ASSERT_ZERO(pthread_cond_destroy(&s->waiting));
    ASSERT_ZERO(pthread_mutex_destroy(&s->mutex));
    destroy(&s->stack);
    

}

int get_work(global_stack* s, Solution solution, Sumset** tab, sumset_pair* pair) {
    ASSERT_ZERO(pthread_mutex_lock(&s->mutex));
    s->n_waiting++;
    if (s->n_waiting == s->n_threads && is_empty(&s->stack)) {
        s->finished = true;
        ASSERT_ZERO(pthread_cond_broadcast(&s->waiting));
    }

    while (is_empty(&s->stack) && !s->finished) {
        ASSERT_ZERO(pthread_cond_wait(&s->waiting, &s->mutex));
    }
    s->n_waiting--;

    if (!s->finished) {

        pop(&s->stack, tab, pair);

        ASSERT_ZERO(pthread_mutex_unlock(&s->mutex));
        return 1;
    }
    else {
        if (s->best_solution.sum < solution.sum) {
            s->best_solution = solution;
        }
        ASSERT_ZERO(pthread_mutex_unlock(&s->mutex));
        return 0;
    }
}

void put_work(n_stack* localStack, global_stack* s)
{

    if (nStack_size(localStack) < 3)
        return;

    ASSERT_ZERO(pthread_mutex_lock(&s->mutex));
    if (s->stack.size < s->n_threads) {
        push(localStack, &s->stack);
        ASSERT_ZERO(pthread_cond_signal(&s->waiting));
    }

    ASSERT_ZERO(pthread_mutex_unlock(&s->mutex));

}

static void solve(n_stack* stack, global_stack* s, Solution* solution) {
    int sum = 500000;
    int threshold = 100;
    while(!nStack_is_empty(stack)) {
        for (int j = 0; j < threshold; ++j) {

            if (!nStack_is_empty(stack)) {
                SumsetP top_pair = nStack_top(stack);
                const Sumset* a = top_pair.a;
                const Sumset* b = top_pair.b;
                int id = top_pair.id;
                bool firstTime = top_pair.firstTime;
                if (id > input_data.d) {
                    nStack_pop(stack);
                    continue;
                }

                bool interrupted = false;
                if (firstTime) {
                    if (a->sum > b->sum) {
                        nStack_swap(stack);
                        continue;
                    }
            
                    if (is_sumset_intersection_trivial(a, b)) {
                        for (size_t i = id; i <= input_data.d; ++i) {
                            if (!does_sumset_contain(b, i)) {
                                nStack_change_id(stack, i + 1);
                                nStack_push(stack, a, b, i);
                                interrupted = true;
                                break;
                                
                            }
                        }
                    
                    } else if ((a->sum == b->sum) && (get_sumset_intersection_size(a, b) == 2)) { // s(a) ∩ s(b) = {0, ∑b}.
                        if (b->sum > solution->sum) {
                            solution_build(solution, &input_data, a, b);
                        }
                    }
                }
                else {
                    for (size_t i = id; i <= input_data.d; ++i) {
                            if (!does_sumset_contain(b, i)) {
                                nStack_change_id(stack, i + 1);
                                nStack_push(stack, a, b, i);
                                interrupted = true;
                                break;
                                
                            }
                        }
                }

                if (!interrupted) {
                        nStack_pop(stack);
                }
            }
            else {
                break;
            }

            
        }
        put_work(stack, s);
        threshold += sum;
        sum = 0;
    }
    
    
}

void* threads_main(void* data) {
    n_stack local_stack;
    Sumset* tab;
    sumset_pair pair;
    Solution local_solution;
    solution_init(&local_solution);
    nStack_init(&local_stack, input_data.d);
    global_stack* s = data;

    while (get_work(s, local_solution, &tab, &pair)) {
        //printf("mam %p \n", &local_stack);
        nStack_start(&local_stack, pair.a, pair.b, pair.id);
        solve(&local_stack, s, &local_solution);
        free(tab);
    }
    nStack_destroy(&local_stack);

    return NULL;

}

int main()
{
    input_data_read(&input_data);
    //input_data_init(&input_data, 8, 10, (int[]){0}, (int[]){1, 0});


    solution_init(&best_solution);
    global_stack s;
    g_stack_init(&s);
    n_stack stack;
    nStack_init(&stack, input_data.d);
    nStack_start(&stack, &input_data.a_start, &input_data.b_start, input_data.a_start.last);
    

    push(&stack, &s.stack);
    nStack_destroy(&stack);
    pthread_t threads[input_data.t];
    for (int i = 0; i < input_data.t; i++) {
        ASSERT_ZERO(pthread_create(&threads[i], NULL, threads_main, &s));  
    }

    for (int i = 0; i < input_data.t; i++)
        ASSERT_ZERO(pthread_join(threads[i], NULL));

    best_solution = s.best_solution;
    g_stack_destroy(&s);


    solution_print(&best_solution);
    return 0;
}
