import tkinter as tk
import random
from tkinter.font import Font
import json
from urllib.request import urlopen
import threading
import requests
import speech_recognition as sr  # SpeechRecognition package to understand the speech
import pyttsx3  # To speak the text
import pywhatkit  # pywhatkit allows us to do searching in youtube and other fun
import datetime  # To use date and time
import wikipedia  # To use for searching online
import pyjokes  # To use jokes by in the program
import webbrowser
import geocoder
import pyautogui
from bs4 import BeautifulSoup
from plyer import notification
import os
import pyglet
import time
import re

import alarmset
import long_responses as ls
import make_request
import mathutils
import there_exists as te

listener = sr.Recognizer()  # create a recognizer which will understand the voice
engine = pyttsx3.init()  # Python text to speech initialize
voices = engine.getProperty('voices')  # Get all the voices
engine.setProperty('voice', voices[1].id)  # set it to second voice


def WhatsAppMessagesendtoNumber():
    speak("Please tell me the mobile number whom do you want to send message.")
    mobile_number = None
    while (True):
        mobile_number = get_command().replace(' ', '')
        if mobile_number[0] == '0':
            mobile_number = mobile_number[1:]
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            speak("Please say it again")
        else:
            break
    mobile_number.replace(' ', '')
    speak("Tell me your message......")
    message = get_command()
    speak("Opening whatsapp web to send your message.")
    speak("Please be patient, sometimes it takes time.\nOR In some cases it does not works.")
    while (True):
        try:
            pywhatkit.sendwhatmsg("+88" + mobile_number, message, datetime.datetime.now().hour,
                                  datetime.datetime.now().minute + 1)
            break
        except Exception:
            pass
    time.sleep(20)
    speak('Message sent succesfully.')


