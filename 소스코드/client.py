import RPi.GPIO as GPIO
import time
import socket
import pygame
a=0
i=0
count=0 
reply = 0
LED = 16
time.sleep(10)
sensor1 = 17
sensor2 = 27
sensor3 = 22
GPIO.setmode(GPIO.BCM)
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/Desktop/sound.wav')
GPIO.setup(LED,GPIO.OUT)
GPIO.output(LED,True)

HOST = '10.0.1.10'
PORT = 45000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
GPIO.output(LED,False)
def callback(channel):
    global a
    if channel == sensor1 and GPIO.input(sensor2) == False and GPIO.input(sensor3) == False:
        a=a|0b000100
        print('interrupt',bin(a),'\t',a)
    elif channel == sensor2 and GPIO.input(sensor1) == False and GPIO.input(sensor3) == False:
        a=a|0b000010
        print('interrupt',bin(a),'\t',a)
    elif channel == sensor3 and GPIO.input(sensor1) == False and GPIO.input(sensor2) == False:
        a=a|0b000001
        print('interrupt',bin(a),'\t',a)
    


GPIO.setup(sensor1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensor2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensor3,GPIO.IN,pull_up_down=GPIO.PUD_UP)


GPIO.setup(LED,GPIO.OUT)

GPIO.add_event_detect(sensor1,GPIO.FALLING,callback=callback)
GPIO.add_event_detect(sensor2,GPIO.FALLING,callback=callback)
GPIO.add_event_detect(sensor3,GPIO.FALLING,callback=callback)
try:
    while True :
        if i==0 and (GPIO.input(sensor1) ==True or GPIO.input(sensor2) == True or GPIO.input(sensor3) == True):
            i = 1
        if GPIO.input(sensor1) == True:
            a=a|0b100000
        if GPIO.input(sensor2) == True:
            a=a|0b010000
        if GPIO.input(sensor3) == True:
            a=a|0b001000
        
        if a >0 :
            print('======')
            if (a&0b000100)>0 :
                print('0 - -',bin(a))
            elif(a&0b000010)>0:
                print('- O -',bin(a))
            elif (a&0b000001)>0:
                print('- - O',bin(a))
            else:
                print('- - -')
            if (a&0b100000)>0:
                print('O',end=' ')
            else:
                print('X',end=' ')
            if (a&0b010000)>0 :
                print('O',end=' ')
            else:
                print('X',end=' ')
            if(a&0b001000)>0:
                print('O')
            else:
                print('X')
            print('======')
        a=str(a)
        a = a.encode('utf-8')
        client_socket.send(a)
        a=0
        reply = client_socket.recv(1024)
        reply = reply.decode('utf-8')
        reply = int(reply)
        print('reply = ',reply)
        if count < 1 and reply > 0:
            count = 1
            pygame.mixer.music.play()
            print('sound play')
        if count > 0:
            count = count+1
        elif count> 40:
            count = 0
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
        time.sleep(0.2)    
except Exception as e:
    print('socket closed',e)
    client_socket.close()
