import io
import webbrowser
import requests
from tkinter import *
from tkinter import ttk
from urllib.request import urlopen
from PIL import ImageTk, Image

class NewsApp:
    def __init__(self):
        # fetch data
        self.data = requests.get(
            'https://newsapi.org/v2/top-headlines?country=in&apiKey=07ce6431517e45c5b04b589c36e5bed6'
        ).json()
        # initial GUI load
        self.load_gui()
        # load the 1st news item
        self.load_news_item(0)

    def load_gui(self):
        self.root = Tk()
        self.root.geometry('400x750')  # Increased height
        self.root.resizable(0, 0)
        self.root.title('Mera News App')
        self.root.configure(background='#2c3e50')  # Dark blue background

        # Create a custom style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 12), borderwidth=1)
        style.map('TButton', background=[('active', '#3498db')], foreground=[('active', 'white')])

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_item(self, index):
        # clear the screen for the new news item
        self.clear()

        # Create a main frame
        main_frame = Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=BOTH, expand=True)

        # Create a canvas
        canvas = Canvas(main_frame, bg='#2c3e50')
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create another frame inside the canvas
        inner_frame = Frame(canvas, bg='#2c3e50')

        # Add that new frame to a window in the canvas
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # image
        try:
            img_url = self.data['articles'][index]['urlToImage']
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((400, 300))
            photo = ImageTk.PhotoImage(im)
        except:
            img_url = 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg'
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((400, 300))
            photo = ImageTk.PhotoImage(im)

        label = Label(inner_frame, image=photo)
        label.image = photo
        label.pack(pady=(0, 20))

        heading = Label(inner_frame,
                        text=self.data['articles'][index]['title'],
                        bg='#2c3e50',
                        fg='#ecf0f1',  # Light gray text
                        wraplength=380,
                        justify='center')
        heading.pack(pady=(10, 20))
        heading.config(font=('Arial', 16, 'bold'))

        details = Label(inner_frame,
                        text=self.data['articles'][index]['description'],
                        bg='#2c3e50',
                        fg='#bdc3c7',  # Lighter gray text
                        wraplength=380,
                        justify='center')
        details.pack(pady=(2, 20))
        details.config(font=('Arial', 12))

        button_frame = Frame(inner_frame, bg='#2c3e50')
        button_frame.pack(expand=True, fill=X, pady=(20, 0))

        if index != 0:
            prev = ttk.Button(button_frame,
                              text='Previous',
                              width=12,
                              command=lambda: self.load_news_item(index - 1))
            prev.pack(side=LEFT, padx=(10, 5))

        read = ttk.Button(button_frame,
                          text='Read More',
                          width=12,
                          command=lambda: self.open_link(self.data['articles'][index]['url']))
        read.pack(side=LEFT, padx=5)

        if index != len(self.data['articles']) - 1:
            next = ttk.Button(button_frame,
                              text='Next',
                              width=12,
                              command=lambda: self.load_news_item(index + 1))
            next.pack(side=LEFT, padx=(5, 10))

        self.root.mainloop()

    def open_link(self, url):
        webbrowser.open(url)

obj = NewsApp()