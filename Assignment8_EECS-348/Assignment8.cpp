#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <iomanip>
#include <map>
#include <ctime>
#include <fstream> //A added to allow file reading

using namespace std;

int arrivalCounter = 0;

// Convert MM-DD-YYYY to time_t for easy comparison
time_t parseDate(const string& dateStr) {
    struct tm tm{};
    sscanf(dateStr.c_str(), "%d-%d-%d", &tm.tm_mon, &tm.tm_mday, &tm.tm_year);
    tm.tm_mon -= 1;           // struct tm months start from 0
    tm.tm_year -= 1900;       // struct tm years are since 1900
    return mktime(&tm);
}

// Map sender category to priority
map<string, int> senderPriority = {
    {"Boss", 5},
    {"Subordinate", 4},
    {"Peer", 3},
    {"ImportantPerson", 2},
    {"OtherPerson", 1}
};

class Email {
public:
    string senderCategory;
    string subject;
    string dateStr;
    time_t date;
    int arrivalOrder;

    Email(string sender, string subj, string date_string) {
        senderCategory = sender;
        subject = subj;
        dateStr = date_string;
        date = parseDate(date_string);
        arrivalOrder = arrivalCounter++;
    }

    // Compare by priority
    bool operator>(const Email& other) const {
        if (senderPriority[senderCategory] != senderPriority[other.senderCategory])
            return senderPriority[senderCategory] > senderPriority[other.senderCategory];
        if (date != other.date)
            return date > other.date;
        return arrivalOrder < other.arrivalOrder; // newer (lower arrivalOrder) is higher priority
    }

    void display() const {
        cout << "Sender: " << senderCategory << endl;
        cout << "Subject: " << subject << endl;
        cout << "Date: " << dateStr << endl;
    }
};

class MaxHeap {
private:
    vector<Email> heap;

    void heapifyUp(int idx) {
        while (idx > 0 && heap[idx] > heap[(idx - 1) / 2]) {
            swap(heap[idx], heap[(idx - 1) / 2]);
            idx = (idx - 1) / 2;
        }
    }

    void heapifyDown(int idx) {
        int size = heap.size();
        while (true) {
            int largest = idx;
            int left = 2 * idx + 1;
            int right = 2 * idx + 2;

            if (left < size && heap[left] > heap[largest]) largest = left;
            if (right < size && heap[right] > heap[largest]) largest = right;

            if (largest != idx) {
                swap(heap[idx], heap[largest]);
                idx = largest;
            } else {
                break;
            }
        }
    }

public:
    void push(const Email& email) {
        heap.push_back(email);
        heapifyUp(heap.size() - 1);
    }

    Email peek() {
        if (!heap.empty()) return heap[0];
        throw runtime_error("No emails to read.");
    }

    void pop() {
        if (heap.empty()) return;
        heap[0] = heap.back();
        heap.pop_back();
        if (!heap.empty()) heapifyDown(0);
    }

    int size() const {
        return heap.size();
    }

    bool empty() const {
        return heap.empty();
    }
};

class EmailManager {
private:
    MaxHeap heap;
    bool hasCurrent = false;
//D Email currentEmail = Email("", "", "01-01-2000"); 
    Email currentEmail = Email("OtherPerson", "default", "01-01-2000"); //A safer init w/o affecting priority

public:
    void processLine(const string& line) {
        if (line.rfind("EMAIL ", 0) == 0) {
            string rest = line.substr(6);
            stringstream ss(rest);
            string sender, subject, date;

            getline(ss, sender, ',');
            getline(ss, subject, ',');
            getline(ss, date, ',');

            Email email(sender, subject, date);
            heap.push(email);
        } else if (line == "COUNT") {
            cout << "There are " << heap.size() << " emails to read.\n" << endl;
        } else if (line == "NEXT") {
            if (!hasCurrent) {
                if (!heap.empty()) {
                    currentEmail = heap.peek();
                    hasCurrent = true;
                }
            }
            if (hasCurrent) {
                cout << "Next email:" << endl;
                currentEmail.display();
                cout << endl;
            } else {
                cout << "No emails to read.\n" << endl;
            }
        } else if (line == "READ") {
            if (hasCurrent) {
                heap.pop();
                hasCurrent = false;
            } else if (!heap.empty()) {
                heap.pop();
            }
        }
    }
};

// Read from a file
void runFromFile(const string& filename) {
    ifstream infile(filename);
    string line;
    EmailManager manager;

    while (getline(infile, line)) {
        if (!line.empty()) {
            manager.processLine(line);
        }
    }
}

int main() {
    // Test using provided test file
    runFromFile("Assignment8_Test_File.txt"); //A updated filename to match instructions 
    return 0;
}
