import datetime  # To use date and time
import pyglet
import time



def alarm(set_alarm_timer):
    while True:
        time.sleep(1)
        current_time = datetime.datetime.now()
        now = current_time.strftime("%H:%M:%S")
        date = current_time.strftime("%d/%m/%Y")
        print("The Set Date is:", date)
        print(now)
        if now == set_alarm_timer:
            print("Time to Wake up")
            song = pyglet.media.load('sound.mp3')
            song.play()
            pyglet.app.event_loop.sleep(10)
            break