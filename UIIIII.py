import tkinter as tk
import joblib
from tkinter import filedialog
from eog_final import preprocessing_each_pair
import random

# load model
clf = joblib.load("model.joblib")
# load accuracy
accuracy = joblib.load("result.text")

print(accuracy)


def restart_game():
    # if there is an any type of collision(lose, win) so we need to delete text
    if check_overlap(0) == 1:
        canvas.delete(text)
    canvas.coords(circle, 50, 50, 110, 110)


# Create a "Restart" button on the canvas


def check_overlap(write):
    # Get the ids of all the items that overlap with the first shape
    intersetion = canvas.find_overlapping(*canvas.coords(circle))
    global text
    # Check if the id of the second shape is in the list of overlapping items
    if obstacle in intersetion:
        if write == 1:
            text = canvas.create_text(250, 100, text="Game over", font=("Arial", 24), fill="black")
        print("Try again!!")
        return 1
    elif end_line in intersetion:
        if write == 1:
            text = canvas.create_text(250, 100, text="You Win", font=("Arial", 24), fill="blue")
            print("You Win!!")
        return 1


def change_color():
    # Generate a random RGB color value
    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    color = f"#{r:02x}{g:02x}{b:02x}"  # Convert the RGB values to a hex color code

    canvas.itemconfig(circle, fill=color, outline=color)


def move_circle(prediction):

    a = check_overlap(0)
    if a == 1:
        return ""
    else:
        if prediction == 1:
            move = 'up'
            canvas.move(circle, 0, -60)

        elif prediction == 0:
            move = 'down'
            canvas.move(circle, 0, 60)

        elif prediction == 3:
            move = 'left'
            canvas.move(circle, -60, 0)

        elif prediction == 2:
            move = 'rigth'
            canvas.move(circle, 60, 0)

        elif prediction == 4:
            move = 'blink'
            change_color()
        print("prediction: ", move, "\n")
        check_overlap(1)  # check if there is a collision after moving


def browse_file():
    file_path1 = filedialog.askopenfilename()
    print("horizonital signal: ", file_path1.split('/')[-1])

    file_path2 = filedialog.askopenfilename()
    print("vertical signal: ", file_path2.split('/')[-1])

    batch = []
    pair = []
    with open(file_path1, 'r') as f:
        lines = f.readlines()
        amp1 = []
        # horizontal first
        for i in range(len(lines) - 1):
            L = lines[i]
            amp1.append(int(L))
        # vertical first
    pair.append(amp1)
    with open(file_path2, 'r') as f:
        lines = f.readlines()
        amp2 = []
        for i in range(len(lines) - 1):
            L = lines[i]
            amp2.append(int(L))
    pair.append(amp2)
    batch.append(pair)
    ready_data = preprocessing_each_pair(batch, None)
    move_circle(clf.predict(ready_data))


window = tk.Tk()
window.title("EOG Moving Objects")

# create a canvas
canvas = tk.Canvas(window, width=400, height=400)
canvas.pack()

# create a circle on the canvas

circle = canvas.create_oval(50, 50, 110, 110, fill="yellow", outline="green")
obstacle = canvas.create_rectangle(200, 150, 250, 400, fill="red", outline="blue")
end_line = canvas.create_rectangle(250, 300, 405, 340, fill="white")
end_text = canvas.create_text(320, 320, text="END LINE", font=("Arial", 20), fill="black")

restart_button = tk.Button(canvas, text="Restart", command=restart_game)
restart_button_window = canvas.create_window(50, 400, anchor="center", window=restart_button)

btn_browse1 = tk.Button(window, text="Move", command=browse_file)
btn_browse1.pack()

# start the main loop
window.mainloop()
