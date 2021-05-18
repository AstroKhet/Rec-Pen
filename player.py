import time
import json
import pyautogui

name = input('Recording name (without extension): ')

with open(f"save/{name}.json", 'r') as recorder_data:
    data = json.load(recorder_data)

    INTERVAL = data['int']
    SCALE = data['scale']
    recorder = data['run']

print("Beginning replay in 3.00 seconds.")
time.sleep(3)

s = time.time()
x, y = pyautogui.position()  # Relative mouse position for replaying and to prevent downscaling rounding errors
for i in range(len(recorder) - 1):
    a1 = recorder[i]
    a2 = recorder[i + 1]

    pos1, c1 = a1
    pos2, c2 = a2
    x1, y1 = pos1
    x2, y2 = pos2

    x += (x2 - x1) * SCALE
    y += (y2 - y1) * SCALE

    if c1 and c2:
        pyautogui.dragTo(round(x), round(y), button='left', _pause=False)
    else:
        if c1 and not c2:
            pyautogui.click(_pause=False)
        pyautogui.moveTo(round(x), round(y), _pause=False)

    time.sleep(INTERVAL)

e = time.time()

print(f"Replaying complete in {e - s:.2f} seconds.")

print("Save recording? (y/n)")
save = input("")
