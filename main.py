import cv2
import time
import datetime
import smtplib
import ssl
from customtkinter import *
import tkinter as tk
import os
import email.mime.multipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email import encoders
from email.mime.text import MIMEText
# import MIMEMultipart
# from email.MIMEText import MIMEText

win = tk.Tk()
app = CTk()
app.geometry("500x400")

directory_path = 'C:\\Users\\PranatiSahithi\\PycharmProjects\\pythonProject10'
most_recent_time = 0
most_recent_file = None

msg = MIMEMultipart()

for entry in os.scandir(directory_path):
    if entry.is_file():
        mod_time = entry.stat().st_mtime_ns
        if mod_time > most_recent_time:
            most_recent_file = entry.name
            most_recent_time = mod_time

#msg = EmailMessage()
msg["subject"] = "Intruder Alert!"

msg["From"] = "namanavaishnavi@gmail.com"
msg["To"] = "sp.gavara@gmail.com"
#msg.set_context("done")

email = "namanavaishnavi@gmail.com"
app_password = "gsez wlmr vcbh phga"

def onclick():
    msg["To"] = "tippalalavanya05@gmail.com"
    text = MIMEText("PLEASE CHECK ON THE HOUSE")
    msg.attach(text)

    context1 = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context1) as server:
        server.login(email, app_password)
        server.send_message(msg)

def onclick2():
    exit(0)

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("video.mp4", fourcc, 20, frame_size)

while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)
            print("Started recording!")
            x = cv2.VideoCapture()

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(email, app_password)
                server.send_message(msg)
                # x = cv2.VideoCapture()
                #  cv2.imwrite("C:\\Users\\PranatiSahithi\\PycharmProjects\\pythonProject10", x)
                attachment = open(f"{current_time}.mp4", "rb")
                #attachment = open("C:\\Users\\PranatiSahithi\\PycharmProjects\\pythonProject10\\pic.png", "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                #p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
                # server.starttls()
                text = msg.as_string()
                server.sendmail(msg['From'], msg['To'], text)
                del msg['To']
                #print(most_recent_file)
                '''
                with open(most_recent_file, 'r') as f:
                    contents = f.read()
                    filename = contents
                    x = cv2.VideoCapture()
                    attachment = open(x, "rb")
                    p = MIMEBase('application', 'octet-stream')
                    p.set_payload((attachment).read())
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                    msg.attach(p)
                    server.starttls()
                    text = msg.as_string()
                    server.sendmail(msg['From'], msg['To'], text)
                    '''
                    # msg.attach(MIMEText(body, 'plain'))

                #win.geometry("200x100")
                app.geometry("500x400")
                btn = CTkButton(master=app, text="Alert", command=onclick, corner_radius=32, fg_color="#C850C0", hover_color="#4158D0",)
                btn2 = CTkButton(master=app, text="Ignore", command=onclick2, corner_radius=32, fg_color="#C850C0",
                                hover_color="#4158D0", )
                btn.place(relx=0.5, rely=0.5, anchor='center')
                btn2.place(relx=0.5, rely=0.2, anchor='center')

                app.mainloop()
                '''
                b = tk.Button(
                    win,
                    text='click here',
                    command=onclick
                )
                b.pack()
                win.mainloop()
                '''
                # msg.attach(MIMEText('<html><body><h1>Hello</h1>' + '<p><img src = "cid:0"></p>' + '</body></html>', 'html', 'utf-8'))
            '''
            connection = smtplib.SMTP("smtp.gmail.com", 587)
            connection.starttls()
            connection.login(user=myemail, password=mypassword)

            connection.sendmail(from_addr=myemail, to_addrs="sp.gavara@gmail.com", msg="intruder alert")
            connection.close()
            '''
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print("STOP RECORDING!")


        time_started = True
        detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    for(x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height),(255, 0, 0), 3)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()