import tkinter
from graph import Graph
import webbrowser
from datetime import datetime

# Background color of the User Interface
BACKGROUND = "#c474f0"

class Interface:
    def __init__(self, graph: Graph):
        # Try to open a data.txt file that contains the study time of today and create it if it does not exist
        # The data.txt consists of today's date on the first line and how long you've studied on the second line
        try:
            with open("./data.txt", mode="r") as file:
                pass
        except:
            with open("./data.txt", mode="w") as file:
                today = datetime.today()
                today = today.strftime("%Y%m%d")
                file.write(today + "\n0")
                data = [today, "0"]
                print(data)
        finally:
            with open("./data.txt", mode="r") as file:
                data = file.readlines()
                today = datetime.today()
                today = today.strftime("%Y%m%d")    
                if data[0].strip("\n") == today:
                    self.passed = float(data[1])
                else:
                    with open("./data.txt", mode="w") as file:
                        file.write(today + "\n0")
                    self.passed = 0
                
        self.h, self.m, self.s, self.switch = 0, 0, 0, 0
        self.timer = None
        self.today = today
        self.graph = graph

        # Creating the User Interface
        self.window = tkinter.Tk()
        self.window.config(width=500, height=500, padx=30, pady=30, bg=BACKGROUND)
        self.window.title("Daily Study")

        self.clock_img = tkinter.PhotoImage(file="./Clock.png")

        self.canvas = tkinter.Canvas(bg=BACKGROUND, width=150, height=150, highlightthickness=0)
        self.canvas.create_image(75, 75, image=self.clock_img)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.stopwatch = tkinter.Label(text="00:00:00", font=("Times New Roman", 20, "bold"), bg=BACKGROUND, pady=20)
        self.stopwatch.grid(row=1, column=0, columnspan=3)

        self.start = tkinter.Button(text="Start", width=10, command=self.start_stopwatch)
        self.start.grid(row=2, column=0)
        self.pause = tkinter.Button(text="Pause", width=10, command=self.pause_stopwatch, state="disabled")
        self.pause.grid(row=2, column=1, padx=10)
        self.update = tkinter.Button(text="Update", width=10, command=self.update_graph)
        self.update.grid(row=2, column=2)
        self.show = tkinter.Button(text="Show Journey", command=self.web, width=37)
        self.show.grid(row=3, column=0, columnspan=3, pady=10)

        self.window.mainloop()

    # Increment the seconds of the clock and adjusts the minutes and hours accordingly
    def increment(self):
        if self.s == 60:
            self.m += 1
            self.s = 0
        if self.m == 60:
            self.h += 1
            self.m = 0
        sec = self.s
        min = self.m
        hr = self.h
        if sec < 10:
            sec = "0" + str(sec)
        if min < 10:
            min = "0" + str(min)
        if hr < 10:
            hr = "0" + str(hr)
        
        self.stopwatch.config(text=f"{hr}:{min}:{sec}")
        self.timer = self.window.after(1000, self.increment)
        self.s += 1

    # Start the stopwatch
    def start_stopwatch(self):
        self.start.config(state="disabled")
        self.pause.config(state="active")
        self.increment()

    # Pause or continue the stopwatch 
    def pause_stopwatch(self):
        if self.switch % 2 == 0:
            self.pause.config(text="Continue")
            self.window.after_cancel(self.timer)
        else:
            self.pause.config(text="Pause")
            self.s -= 1
            self.increment()
        self.switch += 1

    # Update the time to Pixela graph
    def update_graph(self):
        self.window.after_cancel(self.timer)
        self.passed += self.h + (self.m / 60) + (self.s / 3600)
        self.graph.add_pixel(self.passed, self.today)
        self.reset()

    # Take the user to the Pixela graph on the browser to see their progress
    def web(self):
        webbrowser.open(url=f"https://pixe.la/v1/users/{self.graph.username}/graphs/{self.graph.id}.html", new=2)  

    # After the graph updates, the stopwatch resets
    # After the stopwatch resets, the new study time will be incremented to the data.txt as long as the program is run on the same day
    def reset(self):
        with open("./Projects/DailyStudy/data.txt", mode="w") as file:
            file.write(self.today + "\n" + str(self.passed))
        self.h, self.m, self.s, self.switch = 0, 0, 0, 0
        self.stopwatch.config(text="00:00:00")
        self.start.config(state="active")
        self.pause.config(text="Pause", state="disabled")

