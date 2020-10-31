import pyautogui
import win32api
import keyboard
import time
from config import INTERVAL, SCALE, WAIT, START, STOP, FSTOP


recorder = []


def click() -> bool:
    return not win32api.GetKeyState(0x01) in [0, 1]


def _force_stop() -> None:
    if keyboard.is_pressed(FSTOP):
        print(f"PROCESS FORCEFULLY STOPPED (ON KEY PRESS: '{FSTOP}')")
        exit()


def recpen() -> None:
    print(f"Press '{START}' to start recording and '{STOP}' to end recording.")
    while True:  # Await starting command
        _force_stop()
        if keyboard.is_pressed(START):
            break

    print("Recording...")
    s = time.time()
    while True:  # Recording mouse activity
        _force_stop()
        if keyboard.is_pressed(STOP):
            break
        else:
            x, y = pyautogui.position()
            clicked = click()
            recorder.append(((x, y), clicked))

        time.sleep(INTERVAL)
    e = time.time()
    print(f"Recorded {len(recorder)} activities in {e - s:.2f} seconds.")

    print(f"Press '{START}' and wait {WAIT:.2f} seconds to start replaying.")
    while True:  # Await starting command
        _force_stop()
        if keyboard.is_pressed(START):
            print(f"Awaiting {WAIT:.2f} seconds to replaying...")
            time.sleep(WAIT)
            break

    print(f"Replaying recorded activities ({len(recorder)}).")
    s = time.time()
    x, y = pyautogui.position()  # Relative mouse position for replaying and to prevent downscaling rounding errors
    for i in range(len(recorder)-1):
        _force_stop()
        a1 = recorder[i]
        a2 = recorder[i+1]

        pos1, c1 = a1
        pos2, c2 = a2
        x1, y1 = pos1
        x2, y2 = pos2

        x += (x2-x1) * SCALE
        y += (y2-y1) * SCALE

        if c1 and c2:
            pyautogui.dragTo(round(x), round(y), button='left', _pause=False)
        else:
            if c1 and not c2:
                pyautogui.click(_pause=False)
            pyautogui.moveTo(round(x), round(y), _pause=False)

        time.sleep(INTERVAL)

    e = time.time()

    print(f"Replaying complete in {e - s:.2f} seconds.")


recpen()
#
