import tkinter as tk
from tkinter import messagebox

def get_non_negative_integer_input(prompt):
    while True:
        try:
            value = int(prompt())
            if value < 0:
                messagebox.showerror("Error", "Please enter a non-negative integer.")
            else:
                return value
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid non-negative integer.")

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
    table = " ---------------------------------------------------------------------------------------------------------------------\n"
    table += " | Process |  Arrival Time  |  Burst Time  |  Completion Time  |  Turnaround Time  |  Waiting Time  |  Response Time |\n"
    table += " ---------------------------------------------------------------------------------------------------------------------\n"
    for process in processes:
        table += " |    {}    |     {:9}  |   {:9}  |     {:11}   |      {:10}   |     {:9}  |     {:8}   |\n".format(
            process[0], process[1], process[2], process[3],
            process[4], process[5], process[6])
    table += " ---------------------------------------------------------------------------------------------------------------------\n"
    return table

def main():
    root = tk.Tk()
    root.title("Round Robin Scheduling")

    n_entry = tk.Entry(root)
    n_entry.pack()

    quantum_entry = tk.Entry(root)
    quantum_entry.pack()

    processes = []

    def process_input():
        n = n_entry.get()
        quantum = quantum_entry.get()
        try:
            n = int(n)
            quantum = int(quantum)
            if n <= 0 or quantum <= 0:
                messagebox.showerror("Error", "Please enter positive integers for Number of processes and Time Quantum.")
            else:
                for widget in root.winfo_children():
                    widget.destroy()
                process_details(int(n), int(quantum))

        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers for Number of processes and Time Quantum.")

    def process_details(n, quantum):
        label = tk.Label(root, text="Enter process details:")
        label.pack()

        for i in range(n):
            frame = tk.Frame(root)
            frame.pack()
            tk.Label(frame, text="Process {}: ".format(i + 1)).pack(side=tk.LEFT)
            arrival_entry = tk.Entry(frame)
            arrival_entry.pack(side=tk.LEFT)
            tk.Label(frame, text=" Arrival Time ").pack(side=tk.LEFT)
            burst_entry = tk.Entry(frame)
            burst_entry.pack(side=tk.LEFT)
            tk.Label(frame, text=" Burst Time ").pack(side=tk.LEFT)
            processes.append((arrival_entry, burst_entry))

        tk.Button(root, text="Calculate", command=lambda: calculate(processes, quantum)).pack()

    def calculate(processes, quantum):
        process_list = []
        for i, process in enumerate(processes):
            arrival_time = process[0].get()
            burst_time = process[1].get()
            try:
                arrival_time = int(arrival_time)
                burst_time = int(burst_time)
                if arrival_time < 0 or burst_time < 0:
                    messagebox.showerror("Error", "Please enter non-negative integers for Arrival Time and Burst Time.")
                    return
                process_list.append([i + 1, arrival_time, burst_time, 0, 0, 0, -1])
            except ValueError:
                messagebox.showerror("Error", "Please enter valid integers for Arrival Time and Burst Time.")
                return

        calculate_time(process_list, quantum)
        calculate_turnaround_time(process_list)
        calculate_waiting_time(process_list)

        result_text = print_table(process_list)
        result_label = tk.Label(root, text=result_text)
        result_label.pack()

        avg_waiting_time = sum(process[5] for process in process_list) / len(process_list) if len(process_list) > 0 else 0
        avg_turnaround_time = sum(process[4] for process in process_list) / len(process_list) if len(process_list) > 0 else 0
        avg_response_time = sum(process[6] for process in process_list) / len(process_list) if len(process_list) > 0 else 0

        avg_label = tk.Label(root, text="Average Waiting Time: {:.2f}\nAverage Turnaround Time: {:.2f}\nAverage Response Time: {:.2f}".format(
            avg_waiting_time, avg_turnaround_time, avg_response_time))
        avg_label.pack()

    n_label = tk.Label(root, text="Enter the Number of processes:")
    n_label.pack()

    quantum_label = tk.Label(root, text="Enter the Time Quantum:")
    quantum_label.pack()

    submit_button = tk.Button(root, text="Submit", command=process_input)
    submit_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
