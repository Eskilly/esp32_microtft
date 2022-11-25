import st7789
from machine import Pin, SPI
spi=SPI(2,baudrate=40000000,polarity=1,sck=Pin(18),mosi=Pin(23))
TFT=st7789.ST7789(spi,240,240,reset=Pin(4,Pin.OUT),dc=Pin(2,Pin.OUT),backlight=Pin(5,Pin.OUT),rotation=0)
