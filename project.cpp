#include<iostream>
using namespace std;
struct process{
    int id;
    int arrivalTime;
    int burstTime;
    int completionTime;
    int turnaroundTime;
    int watingTime;
};

void calculateTime(process processes[],int n, int quantum) {
    int remainingTime[n];
    for (int i = 0;i < n ; i++)
    {
        remainingTime[i]=processes[i].burstTime;
    }
    int currentTime=0;
    bool allDone=false;
    while (!allDone)
    {
        allDone=true;
        for(int i =0;i<n;i++)
        {
            if(remainingTime[i]>0){
            allDone=false;
            if(remainingTime[i]>quantum){
                 currentTime = currentTime + quantum;
                 remainingTime[i] = remainingTime[i]-quantum;
            }
            else{
                currentTime = currentTime + remainingTime[i];
                processes[i].completionTime=currentTime;
                remainingTime[i]=0; 

            }
        }
        }
    }


}
void calculateTurnaroundTime(process processes[],int n){
    for(int i = 0; i < n; i++)
        processes[i].turnaroundTime = processes[i].completionTime-processes[i].arrivalTime;
} 

void calculatewaitingTime(process processes[],int n) {
    for(int i = 0; i < n; i++)
        processes[i].watingTime = processes[i].turnaroundTime-processes[i].burstTime;
}
void printTable(process processes[],int n){
    cout << " -------------------------------------------------------------------------------------------\n";
    cout << " | process | Arrival Time | Burst Time | Completion Time | TurnaroundTime | Waiting Time  | \n";                                                                                                
    cout << " -------------------------------------------------------------------------------------------\n";
    for(int i = 0; i<n;i++){
       cout << "|    " << processes[i].id << "  |    " << processes[i].arrivalTime << "    |   "
             << processes[i].burstTime << "   |     " << processes[i].completionTime <<
             "      |  "
             << processes[i].turnaroundTime << "     |      " << processes[i].watingTime << "        |\n";
    } 
    cout << "-----------------------------------------------------------------------------------------\n";
}
int main(){
    int n,quantum;
    cout<<"Entrer the Number  of process";
    cin>>n;
    cout<<"Entrer the Time Quantum";
    cin>>quantum;

    process processes[n];
    cout << "Enter process detalis:\n";
    for (int i=0; i <n; i++){
        cout << "process"<< i + 1 << ":\n";
        processes[i].id = i + 1;
        cout << "  Arrival Time: ";
        cin >> processes[i].arrivalTime;
        cout << "Burst Time:";
        cin >> processes[i].burstTime;
    }
    calculateTime(processes,n,quantum);
    calculateTurnaroundTime(processes,n);
    calculatewaitingTime(processes,n); 

    cout << "\nRound Robin Scheduling Results:\n";
    printTable(processes,n);
    return 0;
}
