# __       __                                                __                  __    __     
#/  |  _  /  |                                              /  |                /  |  /  |    
#$$ | / \ $$ |  ______         _____  ____    ______    ____$$ |  ______        $$/  _$$ |_   
#$$ |/$  \$$ | /      \       /     \/    \  /      \  /    $$ | /      \       /  |/ $$   |  
#$$ /$$$  $$ |/$$$$$$  |      $$$$$$ $$$$  | $$$$$$  |/$$$$$$$ |/$$$$$$  |      $$ |$$$$$$/   
#$$ $$/$$ $$ |$$    $$ |      $$ | $$ | $$ | /    $$ |$$ |  $$ |$$    $$ |      $$ |  $$ | __ 
#$$$$/  $$$$ |$$$$$$$$/       $$ | $$ | $$ |/$$$$$$$ |$$ \__$$ |$$$$$$$$/       $$ |  $$ |/  |
#$$$/    $$$ |$$       |      $$ | $$ | $$ |$$    $$ |$$    $$ |$$       |      $$ |  $$  $$/ 
#$$/      $$/  $$$$$$$/       $$/  $$/  $$/  $$$$$$$/  $$$$$$$/  $$$$$$$/       $$/    $$$$/  

import tkinter as tk # python gui libraray ygma3a
from tkinter import messagebox # error box tl3 3ini 34an a search 3liha

#------------------------------------------------------------------------------------------------------------------------

def get_non_negative_integer_input(prompt):
    while True:
        try:
            value = int(prompt()) #convert the value ot int to raise the exption to value error
            if value < 0: # negative value
                messagebox.showerror("Error", "Please enter a non-negative integer.") # dh 3ady massegbox
            else:
                return value
        except ValueError: #exption value error 34an lw al value not int
            messagebox.showerror("Error", "Please enter a valid non-negative integer.")

#--------------------------------------------------------------------------------------------------------------------------

def calculate_time(processes, quantum):
    remaining_time = [process[2] for process in processes] # al 0 - 6 in the talbe
    current_time = 0
    all_done = False
    while not all_done:
        all_done = True
        for i in range(len(processes)):
            if remaining_time[i] > 0: # lsa m5lstsh fe al process
                all_done = False # lsa m5lstsh fe al process
                if remaining_time[i] > quantum: # lsa m5lstsh fe al process
                    current_time += quantum # quantum camla 
                    remaining_time[i] -= quantum #calc the remaining
                else: # al process ht5ls 2bl qunatum camla
                    current_time += remaining_time[i] # hzwd aly fadl mn al remaining msh al quntam
                    processes[i][3] = current_time # complition time
                    remaining_time[i] = 0 # 5las hreset 34an 5lst
                if processes[i][6] == -1: # response time
                    processes[i][6] = current_time - processes[i][1]

#---------------------------------------------------------------------------------------------------------------------------------

def calculate_turnaround_time(processes):
    for process in processes:
        process[4] = process[3] - process[1] #completion time - ariival time = turnaround timve

#----------------------------------------------------------------------------------------------------------------------------------

def calculate_waiting_time(processes):
    for process in processes:
        process[5] = process[4] - process[2]

#-----------------------------------------------------------------------------------------------------------------------------------

def print_table(processes):
    table = "+-----------+--------------+------------+----------------+----------------+--------------+---------------+\n"
    table += "|  Process  | Arrival Time | Burst Time | Completion Time| Turnaround Time| Waiting Time | Response Time |\n"
    table += "+-----------+--------------+------------+----------------+----------------+--------------+---------------+\n"
    for process in processes:
        table += "|{:^11}|{:^14}|{:^12}|{:^16}|{:^16}|{:^14}|{:^15}|\n".format(
            process[0], process[1], process[2], process[3], process[4], process[5], process[6])
    table += "+-----------+--------------+------------+----------------+----------------+--------------+---------------+\n"
    return table

#------------------------------------------------------------------------------------------------------------------------------------

def generate_gantt_chart(processes, quantum):
    gantt_chart = "\nGantt Chart:\n" ## bzbt al borders & initializeation
    gantt_chart += "-" * 80 + "\n"
    
    timeline = [] # start time - end time - id
    current_time = 0
    
    while any(process[2] > 0 for process in processes): # ? any burst time lw ah a5sh loop
        for process in processes:
            if process[2] > 0:
                time_slice = min(quantum, process[2])
                timeline.append((process[0], current_time, current_time + time_slice))
                current_time += time_slice
                process[2] -= time_slice

    for i, (process_id, start_time, end_time) in enumerate(timeline): # loop fe al time lines
        if i == 0 or process_id != timeline[i - 1][0]: # check if we end of the process 34an n7t | 
            gantt_chart += "|"
        gantt_chart += f" P{process_id} {start_time}-{end_time} "
    
    gantt_chart += "|\n"
    gantt_chart += "-" * 80 + "\n"
    
    return gantt_chart

