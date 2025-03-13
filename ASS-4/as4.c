#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_HEAP_SIZE 100
#define MAX_LINE_LENGTH 256

typedef struct {
    char sender_category[50];
    char subject[100];
    char date[20];
    int priority;
    int arrival_order;
} Email;

typedef struct {
    Email heap[MAX_HEAP_SIZE];
    int size;
} MaxHeap;

int get_priority(const char *category) {
    if (strcmp(category, "Boss") == 0) return 5;
    if (strcmp(category, "Subordinate") == 0) return 4;
    if (strcmp(category, "Peer") == 0) return 3;
    if (strcmp(category, "ImportantPerson") == 0) return 2;
    return 1;
}

void swap(Email *a, Email *b) {
    Email temp = *a;
    *a = *b;
    *b = temp;
}

void upheap(MaxHeap *h, int index) {
    while (index > 0) {
        int parent = (index - 1) / 2;
        if (h->heap[index].priority > h->heap[parent].priority) {
            swap(&h->heap[index], &h->heap[parent]);
            index = parent;
        } else break;
    }
}

void downheap(MaxHeap *h, int index) {
    while (1) {
        int left = 2 * index + 1;
        int right = 2 * index + 2;
        int largest = index;
        
        if (left < h->size && h->heap[left].priority > h->heap[largest].priority)
            largest = left;
        if (right < h->size && h->heap[right].priority > h->heap[largest].priority)
            largest = right;
        
        if (largest == index) break;
        swap(&h->heap[index], &h->heap[largest]);
        index = largest;
    }
}

void add_email(MaxHeap *h, char *sender, char *subject, char *date, int arrival_order) {
    if (h->size >= MAX_HEAP_SIZE) return;
    Email email;
    strcpy(email.sender_category, sender);
    strcpy(email.subject, subject);
    strcpy(email.date, date);
    email.priority = get_priority(sender);
    email.arrival_order = -arrival_order;
    h->heap[h->size] = email;
    upheap(h, h->size);
    h->size++;
}

Email pop_email(MaxHeap *h) {
    if (h->size == 0) {
        Email empty = {"", "", "", 0, 0};
        return empty;
    }
    Email top = h->heap[0];
    h->size--;
    if (h->size > 0) {
        h->heap[0] = h->heap[h->size];
        downheap(h, 0);
    }
    return top;
}

Email peek_email(MaxHeap *h) {
    if (h->size == 0) {
        Email empty = {"", "", "", 0, 0};
        return empty;
    }
    return h->heap[0];
}

int email_count(MaxHeap *h) {
    return h->size;
}

void process_file(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        printf("\nFile not found.\n");
        return;
    }

    MaxHeap emailQueue = {.size = 0};
    int arrival_counter = 1;
    char line[MAX_LINE_LENGTH];

    while (fgets(line, sizeof(line), file)) {
        line[strcspn(line, "\n")] = 0;
        if (strlen(line) == 0) continue;

        char *command = strtok(line, " ");
        if (!command) continue;

        if (strcmp(command, "EMAIL") == 0) {
            char *sender = strtok(NULL, ",");
            char *subject = strtok(NULL, ",");
            char *date = strtok(NULL, ",");
            if (!sender || !subject || !date) {
                printf("\nInvalid EMAIL format\n");
                continue;
            }
            add_email(&emailQueue, sender, subject, date, arrival_counter++);
        } else if (strcmp(command, "COUNT") == 0) {
            printf("\nThere are %d emails to read.\n", email_count(&emailQueue));
        } else if (strcmp(command, "NEXT") == 0) {
            Email next_email = peek_email(&emailQueue);
            if (next_email.priority == 0) {
                printf("\nNo emails waiting.\n");
            } else {
                printf("\nNext email:\n\tSender: %s\n\tSubject: %s\n\tDate: %s\n", next_email.sender_category, next_email.subject, next_email.date);
            }
        } else if (strcmp(command, "READ") == 0) {
            Email read_email = pop_email(&emailQueue);
            if (read_email.priority == 0) {
                printf("\nNo emails to read.\n");
            }
        } else {
            printf("\nInvalid command found in file.\n");
        }
    }
    fclose(file);
}

int main() {
    char filename[MAX_LINE_LENGTH];
    printf("Enter the file name containing emails and commands: ");
    scanf("%255s", filename);
    process_file(filename);
    return 0;
}