import tkinter as tk
import requests
import time
import threading


def get_text(usr_input):
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': usr_input,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True
        }
    ).json()
    page = next(iter(response['query']['pages'].values()))
    text = page['extract']
    return text

def run():
    global result
    usr_input = topic.get()
    try:
        text = get_text(usr_input)
    except:
        ErrorFrame()


    if usr_input not in text:
        usr_input = usr_input.title()
        text = get_text(usr_input)
        divided = usr_input.split()
        contains = False
        for i in divided:
            print(i)
            if i in text:
                contains = True
        if not contains:
            return ErrorFrame()

    if "may refer to:" in text:
        return ErrorFrame()
    if "commonly refers to:" in text:
        return ErrorFrame()
    if "primarily refers to:" in text:
        return ErrorFrame()
    if "often refers to:" in text:
        return ErrorFrame()

    result = text
    result = result.replace("  ", " ")
    result = result.replace("–", "-")
    result = result.replace("e.g.", "for exapmle")
    result = result.replace("\n", " ")

    i = 0
    while i < len(result):
        if result[i].isascii():
            i += 1
        else:
            result = result.replace(result[i], "")

    global line_array
    line_array = ["" for i in range(result.count("."))]
    f = 0
    k = 0

    while f < len(result):
        if result[f] == ".":
            if f + 1 >= len(result):
                line_array[k] += "."
                break
            elif result[f + 1] == " ":
                f += 2
            else:
                f += 1
            line_array[k] += "."
            k += 1
        else:
            if k + 1 > len(line_array):
                break
            else:
                line_array[k] += result[f]
                f += 1

    AppGUI()


def return_start(event):
    run()


class MainGUI(tk.Tk):
    error_win = 0

    def __init__(self):
        super().__init__()
        global topic
        topic = tk.StringVar()

        window_width = 800
        window_height = 500

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title("Mainmenu")

        self.backGroundImage = tk.PhotoImage(file="wm_sharpen_white.png")
        self.backGroundImageLabel = tk.Label(self, image=self.backGroundImage)
        self.backGroundImageLabel.place(x=0, y=0)

        self.get_label = tk.Label(self, text="Welcome to Typsy!\nPlease write what topic you would like to use:",
                                  font=("Times", 18), bg="White")
        self.get_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.topic_entry = tk.Entry(self, font=("Helvetica", 18), width=40, textvariable=topic, bd=4)
        self.topic_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.topic_entry.bind("<Return>", return_start)

        self.get_button = tk.Button(self, text="Get topic", font=("Helvetica", 12), command=run)
        self.get_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.opened = False


class AppGUI(tk.Toplevel):
    current = 0

    def __init__(self):
        super().__init__()

        self.geometry("1920x1080")
        self.title("Typsy")
        self.state("zoomed")
        self.resizable(False, False)

        self.backGroundImage = tk.PhotoImage(file="TypsylogoBig.png")
        self.backGroundImageLabel = tk.Label(self, image=self.backGroundImage)
        self.backGroundImageLabel.place(x=0, y=0)

        self.start_label = tk.Label(self, text="Press the start button to start", font=("Times", 16, "bold"),
                                    wraplength=1000, bg="White")
        self.start_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.next_button = tk.Button(self, text="Next line", font=("Helvetica", 12), command=self.next_line)

        self.start_button = tk.Button(self, text="Start", font=("Helvetica", 15), command=self.start)
        self.start_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.input_entry = tk.Text(self, width=60, height=3, font=("Helvetica", 18), bd=4)

        self.speed_label = tk.Label(self, text="Speed: \n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPM",
                                    font=("Helvetica", 18), bg="White")

        self.reset_button = tk.Button(self, text="Reset", font=("Helvetica", 12), command=self.reset)

        self.last_line = tk.Button(self, text="Previous line", font=("Helvetica", 12), command=self.previous_line,
                                   state=tk.DISABLED)

        self.counter = 0
        self.running = False

        AppGUI.mainloop(self)

    def start(self):
        self.start_label.config(text=line_array[0])
        self.start_button.destroy()

        self.input_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.input_entry.bind("<KeyRelease>", self.go)

        self.last_line.place(relx=0.45, rely=0.6, anchor=tk.CENTER)

        self.next_button.place(relx=0.55, rely=0.6, anchor=tk.CENTER)

        self.reset_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.speed_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    def next_line(self):

        self.current += 1
        if self.current > 0:
            self.last_line.config(state=tk.NORMAL)

        if self.current == len(line_array) - 1:
            self.next_button.config(state=tk.DISABLED)

        self.start_label.config(text=line_array[self.current])
        self.reset()

    def previous_line(self):
        self.current -= 1
        if self.current < len(line_array):
            self.next_button.config(state=tk.NORMAL)

        if self.current == 0:
            self.last_line.config(state=tk.DISABLED)

        self.start_label.config(text=line_array[self.current])
        self.reset()

    finished = False

    def go(self, event):
        global t
        if not self.running and not self.finished:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        if not self.start_label.cget("text").startswith(self.input_entry.get("1.0", 'end-1c')):
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")
        if self.input_entry.get("1.0", 'end-1c') == self.start_label.cget("text"):
            self.running = False
            t.join(0)
            self.input_entry.config(fg="green", state="disabled")
            self.finished = True

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            cps = len(self.input_entry.get("1.0", 'end-1c')) / self.counter
            cpm = cps * 60
            wps = len(self.input_entry.get("1.0", 'end-1c').split(" ")) / self.counter
            wpm = wps * 60
            self.speed_label.config(text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM\n{wps: .2f} WPS\n{wpm: .2f} WPM")

    def reset(self):
        t.join(0.25)
        self.finished = False
        self.running = False
        self.counter = 0
        self.speed_label.config(text="Speed: \n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPM")
        self.input_entry.config(state="normal")
        self.input_entry.delete("1.0", "end")


class ErrorFrame(tk.Toplevel):

    def __init__(self):
        super(ErrorFrame, self).__init__()

        self.geometry("300x100")
        self.title("Error")
        self.frame = tk.Frame(self)
        self.frame.pack(expand=True)
        self.resizable(False, False)
        self.bell()
        self.focus_force()
        self.lift()

        self.Error_Label = tk.Label(self, text="Unfortunately the desired topic is not available.\n"
                                               "Please specify a diffrent one.", font=("Helvetica", 10))
        self.Error_Label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        self.ok_button = tk.Button(self, text="Ok", command=self.close)
        self.ok_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def close(self):
        self.destroy()


app = MainGUI()
app.mainloop()