#------------------------------------------------------------------------------------------------------------------------------------

def main(): # al main bta3y
    root = tk.Tk() #root window
    root.title("Round Robin Scheduling") # title
    root.geometry("1000x500")  # Set width and height for the window
    #-------------------------------------------------------------------------------------------------
    def process_input(): #Input Processing Function 
        n = n_entry.get() # number of processs
        quantum = quantum_entry.get() # time quantum
        try: # nfs al function bta3t al validation 
            n = int(n)
            quantum = int(quantum)
            if n <= 0 or quantum <= 0:
                messagebox.showerror("Error", "Please enter positive integers for Number of processes and Time Quantum.")
            else:
                for widget in root.winfo_children(): # destroy current window
                    widget.destroy()
                process_details(int(n), int(quantum))

        except ValueError: # error value like not interger values 
            messagebox.showerror("Error", "Please enter valid integers for Number of processes and Time Quantum.")

    #------------------------------------------------------------------------------------------------------

    def process_details(n, quantum): # creates entry fields for users to input details for each process.
        label = tk.Label(root, text="Enter process details:") #gui window dunamilcly
        label.pack() # al frame bta3y

        global processes
        processes = [] # el details bta3t each process

        for i in range(n): # loop 34an a create input fields ll details
            frame = tk.Frame(root)
            frame.pack()
            tk.Label(frame, text="Process {}: ".format(i + 1)).pack(side=tk.LEFT)
            arrival_entry = tk.Entry(frame)
            arrival_entry.pack(side=tk.LEFT)
            tk.Label(frame, text=" Arrival Time ").pack(side=tk.LEFT)
            burst_entry = tk.Entry(frame)
            burst_entry.pack(side=tk.LEFT)
            tk.Label(frame, text=" Burst Time ").pack(side=tk.LEFT)
            processes.append((arrival_entry, burst_entry)) # append details

        calculate_button = tk.Button(root, text="Calculate", command=lambda: calculate(processes, quantum, calculate_button)) # al button
        calculate_button.pack()

    #-----------------------------------------------------------------------------------------------------------

    def calculate(processes, quantum, calculate_button): #  calculates scheduling parameters based on the user input.
        process_list = []
        for i, process in enumerate(processes): # validation of value error and negative inputs
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
#------------------------------------------------------------------------------------------------------------
        calculate_time(process_list, quantum) # response time
        calculate_turnaround_time(process_list) # turnaround time
        calculate_waiting_time(process_list) # waiting time 

        result_text = print_table(process_list) # print talbe
        result_text_widget = tk.Text(root, width=108, height=10)
        result_text_widget.insert(tk.END, result_text)
        result_text_widget.pack()

        gantt_text = generate_gantt_chart(process_list, quantum) # print  gantt chart
        gantt_label = tk.Label(root, text=gantt_text)
        gantt_label.pack()
        
        # average fields 
        avg_waiting_time = sum(process[5] for process in process_list) / len(process_list) if len(process_list) > 0 else 0
        avg_turnaround_time = sum(process[4] for process in process_list) / len(process_list) if len(process_list) > 0 else 0
        avg_response_time = sum(process[6] for process in process_list) / len(process_list) if len(process_list) > 0 else 0

        avg_label = tk.Label(root, text="Average Waiting Time: {:.2f}\nAverage Turnaround Time: {:.2f}\nAverage Response Time: {:.2f}".format(
            avg_waiting_time, avg_turnaround_time, avg_response_time))
        avg_label.pack()

        calculate_button.destroy()  # Destroy the Calculate button after displaying the result
        
        recalculate_button = tk.Button(root, text="Recalculate", command=lambda: recalculate(root)) # recalc button
        recalculate_button.pack()

    #-------------------------------------------------------------------------------------------------------------

    def recalculate(root): #This function destroys the current root window and restarts the application by calling main() again.
        root.destroy()
        main()
    # Entry Widgets and Buttons:
    
    n_label = tk.Label(root, text="Enter the Number of processes:")
    n_label.pack()

    n_entry = tk.Entry(root)
    n_entry.pack()

    quantum_label = tk.Label(root, text="Enter the Time Quantum:")
    quantum_label.pack()

    quantum_entry = tk.Entry(root)
    quantum_entry.pack()

    submit_button = tk.Button(root, text="Submit", command=process_input)
    submit_button.pack()

    root.mainloop() # The mainloop() method keeps the GUI application running

if __name__ == "__main__": # 34an a run direct not with import 
    main()

# __          __                        _        _ _   
# \ \        / /                       | |      (_) |  
#  \ \  /\  / /__   _ __ ___   __ _  __| | ___   _| |_ 
#   \ \/  \/ / _ \ | '_ ` _ \ / _` |/ _` |/ _ \ | | __|
#    \  /\  /  __/ | | | | | | (_| | (_| |  __/ | | |_ 
#     \/  \/ \___| |_| |_| |_|\__,_|\__,_|\___| |_|\__|
