import tkinter as tk
from tkinter import messagebox
import json


class ListApp(tk.Tk):  # Inherting only Tk class of tkinter module, not every class.
    def __init__(self):
        super().__init__()

        self.title("To Do List")
        self.resizable(height=False, width=False)  # Disabling the maximize button

        self.lst_names = []

        self.file_class = Json_File(self.lst_names)

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.file_option = tk.Menu(self.menu, tearoff="off")
        self.menu.add_cascade(label="File", menu=self.file_option)

        self.file_option.add_command(label="New", command=self.new_list)
        self.file_option.add_command(label="Save", command=self.save_to_file)
        self.file_option.add_command(label="Exit", command=self.quit)

        self.clicked_var = tk.StringVar()
        self.clicked_var.set("< CHOOSE FROM SAVED LISTS... >")
    
        self.options = self.create_lists_menu()

        # Row 0

        self.options_menu = tk.OptionMenu(self, self.clicked_var, "< CHOOSE FROM SAVED LISTS... >", *self.options)
        self.options_menu.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.options_menu.config(width=50)

        self.open_list_button = tk.Button(self, text="OPEN LIST", command= lambda: self.open_list(self.clicked_var.get()))
        self.open_list_button.grid(row=0, column=2, padx=10, pady=10)
        self.open_list_button.config(width=10)

        # Row 1

        self.name_label = tk.Label(self, text="  LIST NAME:  ")
        self.name_label.grid(row=1, column=0, padx=10, pady=10)

        self.name_box = tk.Entry(self, width=40, borderwidth=5)
        self.name_box.grid(row=1, column=1, padx=10, pady=10)

        self.delete_list_button = tk.Button(self, text=" DELETE LIST ", command=self.delete_list)
        self.delete_list_button.grid(row=1, column=2, padx=10, pady=10)

        # Row 2

        self.item_label = tk.Label(self, text=" ITEM: ")
        self.item_label.grid(row=2, column=0, padx=10, pady=10)

        self.item_box = tk.Entry(self, width=40, borderwidth=5)
        self.item_box.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self, text=" ADD ITEM ", command=self.add_item)
        self.add_button.grid(row=2, column=2, padx=10, pady=10)

        # Row 3

        self.heading_label = tk.Label(self, text="INCOMPLETE TASKS")
        self.heading_label.grid(row=3, column=1, padx=10, pady=10)

        # Row 4

        self.upper_frame = tk.Frame(self)
        self.scrollbar1 = tk.Scrollbar(self.upper_frame, orient=tk.VERTICAL)
        self.incomplete_list_box = tk.Listbox(self.upper_frame, selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar1.set, 
                                              borderwidth=5, width=55, height=10)
        
        
        self.upper_frame.grid(row=4, column=1)
        self.scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar1.config(command=self.incomplete_list_box.yview)

        self.incomplete_list_box.pack()

        # Row 5
        
        self.mark_complete_button = tk.Button(self, text=" MARK AS COMPLETE ", command=self.mark_as_complete)
        self.mark_complete_button.grid(row=5, column=0, padx=10, pady=10)

        self.delete_all_button1 = tk.Button(self, text=" DELETE ALL ", command=lambda: self.delete_all(self.incomplete_list_box))
        self.delete_all_button1.grid(row=5, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self, text=" DELETE ITEM ", command= lambda: self.delete_item(self.incomplete_list_box))
        self.delete_button.grid(row=5, column=2, padx=10, pady=10)

        # Row 6

        self.comp_heading_label = tk.Label(self, text=" COMPLETED TASKS ")
        self.comp_heading_label.grid(row=6, column=1, padx=10, pady=10)

        # Row 7

        self.lower_frame = tk.Frame(self)
        self.scrollbar2 = tk.Scrollbar(self.lower_frame, orient=tk.VERTICAL)
        self.completed_list_box = tk.Listbox(self.lower_frame, selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar2.set,
                                              borderwidth=5, width=55, height=10, fg="grey")
        
        self.lower_frame.grid(row=7, column=1)
        self.scrollbar2.config(command=self.completed_list_box.yview)
        self.scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.completed_list_box.pack()


        # Row 8

        self.mark_incomplete_button = tk.Button(self, text=" MARK AS INCOMPLETE ", command=self.mark_as_incomplete)
        self.mark_incomplete_button.grid(row=8, column=0, padx=10, pady=10)

        self.delete_all_button2 = tk.Button(self, text=" DELETE ALL ", command=lambda: self.delete_all(self.completed_list_box))
        self.delete_all_button2.grid(row=8, column=1, padx=10, pady=10)

        self.delete_button_2 = tk.Button(self, text=" DELETE ITEM ", command= lambda: self.delete_item(self.completed_list_box))
        self.delete_button_2.grid(row=8, column=2, padx=10, pady=10)

        self.bind("<Return>", lambda event: self.add_item())

    def add_item(self):
        try:
            value = self.item_box.get()
            assert self.item_box.get() != ""
        except AssertionError:
            if self.item_box.focus_get() == self.item_box:
                icon = messagebox.showerror("ITEM ERROR", "PLEASE ENTER AN ITEM!!!")
        else:
            self.incomplete_list_box.insert(tk.END, value) # This will insert the value at the end of the list
            self.item_box.delete(0, tk.END)

    def mark_as_complete(self):
        try:
            selected_items = self.incomplete_list_box.curselection()
            assert len(selected_items) != 0
        except AssertionError:
            icon = messagebox.showerror("SELECTION ERROR", "PLEASE SELECT AN ITEM!")
        else:
            for index in selected_items:
                self.completed_list_box.insert(tk.END, self.incomplete_list_box.get(index))  # Same as above where item will be added at the end of the list
            
            self.delete_item(self.incomplete_list_box)


    def mark_as_incomplete(self):
        try:
            selected_items = self.completed_list_box.curselection()
            assert len(selected_items) != 0
        except AssertionError:
            icon = messagebox.showerror("SELECTION ERROR", "PLEASE SELECT AN ITEM!")
        else:
            for index in selected_items:
                self.incomplete_list_box.insert(tk.END, self.completed_list_box.get(index)) # Same as above where item will be added at the end of the list
            self.delete_item(self.completed_list_box)

    def create_lists_menu(self):
        file_data = self.file_class.load_json_file()
        # for lst_name in file_data:
        #     if lst_name != "example_listname" and lst_name != "No. of lists":
        #         lst_names.append(lst_name)
        self.lst_names = [
            lst_name for lst_name in file_data if lst_name != "example_listname" and lst_name != "No. of lists"
        ]
        self.lst_names = list(dict.fromkeys(self.lst_names))  # dict.fromkeys forms a dictionary with keys from list and values set as None. 
        # The above will remove duplicates from the dict and return the list.
        print(self.lst_names)
        return self.lst_names

    def update_lists_menu(self):
        local_menu = self.options_menu["menu"]
        local_menu.delete(0, tk.END)
        for name in self.lst_names:
            local_menu.add_command(label=name, command=lambda value=name: self.clicked_var.set(value))
        print(self.lst_names)

    def save_to_file(self):
        inc_lst = list(self.incomplete_list_box.get(0, tk.END))  # From the first index till the end
        comp_lst = list(self.completed_list_box.get(0, tk.END)) 
        lst_name = self.name_box.get()

        check = self.file_class.check_duplicate_names(lst_name)

        if (len(inc_lst) == 0 and len(comp_lst) == 0) or lst_name == "":
            icon = messagebox.showerror("EMPTY BOX ERROR", "PLEASE ENTER AN ITEM TO SAVE A FILE")
        else:
            read_data = self.file_class.load_json_file()

                # read_data[lst_name]["Incomplete List"] = inc_lst
                # read_data[lst_name]["Completed List"] = comp_lst

            data = {
                    lst_name:
                    {
                    "Incomplete List": inc_lst, 
                    "Completed List": comp_lst
                    }
                    }
            if check == 0:
                # Getting the total number of lists
                no_of_lists = read_data["No. of lists"]
                
                # Updating the number of files
                read_data.update({"No. of lists": no_of_lists + 1})
            
            read_data.update({lst_name : data[lst_name]})  # Adding new list
            
            # Writing the data
            self.file_class.write_to_json_file(read_data)  # dump(data to be saved, file name )

            self.create_lists_menu()  # Updating the lst_names variable
            self.update_lists_menu()  # Updating the Option Menu

    def delete_list(self):
        data = self.file_class.load_json_file()
        list_name = self.name_box.get()
        icon = messagebox.askokcancel("WARNING", f"THE CURRENT LIST {list_name} WILL BE DELETED! CONFIRM? ")
        if icon == 1:
            try:
                del data[list_name]
            except KeyError:
                icon = messagebox.showerror("KEY ERROR", "NO SUCH LIST HAS BEEN FOUND!!")
            else:
                no_of_lists = data["No. of lists"]
                data.update({"No. of lists": no_of_lists-1})
                self.file_class.write_to_json_file(data)
                self.name_box.delete(0, tk.END)
                self.incomplete_list_box.delete(0, tk.END)
                self.completed_list_box.delete(0, tk.END)
                self.clicked_var.set("< CHOOSE FROM SAVED LISTS... >")
                self.create_lists_menu()
                self.update_lists_menu()


    def restart(self):
        icon = messagebox.askokcancel("RESTART", "THE PROGRAM WILL NOW RESTART WITH YOUR SAVED CHANGES")
        if icon == 1:
            self.quit()
            


    def new_list(self):
        icon = messagebox.askokcancel("WARNING", 
                                      """PLEASE SAVE YOUR LIST BEFORE MAKING A NEW LIST OR  ALL DATA WILL BE LOST! CLICK OK IF YOU HAVE ALREADY SAVED!
                                      """)
        if icon == 1:
            self.incomplete_list_box.delete(0, tk.END)
            self.completed_list_box.delete(0, tk.END)
            self.name_box.delete(0, tk.END)
            self.item_box.delete(0, tk.END)

    def open_list(self, list_name):
        self.incomplete_list_box.delete(0, tk.END)
        self.completed_list_box.delete(0, tk.END)
        self.name_box.delete(0, tk.END)
        self.name_box.insert(0, list_name)
        if self.clicked_var.get() != "< CHOOSE FROM SAVED LISTS... >":
            read_data = self.file_class.load_json_file()
            inc_list = read_data[list_name]["Incomplete List"]
            comp_list = read_data[list_name]["Completed List"]
            for incomplete_item in inc_list:
                self.incomplete_list_box.insert(tk.END, incomplete_item)
            for completed_item in comp_list:
                self.completed_list_box.insert(tk.END, completed_item)

    @staticmethod
    def delete_item(list_box):
        try:
            selected_items = list_box.curselection()
            assert len(selected_items) != 0
        except AssertionError:
            icon = messagebox.showerror("SELECTION ERROR", "PLEASE SELECT AN ITEM!")
        else:
            for item in selected_items[::-1]:
                list_box.delete(item)

    @staticmethod
    def delete_all(list_box):
        list_box.delete(0, tk.END)

class Json_File:
    def __init__(self, lst_names):
        self.lst_names = lst_names

    def check_duplicate_names(self, lst_names):
        data = self.load_json_file()
        for name in data:
            if name == lst_names:
                icon = messagebox.askyesno("NAME ISSUE", "A LIST ALREADY EXISTS WITH THIS NAME. DO YOU WANT TO OVERWRITE IT?")

    @staticmethod
    def load_json_file():
        with open("Stored_files.json", "r") as json_file:
            data = json.load(json_file)
            return data

    @staticmethod
    def write_to_json_file(data):
        with open("Stored_files.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
 

app = ListApp()
app.mainloop()

