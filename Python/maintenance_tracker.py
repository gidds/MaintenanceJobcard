import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
from datetime import datetime
from tkcalendar import DateEntry
import configparser 
import os

class MaintenanceTracker:
    def __init__(self, master):
        self.master = master
        config = configparser.ConfigParser()
        config.read('config.ini')
        if config.has_section('settings') and config.has_option('settings', 'jobcards_file_path'):
            self.jobcards_file_path = config['settings']['jobcards_file_path']
        else:
            self.jobcards_file_path = None
            
        self.master.title("Maintenance Tracker")
        self.master.geometry("800x600")
    
    
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both")
    
    
        self.create_jobcard_frame()
        self.create_search_frame()
    
        # Load existing jobcards
        if self.jobcards_file_path is None or not os.path.exists(self.jobcards_file_path):
            self.set_jobcards_file_path()
        self.load_jobcards()
        
    def set_jobcards_file_path(self):
        """Sets the userjobcards.xml file path."""
        file_path = filedialog.asksaveasfilename(title="Select or create jobcards file",
                                                 defaultextension=".xml",
                                                 filetypes=[("XML files", "*.xml")])
        if file_path:
            self.jobcards_file_path = file_path
            config = configparser.ConfigParser()
            config.read('config.ini')
            if not config.has_section('settings'):
                config.add_section('settings')
            config.set('settings', 'jobcards_file_path', file_path)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            print(f"Jobcards file path set to: {file_path}")
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write('<?xml version="1.0" encoding="UTF-8"?><jobcards></jobcards>')
                print(f"Created new jobcards file at: {file_path}")
        else:
            print("No file selected.")

    def create_jobcard_frame(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Create Jobcard")

        # Add form fields
        fields = [
            "Requisition Number", "Jobcard Number", "Requested By", "Date",
            "Time Start", "Time Stop", "Fault Description", "Department",
            "Machine", "Work Carried Out", "Type of Fault", "Artisan", "Apprentice"
        ]

        self.entries = {}
        for i, field in enumerate(fields):
            ttk.Label(frame, text=field).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            
            if field == "Date":
                self.entries[field] = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
                self.entries[field].grid(row=i, column=1, padx=5, pady=5)
            elif field in ["Time Start", "Time Stop"]:
                time_frame = ttk.Frame(frame)
                hour = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(24)], width=3)
                minute = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(60)], width=3)
                hour.pack(side=tk.LEFT)
                ttk.Label(time_frame, text=":").pack(side=tk.LEFT)
                minute.pack(side=tk.LEFT)
                self.entries[field] = (hour, minute)
                time_frame.grid(row=i, column=1, padx=5, pady=5)
            else:
                self.entries[field] = ttk.Entry(frame)
                self.entries[field].grid(row=i, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Submit", command=self.save_jobcard).grid(row=len(fields), column=1, pady=10)

    def create_search_frame(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Search Jobcard")

        ttk.Label(frame, text="Search by:").grid(row=0, column=0, padx=5, pady=5)
        self.search_type = ttk.Combobox(frame, values=["Requisition Number", "Jobcard Number"])
        self.search_type.grid(row=0, column=1, padx=5, pady=5)
        self.search_type.current(0)
        self.search_type.bind("<<ComboboxSelected>>", self.update_search_options)

        ttk.Label(frame, text="Search value:").grid(row=1, column=0, padx=5, pady=5)
        self.search_entry = ttk.Combobox(frame)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_search_options)

        ttk.Button(frame, text="Search", command=self.search_jobcard).grid(row=2, column=1, pady=10)

        self.result_text = tk.Text(frame, height=20, width=60)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def load_jobcards(self):
        try:
            tree = ET.parse(self.jobcards_file_path)
            root = tree.getroot()
            self.jobcards = {
                'requisition-number': set(),
                'jobcard-number': set()
            }
            for jobcard in root.findall('jobcard'):
                req_num = jobcard.find('requisition-number')
                job_num = jobcard.find('jobcard-number')
                if req_num is not None and req_num.text:
                    self.jobcards['requisition-number'].add(req_num.text)
                if job_num is not None and job_num.text:
                    self.jobcards['jobcard-number'].add(job_num.text)
        except Exception as e:
            print(f"Error loading jobcards: {str(e)}")
            messagebox.showerror("Error", f"Error loading jobcards: {str(e)}")

    def update_search_options(self, event=None):
        search_type = self.search_type.get().lower().replace(' ', '-')
        self.search_entry['values'] = list(self.jobcards[search_type])

    def filter_search_options(self, event=None):
        search_type = self.search_type.get().lower().replace(' ', '-')
        current_text = self.search_entry.get().lower()
        filtered_options = [option for option in self.jobcards[search_type] if current_text in option.lower()]
        self.search_entry['values'] = filtered_options

    def save_jobcard(self):
        try:
            tree = ET.parse(self.jobcards_file_path)
            root = tree.getroot()

            new_jobcard = ET.Element('jobcard')
            for field, entry in self.entries.items():
                if field == "Date":
                    value = entry.get_date().strftime("%Y-%m-%d")
                elif field in ["Time Start", "Time Stop"]:
                    hour, minute = entry
                    value = f"{hour.get()}:{minute.get()}"
                else:
                    value = entry.get()
                ET.SubElement(new_jobcard, field.lower().replace(' ', '-')).text = value

            ET.SubElement(new_jobcard, 'timestamp').text = datetime.now().isoformat()

            root.append(new_jobcard)
            tree.write(self.jobcards_file_path)

            messagebox.showinfo("Success", "Job card saved successfully!")
            for field, entry in self.entries.items():
                if field == "Date":
                    entry.set_date(datetime.now())
                elif field in ["Time Start", "Time Stop"]:
                    hour, minute = entry
                    hour.set("")
                    minute.set("")
                else:
                    entry.delete(0, tk.END)
            
            # Reload jobcards after saving
            self.load_jobcards()
        except Exception as e:
            print(f"Error saving job card: {str(e)}")
            messagebox.showerror("Error", f"Error saving job card: {str(e)}")

    def search_jobcard(self):
        search_type = self.search_type.get().lower().replace(' ', '-')
        search_input = self.search_entry.get()

        try:
            tree = ET.parse(self.jobcards_file_path)
            root = tree.getroot()

            result = "No matching jobcard found."
            for jobcard in root.findall('jobcard'):
                if jobcard.find(search_type) is not None and jobcard.find(search_type).text == search_input:
                    result = "Jobcard Details:\n\n"
                    for child in jobcard:
                        result += f"{child.tag.replace('-', ' ').title()}: {child.text}\n"
                    
                    # Calculate time spent
                    time_start = datetime.strptime(jobcard.find('time-start').text, "%H:%M")
                    time_stop = datetime.strptime(jobcard.find('time-stop').text, "%H:%M")
                    time_diff = time_stop - time_start
                    hours, remainder = divmod(time_diff.seconds, 3600)
                    minutes = remainder // 60
                    result += f"\nTime Spent: {hours} hours and {minutes} minutes"
                    
                    break

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            print(f"Error searching job card: {str(e)}")
            messagebox.showerror("Error", f"Error searching job card: {str(e)}")
        

if __name__ == "__main__":
    root = tk.Tk()
    app = MaintenanceTracker(root)
    root.mainloop()
