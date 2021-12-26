import socket
import time
import pygame
import RPi.GPIO as GPIO
from flask import Flask, render_template
import datetime
HOST = '10.0.1.10'

PORT1 = 41000
PORT2 = 43000
PORT3 = 45000

LED = 16

a=0#position check
i=0#led count
count=0 #sound play counting
sensor1 = 17
sensor2 = 27
sensor3 = 22
reply22=0
##################################update str1
str1 = ''
##################################
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/Desktop/sound.wav')

server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Socket Created')
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)
GPIO.output(LED,True)
server_socket1.bind((HOST, PORT1))
server_socket2.bind((HOST, PORT2))
server_socket3.bind((HOST, PORT3))

server_socket1.listen(1)
print('Socket1 Waiting accept')
server_socket2.listen(1)
print('Socket2 Waiting accept')
server_socket3.listen(1)
print('Socket3 Waiting accept')


connect_socket1, addr1 = server_socket1.accept()
print('Connected by', addr1)
connect_socket2, addr2 = server_socket2.accept()
print('Connected by', addr2)
connect_socket3, addr3 = server_socket3.accept()
print('Connected by', addr3)
def callback(channel):
    global a
    if channel == sensor1 and GPIO.input(sensor2) == False and GPIO.input(sensor3) == False:
        a=a|0b000100
        print('interrupt',bin(a))
    elif channel == sensor2 and GPIO.input(sensor1) == False and GPIO.input(sensor3) == False:
        a=a|0b000010
        print('interrupt',bin(a))
    elif channel == sensor3 and GPIO.input(sensor1) == False and GPIO.input(sensor2) == False:
        a=a|0b000001
        print('interrupt',bin(a))
    

GPIO.setup(sensor1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensor2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensor3,GPIO.IN,pull_up_down=GPIO.PUD_UP)


GPIO.add_event_detect(sensor1,GPIO.FALLING,callback=callback)
GPIO.add_event_detect(sensor2,GPIO.FALLING,callback=callback)
GPIO.add_event_detect(sensor3,GPIO.FALLING,callback=callback)
GPIO.output(LED,False)
app = Flask(__name__)

@app.route("/")