def find_whatsapp_number(name):
    name = name.lower()
    arr = {'miraj': "+8801797482479", 'purny': "+880184877950", 'sabab': "+8801848344806"}
    number = 'null'
    for x in arr.keys():
        if x == name:
            number = arr[x]
            break
    return number


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])
    response('sorry about that!', ['no', 'nop', 'dont know', 'not interested', 'sorry'], single_response=True)
    response(ls.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(ls.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return ls.unknown() if highest_prob_list[best_match] < 1 else best_match


def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


def speak(text):
    saratelling(str(text))
    engine.say(text)
    engine.runAndWait()


def get_command():
    command = ''
    try:
        with sr.Microphone() as source:  # Use microphone
            print('Listening...')
            # listener.adjust_for_ambient_noise(source, duration=0.3)
            voice = listener.listen(source)  # lister to listen to the source and store as voice
            command = listener.recognize_google(voice)  # Converting the voice to text using google api
            command = command.lower()  # convert to lower case
            metelling(command)

            if 'sara' in command:  # check if name 'alexa' is in command
                command = command.replace('sara', '')  # Remove 'alexa' from command by replacing it with empty string
                print(command)


    except:
        pass

    return command  # return command that we are saying


def run_sara(command):
    if te.there_exists(['play on youtube', 'on youtube'], command):
        song = command.replace('play', '')  # remove play from the command
        song = command.replace('on youtube', '')
        speak('playing' + song)
        pywhatkit.playonyt(song)  # play it in youtube

    elif 'time' in command:  # To get the time
        time = datetime.datetime.now().strftime(
            '%I:%M %p')  # %H:%M for 24 hr format # Get the hours and mins from datetime and format it
        speak('Current time is ' + time)
        print(time)

    elif 'who is' in command:  # To use word wikipedia in command
        person = command.replace('who the hell is', '')  # replace who is with empty str in command
        try:
            info = wikipedia.summary(person, 1)  # search person and mention how many lines we want
            speak(info)  # speak the information
            print(info)

        except:
            speak('Couldn\'t find ' + person)

    elif 'drink' in command:
        speak('sorry, I have a headache ')

    elif 'are you single' in command:
        speak('I am in a relationship with wifi ')

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)
        print(joke)

    elif 'what is your name' in command:
        speak('My name is Sara')
    elif 'thanks' in command:
        speak('you are welcome')
    elif 'how are you' in command:
        speak('I am fine. what about you?')

    elif "location" in command:

        g = geocoder.ip('me')
        print(g.latlng)

    elif "sum of" in command:
        twonumber = command.replace('sum of', '')
        twonumber = twonumber.split("and")
        sumtwo = mathutils._sum(twonumber)
        speak(sumtwo)
        print(sumtwo)
    elif "subtract" in command:
        twonumber = command.replace('subtract', '')
        twonumber = twonumber.split("and")
        sum = mathutils.subtract(int(twonumber[0]), int(twonumber[1]))
        speak(str(sum))
        print(twonumber)

    elif "multiply" in command:
        twonumber = command.replace('multiply', '')
        twonumber = twonumber.split("and")
        sum = 1;
        for i in twonumber:
            sum = mathutils.multiply(sum, int(i))

        speak(str(sum))
        print(sum)

    elif "divide" in command:
        twonumber = command.replace('divide', '')
        twonumber = twonumber.split("and")
        sum = mathutils.divide(int(twonumber[0]), int(twonumber[1]));
        speak(str(sum))
        print(sum)

    elif 'screenshot' in command:
        image = pyautogui.screenshot()
        time = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        image.save(time + '.png')
        speak('Screenshot taken. And the file name is ' + time + '.png')

    # opening software applications
    elif te.there_exists(['open chrome', 'open google chrome'], command):
        speak("Opening chrome")
        os.startfile(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs/Google Chrome')

    elif te.there_exists(['open notepad plus plus', 'open notepad++', 'open notepad ++'], command):
        speak('Opening notepad++')
        os.startfile(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Notepad')

    elif te.there_exists(['open notepad', 'start notepad'], command):
        speak('Opening notepad')
        os.startfile(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Notepad')

    elif te.there_exists(
            ['open ms paint', 'open mspaint', 'open microsoft paint', 'start microsoft paint', 'start ms paint'],
            command):
        speak("Opening Microsoft paint....")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Paint')

    elif te.there_exists(['show me performance of my system', 'open performance monitor', 'performance monitor',
                          'performance of my computer', 'performance of this computer'], command):
        os.startfile(
            "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Administrative Tools\Performance Monitor")

    elif te.there_exists(['open snipping tool', 'snipping tool', 'start snipping tool'], command):
        speak("Opening snipping tool....")
        os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Snipping Tool")

    elif te.there_exists(['open code', 'open visual studio ', 'open vs code'], command):
        speak("Opeining vs code")
        codepath = r"C:\Users\Admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code"
        os.startfile(codepath)

    elif te.there_exists(['open file manager', 'file manager', 'open my computer', 'my computer', 'open file explorer',
                          'file explorer', 'open this pc', 'this pc'], command):
        speak("Opening File Explorer")
        os.startfile("C:")

    elif te.there_exists(['powershell'], command):
        speak("Opening powershell")
        os.startfile(
            r'C:\Users\Admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Windows PowerShell/Windows PowerShell')

    elif te.there_exists(['cmd', 'command prompt', 'command prom', 'commandpromt', ], command):
        speak("Opening command prompt")
        os.startfile(r'C:\Windows\System32\cmd.exe')

    elif te.there_exists(['open whatsapp'], command):
        speak("Opening whatsApp")
        os.startfile(
            r'C:\Users\Raihan Miraj\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\WhatsApp\WhatsApp')

    elif te.there_exists(
            ['open settings', 'open control panel', 'open this computer setting Window', 'open computer setting Window',
             'open computer settings', 'open setting', 'show me settings', 'open my computer settings'], command):
        speak("Opening settings...")
        os.startfile('C:\Windows\System32\control.exe')

    elif te.there_exists(['open your setting', 'open your settings', 'open settiing window', 'show me setting window',
                          'open voice assistant settings'], command):
        speak("Opening my Setting window..")


    elif te.there_exists(['open vlc', 'vlc media player', 'vlc player'], command):
        speak("Opening VLC media player")
        os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\VideoLAN\vlc")
    elif te.there_exists(
            ['send message on whatsapp to a number', 'send message to a number'],
            command):
        WhatsAppMessagesendtoNumber()
    elif te.there_exists(
            ['message whatspp', 'send a message', 'send message on whatsapp', 'send a message on whatsapp'],
            command):
        while (1):
            speak("whom do you want to send a message")
            nameofuser = get_command()
            print(nameofuser)
            if (find_whatsapp_number(nameofuser) != 'null'):
                numberofperson = find_whatsapp_number(nameofuser)
                break

        speak("tell me the message")
        message = get_command()
        hour = int(datetime.datetime.now().strftime(
            '%H'))
        minute = int(datetime.datetime.now().strftime(
            '%M')) + 2
        if (minute > 59):
            minute = 0
            hour += 1

        pywhatkit.sendwhatmsg(numberofperson, message, hour, minute)


    elif te.there_exists(['alarm', 'set alarm', 'alarm set', 'set an alarm'], command):
        c = 0
        hour = 0
        minute = 0
        second = 0
        while (1):
            if c == 0:
                speak("Tell me hour")
                hour = get_command()
                print(hour)
                if hour.isnumeric():
                    c += 1
            elif c == 1:
                speak("Tell me minute")
                minute = get_command()
                print(minute)
                if minute.isnumeric():
                    c += 1
            elif c == 2:
                speak("Tell me second")
                second = get_command()
                print(second)
                if second.isnumeric():
                    c += 1
                    break

        hours = str(hour) if (int(hour) > 10) else '0' + str(hour)
        minutes = str(minute) if (int(minute) > 10) else '0' + str(minute)
        seconds = str(second) if (int(second) > 10) else '0' + str(second)
        set_alarm_timer = hours + ':' + minutes + ':' + seconds

        alarmset.alarm(set_alarm_timer)

    elif 'covid news' in command:
        html_data = make_request.make_request('https://www.worldometers.info/coronavirus/')
        # print(html_data)
        soup = BeautifulSoup(html_data, 'html.parser')
        total_global_row = soup.find_all('tr', {'class': 'total_row'})[-1]
        total_cases = total_global_row.find_all('td')[2].get_text()
        new_cases = total_global_row.find_all('td')[3].get_text()
        total_recovered = total_global_row.find_all('td')[6].get_text()
        print('total cases : ', total_cases)
        print('new cases', new_cases[1:])
        print('total recovered', total_recovered)
        notification_message = f" Total cases : {total_cases}\n New cases : {new_cases[1:]}\n Total Recovered : {total_recovered}\n"
        notification.notify(
            title="COVID-19 Statistics",
            message=notification_message,
            timeout=5
        )
        speak('total cases : ' + total_cases)
        speak('new cases ' + new_cases[1:])
        speak('total recovered' + total_recovered)

    elif 'sport news' in command:
        jsonObj = urlopen(
            'https://apiv3.apifootball.com/?action=get_events&match_live=1&APIkey=85a6560f2a056eca59562d815bd935f30bfb31b182ac11190ca2534eaa769dfa')
        data = json.load(jsonObj)
        speak('here is the sport news')
        for item in data:
            speak('country ' + item['country_name'] + ' league ' + item['league_name'] + ' match will run between ' +
                  item['match_hometeam_name'] + ' and ' + item['match_awayteam_name'])
            print('country ' + item['country_name'] + ' league ' + item['league_name'] + ' match will run between ' +
                  item['match_hometeam_name'] + ' and ' + item['match_awayteam_name'])
    elif "weather" in command:
        api_key = "5b3f3248556f11ae2c810fa19130037e"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        speak("what is the city name")
        city_name = get_command()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        print(response)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            speak(" Temperature in kelvin unit is " +
                  str(current_temperature) +
                  "\n humidity in percentage is " +
                  str(current_humidiy) +
                  "\n description  " +
                  str(weather_description))
            print(" Temperature in kelvin unit = " +
                  str(current_temperature) +
                  "\n humidity (in percentage) = " +
                  str(current_humidiy) +
                  "\n description = " +
                  str(weather_description))



    elif 'news' in command:

        try:
            jsonObj = urlopen(
                'https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=04dbcc0f6b404030ba70cda8d9c3aff6')
            data = json.load(jsonObj)
            i = 1

            speak('here are some top news from the times of india')
            for item in data['articles']:
                print(str(i) + '. ' + item['title'] + '\n')
                print(item['description'] + '\n')
                speak(str(i) + '. ' + item['title'] + '\n')
                i += 1
        except Exception as e:

            print(str(e))



    elif 'write' in command:
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.3)
                audio = recognizer.listen(mic)

                text = recognizer.recognize_google(audio)
                text.lower()

                print('Recognized as: ')
                print(text)

        except sr.UnknownValueError():
            command = get_command()
            run_sara(command)

    elif 'open youtube' in command:
        webbrowser.open_new_tab("https://www.youtube.com")
        speak("youtube is open now")


    elif 'open google' in command:
        webbrowser.open_new_tab("https://www.google.com")
        speak("Google is open now")


    elif 'open gmail' in command:
        webbrowser.open_new_tab("gmail.com")
        speak("Google Mail open now")

    else:  # Default
        noway = get_response(command)
        speak(noway)
        print(noway)

        # speak("Please say it again")


def exitwindow():
    root.destroy()
    root.quit()
    os.exit()


def metelling(data):
    global text2
    text = "ME : " + data + "\n"
    text2.insert('1.0', text, 'color')


def saratelling(data):
    global text2
    text = "Sara : " + data + "\n"
    text2.insert('1.0', text, 'color')


def startSaraclick():
    speak('Hi, I am sara , How can I help you? ')
    while True:
        try:
            command = get_command()
            if 'bye' in command:
                root.destroy()
                root.quit()
                break
                exit()
            else:
                run_sara(command)  # Run it continuously

        except sr.UnknownValueError():
            listener = sr.Recognizer()
            continue


def startSara():
    threading.Thread(target=startSaraclick).start()


root = tk.Tk()

text1 = tk.Text(root, height=20, width=30)
photo = tk.PhotoImage(file='./sara.png')
text1.insert(tk.END, '\n')
text1.image_create(tk.END, image=photo)

text1.pack(side=tk.LEFT)
global text2
text2 = tk.Text(root, height=20, width=50)
scroll = tk.Scrollbar(root, command=text2.yview)
text2.configure(yscrollcommand=scroll.set)
text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
text2.tag_configure('big', font=('Verdana', 20, 'bold'))
text2.tag_configure('color',
                    foreground='#476042',
                    font=('Tempus Sans ITC', 12, 'bold'))

text2.pack(side=tk.LEFT)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

button1 = tk.Button(root)
button1["bg"] = "#efefef"
ft = Font(family='Times', size=10)
button1["font"] = ft
button1["fg"] = "#000000"
button1["justify"] = "center"
button1["text"] = "Start"
button1.place(x=40, y=280, width=70, height=25)
button1["command"] = startSara

button2 = tk.Button(root)
button2["bg"] = "#efefef"
ft = Font(family='Times', size=10)
button2["font"] = ft
button2["fg"] = "#000000"
button2["justify"] = "center"
button2["text"] = "Exit"
button2.place(x=130, y=280, width=70, height=25)
button2["command"] = exitwindow

root.mainloop()
