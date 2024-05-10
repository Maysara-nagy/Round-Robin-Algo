#include <iostream>
#include <iomanip>
#include <cctype> // for isdigit function
using namespace std;

struct process {
    int id;
    int arrivalTime;
    int burstTime;
    int completionTime;
    int turnaroundTime;
    int waitingTime;
    int responseTime;
};

// Function to calculate completion time using Round Robin scheduling
void calculateTime(process processes[], int n, int quantum) {
    int remainingTime[n];
    for (int i = 0; i < n; i++) {
        remainingTime[i] = processes[i].burstTime;
    }
    int currentTime = 0;
    bool allDone = false;
    while (!allDone) {
        allDone = true;
        for(int i = 0; i < n; i++) {
            if (remainingTime[i] > 0) {
                allDone = false;
                if (remainingTime[i] > quantum) {
                    currentTime += quantum;
                    remainingTime[i] -= quantum;
                } else {
                    currentTime += remainingTime[i];
                    processes[i].completionTime = currentTime;
                    remainingTime[i] = 0;
                }
                if (processes[i].responseTime == -1) {
                    processes[i].responseTime = currentTime - processes[i].arrivalTime;
                }
            }
        }
    }
}

// Function to calculate turnaround time
void calculateTurnaroundTime(process processes[], int n){
    for(int i = 0; i < n; i++)
        processes[i].turnaroundTime = processes[i].completionTime - processes[i].arrivalTime;
} 

// Function to calculate waiting time
void calculateWaitingTime(process processes[], int n) {
    for(int i = 0; i < n; i++)
        processes[i].waitingTime = processes[i].turnaroundTime - processes[i].burstTime;
}

// Function to print the table
void printTable(process processes[], int n) {
    cout << " ---------------------------------------------------------------------------------------------------------------------\n";
    cout << " | Process |  Arrival Time  |  Burst Time  |  Completion Time  |  Turnaround Time  |  Waiting Time  |  Response Time |\n";                                                                                                
    cout << " ---------------------------------------------------------------------------------------------------------------------\n";
    for(int i = 0; i < n; i++){
       cout << " |    " << processes[i].id << "    |     " << setw(9) << processes[i].arrivalTime << "  |   "
             << setw(9) << processes[i].burstTime << "  |     " << setw(11) << processes[i].completionTime <<
             "   |      " << setw(10) << processes[i].turnaroundTime <<
             "   |     " << setw(9) << processes[i].waitingTime << "  |     "
             << setw(8) << processes[i].responseTime << "   |\n";
    } 
    cout << " ---------------------------------------------------------------------------------------------------------------------\n";
}

int main(){
    int n, quantum;
    cout << "Enter the Number of processes: ";
    cin >> n;
    while (cin.fail() || n <= 0) {
        cout << "Invalid input. Please enter a positive integer for the number of processes: ";
        cin.clear();
        cin.ignore(10000, '\n');
        cin >> n;
    }
    cout << "Enter the Time Quantum: ";
    cin >> quantum;
    while (cin.fail() || quantum <= 0) {
        cout << "Invalid input. Please enter a positive integer for the time quantum: ";
        cin.clear();
        cin.ignore(10000, '\n');
        cin >> quantum;
    }

    process processes[n];
    cout << "Enter process details:\n";
    for (int i = 0; i < n; i++){
        cout << "Process " << i + 1 << ":\n";
        processes[i].id = i + 1;
        cout << "  Arrival Time: ";
        cin >> processes[i].arrivalTime;
        while (cin.fail() || processes[i].arrivalTime < 0) {
            cout << "Invalid input. Please enter a non-negative integer for the arrival time: ";
            cin.clear();
            cin.ignore(10000, '\n');
            cin >> processes[i].arrivalTime;
        }
        cout << "  Burst Time: ";
        cin >> processes[i].burstTime;
        while (cin.fail() || processes[i].burstTime < 0) {
            cout << "Invalid input. Please enter a non-negative integer for the burst time: ";
            cin.clear();
            cin.ignore(10000, '\n');
            cin >> processes[i].burstTime;
        }
        processes[i].responseTime = -1; // initialize response time to -1
    }
    calculateTime(processes, n, quantum);
    calculateTurnaroundTime(processes, n);
    calculateWaitingTime(processes, n); 

    cout << "\nRound Robin Scheduling Results:\n";
    printTable(processes, n);

    // Calculate and print averages
    float avgWaitingTime = 0, avgTurnaroundTime = 0, avgResponseTime = 0;
    for (int i = 0; i < n; i++) {
        avgWaitingTime += processes[i].waitingTime;
        avgTurnaroundTime += processes[i].turnaroundTime;
        avgResponseTime += processes[i].responseTime;
    }
    avgWaitingTime /= n;
    avgTurnaroundTime /= n;
    avgResponseTime /= n;
    cout << "\nAverage Waiting Time: " << avgWaitingTime << endl;
    cout << "Average Turnaround Time: " << avgTurnaroundTime << endl;
    cout << "Average Response Time: " << avgResponseTime << endl;
    cout << "\n";

    return 0;
}