def main():
    global LED
    global a
    global i
    global count
    global sensor1
    global sensor2
    global sensor3
    global reply22
    ############################################update str1 global
    global str1
    ############################################
    reply1=0
    reply2=0
    reply3=0
    ##################################################################update sstr
    data={'aa1':'-','aa2':'-','aa3':'-','bb1':'-','bb2':'-','bb3':'-','cc1':'-','cc2':'-','cc3':'-','dd1':'-','dd2':'-','dd3':'-','sstr':'','aaa':0,'bbb':0,'ccc':0,'ddd':0}
    ##################################################################
    ###move detect START###
    #if move detected i increse, LED blinking begin
    if i==0 and (GPIO.input(sensor1) == True or GPIO.input(sensor2) == True or GPIO.input(sensor3) == True):
        i = 1
    if GPIO.input(sensor1) == True:
        a=a|0b100000
    if GPIO.input(sensor2) == True:
        a=a|0b010000
    if GPIO.input(sensor3) == True:
        a=a|0b001000
    ###move detect END###
    
    ###final move + movedetect START###
    if a >0 :
        reply1 = 1
        if (a&0b000100)>0:
            data.update(aaa=1)

            #########################################################################update
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 거실 좌측에서 마지막 위치 감지됨 -'+time1 + str1
            print('a left')
            ###########################################################################

        elif (a&0b000010)>0:
            data.update(aaa=2)

            ###########################################################################
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 거실 중간에서 마지막 위치 감지됨 -'+time1 + str1
            print('a middle')
            ###########################################################################

        elif (a&0b000001)>0:
            data.update(aaa=3)

            ###########################################################################
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 거실 우측에서 마지막 위치 감지됨 -'+time1 + str1
            print('a right')
            ###########################################################################

        if (a&0b100000)>0:
            data.update(aa1='O')
        if (a&0b010000)>0 :
            data.update(aa2='O')
        if(a&0b001000)>0:
            data.update(aa3='O')
        a=0
            
    else :
        reply1 = 0
        
    ##final move + movedetect END###
            
            
    ###LED BLINK START###        
    if i >0 and i < 2:
        GPIO.output(LED,True)
        i=i+1
    elif i>=2 and i <3:
        GPIO.output(LED,False)
        i=i+1
    elif i>=3 and i < 4:
        GPIO.output(LED,True)
        i=i+1
    elif i >=4 and i < 5:
        GPIO.output(LED,False)
        i=i+1
    elif i>=5 and i <6:
        GPIO.output(LED,True)
        i=i+1
    elif i>=6 and i < 7:
        GPIO.output(LED,False)
        i=i+1
    elif i>=7 and i <8:
        GPIO.output(LED,True)
        i=i+1
    elif i>=8 and i < 9:
        GPIO.output(LED,False)
        i=i+1
    elif i>=9 and i <10:
        GPIO.output(LED,True)
        i=i+1
    elif i>=10 and i < 11:
        GPIO.output(LED,False)
        i=i+1
    elif i>=11 and i <12:
        GPIO.output(LED,True)
        i=i+1
    elif i>=12 and i < 13:
        GPIO.output(LED,False)
        i=i+1
    elif i>=13:
        i=0
    ####LED BLINK #######
        
    ###socket START###
    #1 -> 3 -> 4 -> 2 -> 1
    a1 = connect_socket1.recv(1024)
    a1 = a1.decode('utf-8')
    a1 = int(a1)
    if a1 >0:
        print('b - ',bin(a1))
        reply3 = 1
        if (a1&0b000100)>0 :
            data.update(bbb=1)

            ###########################################################################
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 주방 좌측에서 마지막 위치 감지됨 -'+time1 + str1
            print('b left')
            ###########################################################################
            
        elif(a1&0b000010)>0:
            data.update(bbb=2)

            ###########################################################################
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 주방 중간에서 마지막 위치 감지됨 -'+time1 + str1
            print('b middle')
            ###########################################################################

        elif (a1&0b000001)>0:
            data.update(bbb=3)

            ###########################################################################
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 주방 우측에서 마지막 위치 감지됨 -'+time1 + str1
            print('b right')
            ###########################################################################

        if (a1&0b100000)>0:
            data.update(bb1='O')
        if (a1&0b010000)>0 :
            data.update(bb2='O')
        if(a1&0b001000)>0:
            data.update(bb3='O')
          
    else :
        reply3 = 0
        
    reply1 = str(reply1).encode('utf-8')
    connect_socket1.send(reply1)
    reply1 = 0
    
    
    ###play music
    a2 = connect_socket2.recv(1024)
    a2 = a2.decode('utf-8')
    a2 = int(a2)
    if a2 > 0 :
        print('c - ',bin(a2))
        if count < 1:
            count = 1
            pygame.mixer.music.play()
        
        if (a2&0b000100)>0 :
            data.update(ccc=1)

            ###########################################################################
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 현관 좌측에서 마지막 위치 감지됨 -'+time1 + str1
            print('c left')
            ###########################################################################

        elif(a2&0b000010)>0 :
            data.update(ccc=2)

            ###########################################################################
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 현관 중간에서 마지막 위치 감지됨 -'+time1 + str1
            print('c middle')
            ###########################################################################

        elif (a2&0b000001)>0 :
            data.update(ccc=3)

            ###########################################################################
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 현관 우측에서 마지막 위치 감지됨 -'+time1 + str1
            print('c right')
            ###########################################################################

        if (a2&0b100000)>0:
            data.update(cc1='O')
        if (a2&0b010000)>0 :
            data.update(cc2='O')
        if(a2&0b001000)>0:
            data.update(cc3='O')
  
     
    if count > 0 and count < 81:
        count = count + 1
    elif count > 40:
        count = 0
    if reply22 == 1:
        reply2 = 1
        reply22=0
    reply2 = str(reply2).encode('utf-8')
    connect_socket2.send(reply2)
    reply2 = 0
    
    a3 = connect_socket3.recv(1024)
    a3 = a3.decode('utf-8')
    a3 = int(a3)
    if a3 >0:
        print('d - ',bin(a3))
        reply22 = 1
        if (a3&0b000100)>0 :
            data.update(ddd=1)

            ###########################################################################
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 안방 좌측에서 마지막 위치 감지됨 -'+time1 + str1
            print('d left')
            ###########################################################################

        elif(a3&0b000010)>0 :
            data.update(ddd=2)

            ###########################################################################
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 안방 중간에서 마지막 위치 감지됨 -'+time1 + str1
            print('d middle')
            ###########################################################################

        elif (a3&0b000001)>0 :
            data.update(ddd=3)

            ###########################################################################
            localtime = datetime.datetime.now()
            time1 = localtime.strftime("%H:%M")
            str1 = ' 안방 우측에서 마지막 위치 감지됨 -'+time1 + str1
            print('d right')
            ###########################################################################

        if (a3&0b100000)>0:
            data.update(dd1='O')
        if (a3&0b010000)>0 :
            data.update(dd2='O')
        if(a3&0b001000)>0:
            data.update(dd3='O')
          
    else :
        reply2 = 0
        reply22=0
        
    reply3 = str(reply3).encode('utf-8')
    connect_socket3.send(reply3)
    reply3 = 0

    #############################################################################
    if str1.count('-') > 50:
      str1 = str1[0:4000]

      #########################################################################
    data.update(sstr=str1)
    
    return render_template('Index1-3.html',**data)


if __name__ == "__main__":
        app.run(host='10.0.1.10',port=8080)


###socket END###


connect_socket1.close()
server_socket1.close()
connect_socket2.close()
server_socket2.close()
connect_socket3.close()
server_socket3.close()

GPIO.cleanup()



