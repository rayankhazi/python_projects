import pyttsx3            #speech from system
import datetime 
import speech_recognition as sr
import pyaudio
import wikipedia
import smtplib       #email sending
import webbrowser as wb
import psutil       #cpu information and battery status
import pyjokes      #jokes
import os          #opening system apps
import pyautogui   #for screenshot
import random
import json       #for news report
import requests   #for news report
from urllib.request import urlopen     #to open news urls
import wolframalpha         #calculator functions
import time


engine= pyttsx3.init()
wolframalpha_app_id = 'X8Q943-ERXGA6YXAY'


def  speak(audio):
    engine.say(audio)
    engine.runAndWait()
    

def time_fun():
    T=datetime.datetime.now().strftime("%I:%M:%S")
    speak("the current time is ")
    speak(T)
    
    
def date_fun():
    Y=datetime.datetime.now().year
    M=datetime.datetime.now().month
    D=datetime.datetime.now().day
    speak("the current year is")
    speak(Y)
    speak("the current month is")
    speak(M)
    speak("the current day is")
    speak(D)
    
def wishme() :

    speak("welcome back chief")
    
   
    
    hour = datetime.datetime.now().hour
    
    if hour>=6 and hour<12 :
        speak ("good morning Chief!")
    
    elif hour>=12 and hour<18 :
    
        speak("good afternoon Chief!")
        
    elif hour>=18 and hour<24:
    
        speak("good evening Chief!")
    
    else:
        speak("good night Chief")
    
    speak("Jarvis at your service. How can I help you Chief?")
    
def TakeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening......")
        r.pause_threshhold = 0.8
        audio = r.listen(source)
        
        
    try:
        print("recognising.......")
        query=r.recognize_google(audio,language="en-US")
        print(query)
    
    except Exception as e:
        print(e)
        print("say again please......")
        return "None"
    return query

def sendEmail(to,content):
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    
    server.login('username@gmail.com', 'password')
    server.sendmail('username@gmail.com', to, content)
    server.close()

def cpu() :
    usage = str(psutil.cpu_percent())
    speak("CPU is at"+usage)
    
    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(battery.percent)
    
def joke() :
    speak(pyjokes.get_joke())
    
def screenshot() :
    img = pyautogui.screenshot()
    img.save('C:/imagesfromjarvis/screenshot.png')

if __name__=="__main__":
    
    wishme()
    while True:
        query=TakeCommand().lower()
        
        if 'time'in query:
            time_fun()
        elif 'date' in query:
            date_fun()
        elif 'wikipedia' in query:
            speak("searching......")
            query=query.replace('wikipedia','')
            result = wikipedia.summary(query,sentences=3)
            speak("according to wikipedia")
            print(result)
            speak(result)
        elif 'send email' in query :
            try :
                speak("what should i say ?")
                content = TakeCommand()
                
                speak("who is the receiver ?")
                
                receiver = input("enter receiver's email id")
                to = receiver
                sendEmail(to, content)
                speak(content)
                speak("email has been sent")
            except Exception as e:
                print(e)
                speak("unable to send email")


        elif 'search in chrome' in query :
            speak("what should i  search?")
            chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            
            
            search = TakeCommand().lower()
            wb.get(chromepath).open_new_tab(search+'.com')
            
        elif 'search youtube' in query :
            speak("what should i search?")
            search_term = TakeCommand().lower()
            speak("here we go to YOUTUBE!")
            wb.open("https://www.youtube.com/results?search_query="+search_term)
            
        elif 'search google' in query :
            speak("what should i search?")
            search_term = TakeCommand().lower()
            speak("searching.....")
            wb.open('https://www.google.com/search?q='+search_term)
            
        
        elif 'cpu' in query :
            cpu()
            
        elif 'joke' in query :
            joke()
            
        elif 'thank you' in query :
            speak("Thank You ! going offline SIR!")
            quit()
            
        #elif 'word' in query :
            #speak("opening ms word!")
            #ms_word = r'E:/Office/Office16/WINWORD.EXE'
            #os.startfile(ms_word)
            
            
        elif 'write a note' in query :
            speak("what should i write sir?")
            notes = TakeCommand()
            file = open('notes.txt','w')
            speak("Sir should i include date and time?")
            ans = TakeCommand()
            if 'yes' in ans or 'sure' in ans :
                strftime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strftime)
                file.write(':-')
                file.write(notes)
                speak("done taking notes, SIR")
            else :
                file.write(notes)
                speak("done taking notes, SIR")
                
        elif 'show notes' in query :
            speak("showing notes sir")
            file = open('notes.txt','r')
            print(file.read())
            speak(file.read())
            
        elif 'screenshot' in query :
            screenshot()
            
        elif 'play music' in query:
            songs_dir='C:/Users/user/Music'
            music=os.listdir(songs_dir)
            speak('what should I play?')
            speak('select a number......')
            ans=TakeCommand().lower()
            while('number' not in ans and ans != 'random' and ans != 'you choose') :
                speak('i could not understand you. Please try again.')
                ans = TakeCommand().lower()
                
            if 'number'in ans:
                no=int(ans.replace('number', ''))  
                
            elif 'random' or 'you choose' in ans:
                no = random.randint(1,15)
            
            os.startfile(os.path.join(songs_dir,music[no]))
            
            
        elif 'remember that' in query :
            speak("what should i remember?")
            memory = TakeCommand()
            speak("you asked to remember that.."+memory)
            remember = open('memory.txt','w')
            remember.write(memory)
            remember.close()
            
        elif 'do you remember anything' in query :
            remember = open('memory.txt','r')
            speak('you asked me to remember that'+memory)
            
        elif 'news' in query :
            try :
                jsonobj = urlopen('http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=4552266c9c204f7391fe0cbbe321c40a')
                data = json.load(jsonobj)
                i = 1
                
                speak("here are some headlines from entertainment industry")
                print("################### TOP HEADLINES ####################"+'\n')
                for item in data['articles'] :
                    print(str(i)+". "+item['title']+'\n')
                    print(item['description']+'\n')
                    speak(item['title'])
                    i += 1
                    
            except Exception as e :
                print(str(e))
                
        elif 'where is' in query :
            query = query.replace('where is','')
            location = query
            speak("user asked to locate.."+location)
            wb.open_new_tab("https://www.google.com/maps/place/"+location)
            
        elif 'calculate' in query :
            client = wolframalpha.Client(wolframalpha_app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx +1:]
            res = client.query(''.join(query))
            answer = next(res.results).text
            print('the answer is '+answer)
            speak('the answer is '+answer)
            
        elif 'what is' in query or 'who is' in query :
            #same api key as for wolframalpha
            client = wolframalpha.Client(wolframalpha_app_id)
            res = client.query(query)
            
            
            try :
                print(next(res.results).text)
                speak(next(res.results).text)
                
            except StopIteration :
                print("No Results")
                
        elif 'stop listening'in query :
                speak("for how many seconds you want me to stop listening to your commands")
                ans = int(TakeCommand())
                time.sleep(ans)
                print(ans)
                
        
        #elif 'log out' in query :
            #os.system('shutdown -l')
            
        #elif 'restart' in query :
            #os.system('shutdown /r /t 1')
            
        #elif 'shutdown' in query :
            #os.system('shutdown /s /t 1')
            
            
            
            
        
        
                    
                
        
        
        
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            