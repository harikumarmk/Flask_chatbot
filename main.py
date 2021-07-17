from flask import Flask,render_template,request
import datetime
import pandas as pd
import collections

app=Flask(__name__,template_folder="templates")

class Chatbot:
    def __init__(self):
        wish="Good Morning,"
        if (datetime.datetime.now().hour>=12 and datetime.datetime.now().hour<16):
            wish="Good Afternoon, "
        if (datetime.datetime.now().hour>=16 and datetime.datetime.now().hour<=23):
            wish="Good Evening, "

        welcomeFile=open("src/welcome.txt")
        self.WelcomeText=(wish+welcomeFile.read())

        ConclusionFile=open("src/conclusion.txt")
        self.ConclusionText=(ConclusionFile.read())

        self.dict=collections.defaultdict(lambda : "False")
        self.dict["hi"]="hello"
        self.read_chat_csv=pd.read_csv('src/chat.csv')
        self.read_chat_csv_key=list(self.read_chat_csv['Key'])
        self.read_chat_csv_msg=list(self.read_chat_csv['Message'])
        for i in range(len(self.read_chat_csv_key)):
            self.dict[self.read_chat_csv_key[i].lower()]=self.read_chat_csv_msg[i]

    def welcome(self):
        return self.WelcomeText

    def search(self,key):
        found=0
        Msg=key.split(' ')
        for i in Msg:
            i=i.lower()
            print(i)
            if(i=="bye"):
                return (self.ConclusionText)
                found=1
                break
            if(self.dict[i]!="False"):
                return (self.dict[i]) 
                found=1
                break   
        if (found==0):
            return ("Can't get it try another one.")

Chathistory =list()
chatBot_start=Chatbot()
@app.route('/')
def index():
    Chathistory.clear()
    Msg=chatBot_start.welcome()
    Chathistory.append(Msg)
    return render_template('chatbot.html',msgs=Msg,len=0)

@app.route('/',methods= ['POST','GET'])
def chat():
    msg=request.form['Message']
    Chathistory.append(msg)
    message=chatBot_start.search(msg)
    Chathistory.append(message)
    return render_template("chatbot.html",msg=Chathistory,len=len(Chathistory))


if __name__ == '__main__' :
    app.run(debug=True)