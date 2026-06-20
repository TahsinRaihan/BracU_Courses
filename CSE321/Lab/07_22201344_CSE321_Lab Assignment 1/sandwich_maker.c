#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>

#define NUM_MAKERS 3
#define BREAD 0
#define CHEESE 1
#define LETTUCE 2

const char *ingredient_names[] = {"Bread", "Cheese", "Lettuce"};
volatile int done = 0;
int table_ingredients[3] = {0, 0, 0}; 
pthread_mutex_t table_lock; 
sem_t supplier_sem;      
sem_t maker_sem[NUM_MAKERS];  

int is_on_table(int ingredient) {
    return table_ingredients[ingredient];
}

// Thred- MakEr (A, B, or C)
void *maker_func(void *arg) {
    int maker_id = *((int *)arg); 
    const char maker_name = 'A' + maker_id;
    int missing_ingredient = maker_id; 
    while (1) {
        sem_wait(&maker_sem[maker_id]);
        if (done) {
            break;
        }
        pthread_mutex_lock(&table_lock);
        int ing1 = (missing_ingredient + 1) % NUM_MAKERS;
        int ing2 = (missing_ingredient + 2) % NUM_MAKERS;
        table_ingredients[ing1] = 0;
        table_ingredients[ing2] = 0;
        
        printf("Maker %c picks up %s and %s\n", maker_name, ingredient_names[ing1], ingredient_names[ing2]);

        pthread_mutex_unlock(&table_lock); 
        printf("Maker %c is making the sandwich...\n", maker_name); 
        sleep(1); 
        printf("Maker %c finished making the sandwich and eats it\n", maker_name);
        printf("Maker %c signals Supplier\n", maker_name);
        sem_post(&supplier_sem);
    }
    return NULL;
}
// Thread:suppliier
void *supplier_func(void *arg) {
    int N = *((int *)arg); 
    srand(time(NULL));
    for (int i = 0; i < N; i++) {
        sem_wait(&supplier_sem);
        pthread_mutex_lock(&table_lock);
        int missing_ing = rand() % NUM_MAKERS; 
        int ing1 = (missing_ing + 1) % NUM_MAKERS;
        int ing2 = (missing_ing + 2) % NUM_MAKERS;
        table_ingredients[ing1] = 1;
        table_ingredients[ing2] = 1;
        printf("Supplier places: %s and %s\n", ingredient_names[ing1], ingredient_names[ing2]);
        pthread_mutex_unlock(&table_lock); 
        sem_post(&maker_sem[missing_ing]); 
    }
    sem_wait(&supplier_sem);
    done = 1;
    for (int i = 0; i < NUM_MAKERS; i++) {
        sem_post(&maker_sem[i]);
    }
    return NULL;
}
int main() {
    int N;
    printf("Enter the number of times a supplier places ingredients (N):\n"); 
    if (scanf("%d", &N) != 1 || N <= 0) {
        fprintf(stderr, "Invalid input for N.\n");
        return 1;
    }
    pthread_mutex_init(&table_lock, NULL); 
    sem_init(&supplier_sem, 0, 1); 
    sem_init(&maker_sem[BREAD], 0, 0);
    sem_init(&maker_sem[CHEESE], 0, 0);
    sem_init(&maker_sem[LETTUCE], 0, 0);

    // Creating threads
    pthread_t supplier_t;
    pthread_t maker_t[NUM_MAKERS];
    
    int maker_ids[NUM_MAKERS] = {BREAD, CHEESE, LETTUCE}; 
    // Creating maker threads
    for (int i = 0; i < NUM_MAKERS; i++) {
        pthread_create(&maker_t[i], NULL, maker_func, &maker_ids[i]); 
    }
    // Createng supplier thread
    pthread_create(&supplier_t, NULL, supplier_func, &N); 

    pthread_join(supplier_t, NULL); 

    for (int i = 0; i < NUM_MAKERS; i++) {
        pthread_join(maker_t[i], NULL);
    }
    pthread_mutex_destroy(&table_lock); 
    sem_destroy(&supplier_sem); 
    sem_destroy(&maker_sem[BREAD]);
    sem_destroy(&maker_sem[CHEESE]);
    sem_destroy(&maker_sem[LETTUCE]);
    return 0;
}
