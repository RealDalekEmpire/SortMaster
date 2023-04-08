import os
import csv
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageSorter(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Image Sorter")
        self.geometry("2048x1536")

        self.current_img_path = None
        self.current_img = None
        self.img_idx = -1
        self.img_list = []
        self.bboxes = []
        self.x = None
        self.y = None
        self.rectangle = None

        # Create buttons before loading images
        self.create_buttons()

        self.load_images()

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        
        self.canvas.bind("<ButtonPress-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind('<Motion>', self.mouse_move_label)
        self.canvas.bind('<B1-Motion>', self.on_left_click_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_click_release)
        
        self.h_line = self.canvas.create_line(0, 0, 0, self.canvas.winfo_height(), fill='gold',width=2)
        self.v_line = self.canvas.create_line(0, 0, self.canvas.winfo_width(), 0, fill='gold',width=2)
        

        self.show_next_image()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_buttons(self):
        self.day_night_var = tk.IntVar(value=1)
        self.snow_var = tk.IntVar(value=0)
        self.object_var = tk.IntVar()
        self.obj_class_var = tk.StringVar()
        self.day_button = tk.Radiobutton(self, text="Day", variable=self.day_night_var, value=1)
        self.night_button = tk.Radiobutton(self, text="Night", variable=self.day_night_var, value=0)
        self.snow_button = tk.Radiobutton(self, text="Snow", variable=self.snow_var, value=1)
        self.no_snow_button = tk.Radiobutton(self, text="No Snow", variable=self.snow_var, value=0)
        self.object_button = tk.Checkbutton(self, text="Object", variable=self.object_var)
        self.obj_class_entry = tk.Entry(self, textvariable=self.obj_class_var)

        self.day_button.pack(side=tk.LEFT)
        self.night_button.pack(side=tk.LEFT)
        self.snow_button.pack(side=tk.LEFT)
        self.no_snow_button.pack(side=tk.LEFT)
        self.object_button.pack(side=tk.LEFT)
        self.obj_class_entry.pack(side=tk.LEFT)

        self.next_button = tk.Button(self, text="Next", command=self.save_and_next)
        self.next_button.pack(side=tk.LEFT)

    def load_images(self):
        folder_path = filedialog.askdirectory(title="Select Image Folder")
        self.img_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".jpg")]
        self.load_progress()

    def load_progress(self):
        if os.path.exists("progress.csv"):
            with open("progress.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    img_path = row[0]
                    if img_path in self.img_list:
                        self.img_list.remove(img_path)

    def save_progress(self, data):
        with open("progress.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def show_next_image(self):
        self.img_idx += 1
        if self.img_idx < len(self.img_list):
            self.current_img_path = self.img_list[self.img_idx]
            self.current_img = cv2.imread(self.current_img_path)
            self.display_image()
        else:
            self.canvas.create_text(400, 300, text="All images sorted!", font=("Arial", 24), fill="red")

    def display_image(self):
        img = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2RGB)

        # Calculate average brightness
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        avg_brightness = cv2.mean(gray)[0]

        print(avg_brightness)
        # Set night radio button if avg_brightness is <= 15
        if avg_brightness <= 100:
            self.night_button.select()
        else:
            self.day_button.select()

        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img

    def mouse_move_label(self,event):
        self.canvas.lift(self.h_line)
        self.canvas.lift(self.v_line)
        x, y = event.x, event.y
        self.canvas.coords(self.h_line, 0, y, self.canvas.winfo_width(), y)
        self.canvas.coords(self.v_line, x, 0, x, self.canvas.winfo_height())

    def on_left_click(self, event):
        if event.num == 1:  # Check if the left mouse button was clicked
            self.x, self.y = event.x, event.y
            self.rectangle = self.canvas.create_rectangle(self.x,self.y,1,1,outline='red',width=2
            self.bboxes.append((self.x, self.y)
    
    def on_left_click_drag(self,event):
        x1, y1 = event.x, event.y
        self.canvas.coords(self.rectangle, self.x, self.y, x1, y1)
        self.canvas.coords(self.h_line, 0, y1, self.canvas.winfo_width(), y1)
        self.canvas.coords(self.v_line, x1, 0, x1, self.canvas.winfo_height())

    def on_left_click_release(self, event):
        x1, y1 = event.x, event.y
        self.bboxes.append((x1,y1))
    

        
    def on_right_click(self, event):
        if event.num == 3:  # Check if the right mouse button was clicked
            x, y = event.x, event.y
            self.bboxes = []
            
            self.display_image()

    def save_and_next(self):
        day_night = self.day_night_var.get()
        snow = self.snow_var.get()
        obj = self.object_var.get()
        obj_class = self.obj_class_var.get()

        data = [self.current_img_path, day_night, snow, obj, obj_class] + self.bboxes
        self.save_progress(data)

        self.bboxes = []
        self.object_var.set(0)  # Clear object variable
        self.obj_class_var.set("")  # Clear objClass variable
        self.show_next_image()

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    app = ImageSorter()
    app.mainloop()
