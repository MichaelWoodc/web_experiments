### Jan 22 2024
### Jan 22 2024
import tkinter as tk
from tkinter import filedialog
import os

class ExperimentConfigWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Experiment Configuration")

        # Variables to store values
        self.participant_id_var = tk.StringVar()
        self.num_phases_var = tk.IntVar()
        self.num_phases_var.set(2)  # Default value

        # Callback function for the main program
        self.callback = None  # Initialize the callback attribute

        # Create widgets
        self.create_widgets()

    def get_values(self):
        # Return all the values as a list of dictionaries, one per phase
        values_per_phase = []
        for phase_num in range(1, self.num_phases_var.get() + 1):
            phase_values = {
                "participant_id": self.participant_id_var.get(),
                "number_phases": self.num_phases_var.get(),

                # Values from entry widgets for each phase
                "duration_of_phase": self.get_entry_value_by_label(phase_num, "Duration of Phase"),
                "number_of_balls": self.get_entry_value_by_label(phase_num, "Number of Balls"),


                # Additional details for each ball
                "ball_colors": self.get_entry_value_by_label(phase_num, "Color"),
                "clicked_colors": self.get_entry_value_by_label(phase_num, "Clicked Colors"),
                "fixed_interval": self.get_entry_value_by_label(phase_num, "Reinforcement Interval"),
                "fixed_ratio": self.get_entry_value_by_label(phase_num, "Reinforcement Ratio"),
                "initial_speeds": self.get_entry_value_by_label(phase_num, "Speed"),
                "speed_limits": self.get_entry_value_by_label(phase_num, "Speed Limits"),
                # "fixed_interval": self.get_entry_value_by_label(phase_num, "Fixed Interval"),
                "radii": self.get_entry_value_by_label(phase_num, "Radii"),
            }
            values_per_phase.append(phase_values)
        print(values_per_phase)
        return values_per_phase

    def get_entry_value_by_label(self, phase_num, label_text):
        # Helper method to get the value of an entry widget based on its label and phase
        for widget in self.columns_frame.winfo_children()[phase_num - 1].grid_slaves():
            if isinstance(widget, tk.Entry):
                if widget.master.grid_slaves(row=widget.grid_info()["row"], column=0)[0].cget("text") == label_text:
                    return widget.get()
        return None

    def create_widgets(self):
        # Label and Entry for Participant ID
        label_participant_id = tk.Label(self.root, text="Participant ID")
        label_participant_id.pack(anchor="w")

        entry_participant_id = tk.Entry(self.root, textvariable=self.participant_id_var)
        entry_participant_id.pack(anchor="w")

        # Label and Spinbox for selecting the number of phases
        label_phases = tk.Label(self.root, text="Number of Phases")
        label_phases.pack(anchor="w")

        spinbox_phases = tk.Spinbox(self.root, from_=2, to=5, textvariable=self.num_phases_var, command=self.generate_columns)
        spinbox_phases.pack(anchor="w")

        # Frame to contain columns
        self.columns_frame = tk.Frame(self.root)
        self.columns_frame.pack()

        # Generate default columns
        self.generate_columns()

        # Save and Load buttons
        save_button = tk.Button(self.root, text="Save Settings", command=self.save_settings)
        save_button.pack()

        load_button = tk.Button(self.root, text="Load Settings", command=self.load_settings)
        load_button.pack()

        # Dropdown menu for saved files
        self.saved_files_var = tk.StringVar()
        saved_files = self.get_saved_files()
        if saved_files:
            self.saved_files_var.set(saved_files[0])  # Set the initial value if files exist
            self.saved_files_dropdown = tk.OptionMenu(self.root, self.saved_files_var, *saved_files)
        else:
            self.saved_files_var.set("No files available")
            self.saved_files_dropdown = tk.OptionMenu(self.root, self.saved_files_var, "No files available")
        self.saved_files_dropdown.pack()

        # Continue button to close the window
        continue_button = tk.Button(self.root, text="Continue", command=lambda: self.continue_to_experiment(self.callback))
        continue_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def continue_to_experiment(self, callback_function):
        print('Continuing to experiment')
        values = self.get_values()
        callback_function(values)
        # self.root.destroy()  # Close the window after calling the callback

    def generate_columns(self):
        num_phases = self.num_phases_var.get()

        # Destroy existing columns
        for widget in self.columns_frame.winfo_children():
            widget.destroy()

        # Create columns based on the selected number of phases
        for phase_num in range(1, num_phases + 1):
            phase_frame = tk.Frame(self.columns_frame, padx=10, pady=10, relief=tk.GROOVE, borderwidth=2)
            phase_frame.grid(row=0, column=phase_num - 1, sticky="w")  # Left-justify

            # Add labels and entry widgets for each column
            tk.Label(phase_frame, text=f"Phase {phase_num}").grid(row=0, column=0, pady=(0, 5), sticky="w")
            tk.Label(phase_frame, text="Duration of Phase").grid(row=1, column=0, pady=(0, 5), sticky="w")
            tk.Entry(phase_frame).grid(row=1, column=1, pady=(0, 5), padx=5, sticky="w")  # Duration of Phase
            
            tk.Label(phase_frame, text="Number of Balls").grid(row=2, column=0, pady=(0, 5), sticky="w")
            tk.Entry(phase_frame).grid(row=2, column=1, pady=(0, 5), padx=5, sticky="w")  # Number of Balls
            
            tk.Label(phase_frame, text="Speed").grid(row=3, column=0, pady=(0, 5), sticky="w")
            tk.Entry(phase_frame).grid(row=3, column=1, pady=(0, 5), padx=5, sticky="w")  # Initial Speed
            
            # tk.Label(phase_frame, text="Speed Limits").grid(row=4, column=0, pady=(0, 5), sticky="w")
            # tk.Entry(phase_frame).grid(row=4, column=1, pady=(0, 5), padx=5, sticky="w")  # Speed Limits
            
            # tk.Label(phase_frame, text="Interval").grid(row=5, column=0, pady=(0, 5), sticky="w")
            # tk.Entry(phase_frame).grid(row=5, column=1, pady=(0, 5), padx=5, sticky="w")  # Max Score Rate
            
            # tk.Label(phase_frame, text="Ratio").grid(row=7, column=0, pady=(0, 5), sticky="w")
            # tk.Entry(phase_frame).grid(row=7, column=1, pady=(0, 5), padx=5, sticky="w")  # Max Score Rate

            # Additional details for each ball
            tk.Label(phase_frame, text=f"Stimuli").grid(row=9, column=0, pady=(10, 5), sticky="w")

            tk.Label(phase_frame, text="Color").grid(row=10, column=0, pady=(0, 5), sticky="w")
            tk.Entry(phase_frame).grid(row=10, column=1, pady=(0, 5), padx=5, sticky="w")  # Color

            tk.Label(phase_frame, text="Clicked Color").grid(row=11, column=0, pady=(0, 5), sticky="w")
            tk.Entry(phase_frame).grid(row=11, column=1, pady=(0, 5), padx=5, sticky="w")  # Color

            tk.Label(phase_frame, text="Reinforcement Interval").grid(row=12, column=0, pady=(0, 5), sticky="w")
            tk.Entry(phase_frame).grid(row=12, column=1, pady=(0, 5), padx=5, sticky="w")  # Reinforcement Type

            tk.Label(phase_frame, text="Reinforcement Ratio").grid(row=13, column=0, pady=(0, 5), sticky="w")
            tk.Entry(phase_frame).grid(row=13, column=1, pady=(0, 5), padx=5, sticky="w")  # Reinforcement Value

            tk.Label(phase_frame, text="Radii").grid(row=14, column=0, pady=(0, 5), sticky="w")
            tk.Entry(phase_frame).grid(row=14, column=1, pady=(0, 5), padx=5, sticky="w")  # Radius

    def save_settings(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialdir="./experiment_settings")
        if file_name:
            with open(file_name, "w") as file:
                file.write(f"Participant ID: {self.participant_id_var.get()}\n")
                file.write(f"Number of Phases: {self.num_phases_var.get()}\n")

                # Save values from entry widgets
                for phase_num in range(1, self.num_phases_var.get() + 1):
                    for widget in self.columns_frame.winfo_children()[phase_num - 1].grid_slaves():
                        if isinstance(widget, tk.Entry):
                            value = widget.get()
                            label_text = widget.master.grid_slaves(row=widget.grid_info()["row"], column=0)[0].cget("text")
                            file.write(f"{label_text}: {value}\n")

            # Update the dropdown menu with the saved files
            self.update_saved_files_dropdown()

    def load_settings(self):
        selected_file = self.saved_files_var.get()
        if selected_file and selected_file != "No files available":
            file_path = os.path.join("experiment_settings", selected_file)
            with open(file_path, "r") as file:
                lines = file.readlines()

                # Extract values from the loaded file and set them to the variables
                participant_id = None
                num_phases = None
                entry_values_per_phase = {}  # Separate dictionary for each phase

                for line in lines:
                    if "Participant ID" in line:
                        participant_id = line.split(":")[1].strip()
                    elif "Number of Phases" in line:
                        num_phases = int(line.split(":")[1].strip())
                    else:
                        parts = line.split(":")
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            
                            # Handle special cases for "Color" and "Clicked Color"
                            if key == "Color" or key == "Clicked Color":
                                # Parse the list from the string and remove extra characters
                                value_list = [item.strip(" [\\]") for item in value.split(',')]
                                entry_values_per_phase.setdefault(key, []).append(value_list)
                            else:
                                # If it's not "Color" or "Clicked Color," treat it as a single string
                                entry_values_per_phase.setdefault(key, []).append(value)
                            
                            

                            # # Handle special cases for "Color" and "Clicked Color"
                            # if key == "Color" or key == "Clicked Color":
                            #     # Parse the list from the string and remove extra characters
                            #     value_list = [item.strip(" [\\]") for item in value.split(',')]
                            #     entry_values_per_phase.setdefault(key, []).append(value_list)
                            # else:
                            #     entry_values_per_phase.setdefault(key, []).append(value)



                # Set participant ID and number of phases
                self.participant_id_var.set(participant_id)
                self.num_phases_var.set(num_phases)

                # Update the GUI with the new values
                self.generate_columns()

                # Update the entry values based on the loaded file
                for phase_num in range(1, num_phases + 1):
                    for widget in self.columns_frame.winfo_children()[phase_num - 1].grid_slaves():
                        if isinstance(widget, tk.Entry):
                            label_text = widget.master.grid_slaves(row=widget.grid_info()["row"], column=0)[0].cget("text")
                            values_for_label = entry_values_per_phase.get(label_text, [])
                            if len(values_for_label) >= phase_num:
                                value = values_for_label[phase_num - 1]
                                widget.delete(0, tk.END)
                                widget.insert(0, value)

                # Additional details for each ball
                # for phase_num in range(1, num_phases + 1):
                #     self.get_and_set_additional_details(entry_values_per_phase, phase_num)


    def get_saved_files(self):
        # Get a list of saved files in the experiment_settings folder
        folder_path = "experiment_settings"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return [file for file in os.listdir(folder_path) if file.endswith(".txt")]

    def update_saved_files_dropdown(self):
        saved_files = self.get_saved_files()
        if saved_files:
            self.saved_files_var.set(saved_files[0])
            menu = self.saved_files_dropdown["menu"]
            menu.delete(0, "end")
            for saved_file in saved_files:
                menu.add_command(label=saved_file, command=tk._setit(self.saved_files_var, saved_file))
        else:
            self.saved_files_var.set("No files available")
            self.saved_files_dropdown["menu"].delete(0, "end")
            self.saved_files_dropdown["menu"].add_command(label="No files available", command=tk._setit(self.saved_files_var, "No files available"))

if __name__ == "__main__":
    root_main = tk.Tk()

    def callback(values):
        print(values)

    # Create an instance of the ExperimentConfigWindow class
    config_window = ExperimentConfigWindow(root_main)
    config_window.callback = callback  # Set the callback attribute

    # Start the Tkinter event loop
    root_main.mainloop()
