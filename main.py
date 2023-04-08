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
        self.geometry("1920x1080")

        self.current_img_path = None
        self.current_img = None
        self.img_idx = -1
        self.img_list = []
        self.bboxes = []

        self.load_images()

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        self.show_next_image()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Adding buttons and input box
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
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img

    def on_left_click(self, event):
        x, y = event.x, event.y
        if len(self.bboxes) == 0:
            self.bboxes.append((x, y))
        else:
            x1, y1 = self.bboxes[0]
            self.bboxes.append((x, y))
            self.canvas.create_rectangle(x1, y1, x, y, outline="red", width=2)

    def on_right_click(self, event):
        x, y = event.x, event.y
        for idx, bbox in enumerate(self.bboxes):
            if bbox[0] - 10 <= x <= bbox[0] + 10 and bbox[1] - 10 <= y <= bbox[1] + 10:
                self.bboxes.pop(idx)
                break
        self.display_image()
        for bbox in self.bboxes:
            self.canvas.create_rectangle(bbox[0] - 10, bbox[1] - 10, bbox[0] + 10, bbox[1] + 10, outline="red", width=2)

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