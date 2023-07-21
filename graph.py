import requests
import tkinter
from tkinter import messagebox

# Pixela API Endpoint
ENDPOINT = "https://pixe.la/v1/users"

class Graph():
    def __init__(self):
        self.token, self.username, self.id = '', '', ''
        self.header = None

        # Try to find the user.txt file that contains the user's username, token, and graph id to make requests, and create it if it's not found
        # The user.txt file consists of the user's username on the first line, the user's token on the second line, and the graph id on the last line
        try:
            with open('./user.txt', mode='r') as file:
                content = file.readlines()
                self.username = content[0].strip()
                self.token = content[1].strip()
                self.id = content[2].strip()
        except:
            with open('./user.txt', mode='w') as file:
                self.make_user()
                file.write(self.username + '\n' + self.token + '\n' + self.id)

        self.req_graph(self.username, self.token, self.id)

    # Request to post a graph
    def req_graph(self, username, token, id):
        graph_prm = {
            "id": id,
            "name": "Daily Study Graph",
            "unit": "Hour",
            "type": "float",
            "color": "ichou" # Choose the color graph between shibafu (green), momiji (red), sora (blue), ichou (yellow), ajisai (purple) and kuro (black)
        }
        self.header = {
            "X-USER-TOKEN": token
        }
        response = requests.post(url=f"{ENDPOINT}/{username}/graphs", json=graph_prm, headers=self.header).json()

    # Make a new Pixela user if the user does not have it
    def make_user(self):
        self.window = None
        self.existing = True
        self.new_to_pixela()

    # Add a new pixel to the graph
    def add_pixel(self, hr, today):
        pixel_prm = {
            "date": today,
            "quantity": str(hr)
        }
        # The requests will be rejected 25% of the time, so by making a while loop, it will try to make requests until successful
        while True:
            response = requests.post(url=f"{ENDPOINT}/{self.username}/graphs/{self.id}", json=pixel_prm, headers=self.header)
            if response.json()['isSuccess'] == True:
                break

    # Returns a fail notification if the process of making a new user is encountering errors
    def valid(self, username, token, id, existing):
        if existing:
            self.req_graph(username, token, id)
            return ("Successful.", True)
        else:
            user_param = {
                "token": token,
                "username": username,
                "agreeTermsOfService": "yes",
                "notMinor": "yes"
            }
            response = requests.post(url=ENDPOINT, json=user_param).json()
            print(response)
            if response['isSuccess']:
                return ("Successful.", True)
            else:
                return ('Try again. Username or token may already be taken or not follow the requirements.', False)

    # User interface to ask whether the user have or don't have a Pixela account
    def new_to_pixela(self):
        self.window = tkinter.Tk()
        self.window.config(padx=50, pady=50, bg='white')
        self.window.title("New to Pixela?")
        l1 = tkinter.Label(text="Do you already have a Pixela account and graph?")
        l1.grid(row=0, column=0, columnspan=2)
        yes = tkinter.Button(text='Yes', command=self.sign_in, width=18)
        yes.grid(row=1, column=0)
        no = tkinter.Button(text='No', command=self.sign_up, width=17)
        no.grid(row=1, column=1)
        self.window.mainloop()

    # User interface to insert username, token, and graph ID
    def ui(self, title):
        self.window = tkinter.Tk()
        self.window.config(padx=50, pady=50, bg='white')
        self.window.title(title)

        self.l1 = tkinter.Label(text="Username:", bg='white')
        self.l1.grid(row=0, column=0, sticky="e")
        self.l2 = tkinter.Label(text="Token:", bg='white')
        self.l2.grid(row=1, column=0, sticky="e")
        self.l3 = tkinter.Label(text="Graph ID:", bg='white')
        self.l3.grid(row=2, column=0, sticky="e")

        self.e1 = tkinter.Entry(width=30, relief='solid')
        self.e1.grid(row=0, column=1)
        self.e2 = tkinter.Entry(width=30, relief='solid')
        self.e2.grid(row=1, column=1)
        self.e3 = tkinter.Entry(width=30, relief='solid')
        self.e3.grid(row=2, column=1)

        self.b1 = tkinter.Button(text=title, width=34, command=self.check)
        self.b1.grid(row=3, column=0, columnspan=3)

        self.window.mainloop()

    # Sign in for existing users
    def sign_in(self):
        self.window.destroy()
        self.ui('Sign In')

    # Sign up for new users
    def sign_up(self):
        self.window.destroy()
        self.existing = False
        self.ui('Sign Up')

    # Check the user's input's validation
    def check(self):
        self.username = self.e1.get()
        self.token = self.e2.get()
        self.id = self.e3.get()
        msg_box = self.valid(self.username, self.token, self.id, self.existing)
        messagebox.showinfo(title="Notification", message=msg_box[0])
        if msg_box[1]:
            self.window.destroy()
        else:
            self.e1.delete(0, tkinter.END)
            self.e2.delete(0, tkinter.END)
            self.e3.delete(0, tkinter.END)
