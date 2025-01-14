#include <stddef.h>
#include <stdio.h>

#include "common/io.h"
#include "common/sumset.h"
#include "n_stack.h"
#include <stdlib.h>



static Solution best_solution;
static InputData input_data;


static void solve2(n_stack* stack) {
    while (!nStack_is_empty(stack)) {
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
                if (b->sum > best_solution.sum) {
                    solution_build(&best_solution, &input_data, a, b);
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
    
}

int main()
{
    input_data_read(&input_data);
    //printf("here");
    //input_data_init(&input_data, 8, 32, (int[]){0}, (int[]){1, 0});

    solution_init(&best_solution);
    n_stack stack;
    nStack_init(&stack, input_data.d);
    nStack_start(&stack, &input_data.a_start, &input_data.b_start, input_data.a_start.last);
    solve2(&stack);
    //printf("here234");
    // ...

    solution_print(&best_solution);

    nStack_destroy(&stack);
    return 0;
}
