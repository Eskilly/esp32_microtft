#-*-coding:utf_8-*-
from umqtt.simple import MQTTClient
from machine import Pin
#import network
import time
import machine
import dht
from machine import Timer
from tft import TFT,st7789
import font8x8

SSID="DESKTOP-RP2SCQP4177"#你的wifi名称
PASSWORD="www12345687"#你的wifi密码
 #三元组信息
SERVER ='192.168.137.1'  #MQTT Server: 网址LGSODS81VJ.iotcloud.tencentdevices.com
CLIENT_ID = "esp32"   #设备ID
PORT=1883#端口号
#三元组的
username=''
password=''
 #主题
publish_TOPIC = '222'
subscribe_TOPIC =''
d=dht.DHT11(Pin(13))#连接引脚
#以json发送温湿度数据：
def pubdata(temp,hum):#
    message=r'{"temperature":%d,"humidity":%d}'%(temp,hum)
    return message
#wifi连接配置
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    start_time=time.time()
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            
            pass
            if time.time()-start_time>15:
                print("WIFI Connected Timeout!")
                break
    if wlan.isconnected():
        print('network config:', wlan.ifconfig())
        return True
    else:
        return False

#定义mqqt发送数据

def MQTT_Send(tim):
    d.measure()
    #发送温湿度
    client.publish(publish_TOPIC,pubdata(d.temperature(),d.humidity()))

#连接上wifi后判断是否连接上MQTT
def showtext(tim):
    d.measure()
    dt=d.temperature()
    dh=d.humidity()
    TFT.text(font8x8,r'temperature:%d'%(dt),0,0)
    TFT.text(font8x8,r'humidity:%d'%(dh),0,8)
    time.sleep(10)
    TFT.fill(st7789.BLACK)
def main():
    try:
        do_connect()
        client=MQTTClient(CLIENT_ID,SERVER,PORT,username,password,60)
        client.connect()
        tim=Timer(-1)
        tim.init(period=10000,mode=Timer.PERIODIC,callback=MQTT_Send)
    except:
        tim=Timer(-1)
        tim.init(period=10000,mode=Timer.PERIODIC,callback=showtext)
