def get_non_negative_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a non-negative integer.")
            else:
                return value
        except ValueError:
            print("Please enter a valid non-negative integer.")

def calculate_time(processes, quantum):
    remaining_time = [process[2] for process in processes]
    current_time = 0
    all_done = False
    while not all_done:
        all_done = True
        for i in range(len(processes)):
            if remaining_time[i] > 0:
                all_done = False
                if remaining_time[i] > quantum:
                    current_time += quantum
                    remaining_time[i] -= quantum
                else:
                    current_time += remaining_time[i]
                    processes[i][3] = current_time
                    remaining_time[i] = 0
                if processes[i][6] == -1:
                    processes[i][6] = current_time - processes[i][1]

def calculate_turnaround_time(processes):
    for process in processes:
        process[4] = process[3] - process[1]

def calculate_waiting_time(processes):
    for process in processes:
        process[5] = process[4] - process[2]

def print_table(processes):
    print(" ---------------------------------------------------------------------------------------------------------------------")
    print(" | Process |  Arrival Time  |  Burst Time  |  Completion Time  |  Turnaround Time  |  Waiting Time  |  Response Time |")
    print(" ---------------------------------------------------------------------------------------------------------------------")
    for process in processes:
        print(" |    {}    |     {:9}  |   {:9}  |     {:11}   |      {:10}   |     {:9}  |     {:8}   |".format(
            process[0], process[1], process[2], process[3],
            process[4], process[5], process[6]))
    print(" ---------------------------------------------------------------------------------------------------------------------")

def generate_gantt_chart(processes, quantum):
    print("\nGantt Chart:")
    print("-" * 60)
    
    timeline = []
    current_time = 0
    while any(process[2] > 0 for process in processes):
        for process in processes:
            if process[2] > 0:
                time_slice = min(quantum, process[2])
                timeline.append((process[0], current_time, current_time + time_slice))
                current_time += time_slice
                process[2] -= time_slice

    for i in range(len(timeline)):
        if i == 0 or timeline[i][0] != timeline[i - 1][0]:
            print("|", end="")
        print(" P{} {}-{} ".format(timeline[i][0], timeline[i][1], timeline[i][2]), end="")
    print("|")
    print("-" * 60)

def main():
    n = get_non_negative_integer_input("Enter the Number of processes: ")
    quantum = get_non_negative_integer_input("Enter the Time Quantum: ")

    processes = []
    print("Enter process details:")
    for i in range(n):
        print("Process {}:".format(i + 1))
        pid = i + 1
        arrival_time = get_non_negative_integer_input("  Arrival Time: ")
        burst_time = get_non_negative_integer_input("  Burst Time: ")
        processes.append([pid, arrival_time, burst_time, 0, 0, 0, -1])

    calculate_time(processes, quantum)
    calculate_turnaround_time(processes)
    calculate_waiting_time(processes)

    print("\nRound Robin Scheduling Results:")
    print_table(processes)
    generate_gantt_chart(processes, quantum)

    # Calculate and print averages
    avg_waiting_time = sum(process[5] for process in processes) / n if n > 0 else 0
    avg_turnaround_time = sum(process[4] for process in processes) / n if n > 0 else 0
    avg_response_time = sum(process[6] for process in processes) / n if n > 0 else 0
    print("\nAverage Waiting Time: {:.2f}".format(avg_waiting_time))
    print("Average Turnaround Time: {:.2f}".format(avg_turnaround_time))
    print("Average Response Time: {:.2f}".format(avg_response_time))

if __name__ == "__main__":
    main()
