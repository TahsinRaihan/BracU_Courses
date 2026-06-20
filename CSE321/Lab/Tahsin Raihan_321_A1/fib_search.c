#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int *fib_sequence = NULL;
int sequence_length = 0; 
typedef struct {
    int num_searches;
    int *search_indices; 
    int *search_results; 
} search_args_t;

// Thread 1: fibonacci Sequence GeneRation
void *fibonacci_generator(void *arg) {
    int n = *((int *)arg);
    sequence_length = n;
    int *fib = (int *)malloc(sizeof(int) * (n + 1));
    if (fib == NULL) {
        perror("Failed to allocate memory for Fibonacci sequence");
        pthread_exit(NULL);
    }
    if (n >= 0) fib[0] = 0;
    if (n >= 1) fib[1] = 1;
    
    for (int i = 2; i <= n; i++) {
        fib[i] = fib[i-1] + fib[i-2];
    }
    
    fib_sequence = fib;
    pthread_exit((void *)fib);
}
// Thread 2: Fibonacci Value Search
void *fibonacci_search(void *arg) {
    search_args_t *args = (search_args_t *)arg;
    int num_searches = args->num_searches;
    int *indices = args->search_indices;
    int *results = args->search_results;

    for (int i = 0; i < num_searches; i++) {
        int index = indices[i];

        if (index >= 0 && index <= sequence_length) {
            results[i] = fib_sequence[index];
        } else {
            results[i] = -1;
        }
    }

    pthread_exit((void *)results);
}

int main() {
    int n;
    int s;
    printf("Enter the term of fibonacci sequence:\n");
    if (scanf("%d", &n) != 1 || n < 0 || n > 40) { 
        fprintf(stderr, "Invalid input for n. Must be 0 <= n <= 40.\n");
        return 1;
    }
    
    pthread_t t1;
    void *t1_ret;

    pthread_create(&t1, NULL, fibonacci_generator, (void *)&n); 
    
    pthread_join(t1, &t1_ret); 
    

    printf("How many numbers you are willing to search?:\n");
    if (scanf("%d", &s) != 1 || s <= 0) { 
        fprintf(stderr, "Invalid input for number of searches s. Must be s > 0.\n");
        free(fib_sequence);
        return 1;
    }
    
    int *search_indices = (int *)malloc(sizeof(int) * s);
    int *search_results = (int *)malloc(sizeof(int) * s);
    if (search_indices == NULL || search_results == NULL) {
        perror("Failed to allocate memory for search arrays");
        free(fib_sequence);
        free(search_indices);
        free(search_results);
        return 1;
    }
    
    for (int i = 0; i < s; i++) {
        printf("Enter search %d:\n", i + 1);
        if (scanf("%d", &search_indices[i]) != 1) { 
             fprintf(stderr, "Invalid input for search index.\n");
             free(fib_sequence);
             free(search_indices);
             free(search_results);
             return 1;
        }
    }
    
    search_args_t search_args = {
        .num_searches = s,
        .search_indices = search_indices,
        .search_results = search_results
    };
    pthread_t t2;
    void *t2_ret;
    pthread_create(&t2, NULL, fibonacci_search, (void *)&search_args); 
    pthread_join(t2, &t2_ret); 
    
    // Fibonacci sequence
    for (int i = 0; i <= n; i++) {
        printf("a[%d]=%d\n", i, fib_sequence[i]);
    }
    // Search results
    for (int i = 0; i < s; i++) {
        printf("result of search #%d=%d\n", i + 1, search_results[i]);
    }
    free(fib_sequence); 
    free(search_indices); 
    free(search_results); 
    return 0;
}
