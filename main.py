from machine import Pin, UART, SPI, ADC, I2C
import time
import ssd1306
import DFRobot_MAX31855

i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=10000)
max31855 = DFRobot_MAX31855.DFRobot_MAX31855(i2c)

setTempPin = Pin(16, Pin.IN, Pin.PULL_UP)
ovenOnPin = Pin(17, Pin.IN, Pin.PULL_UP)
elementOnPin = Pin(18, Pin.OUT)
targetTemp = 100
currentTemp = 0

tempArray = []
tempArrayPointer=0
tempAverage = 0

tempSetPot = ADC(Pin(26))

#tempSense = ADC(Pin(27))

#Screen

#screenspi = SPI(0)

screenspi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))

screenDCPin = Pin(8)
screenRSTPin = Pin(9)
screen1Pin = Pin(6)

#screenRSTPin.value(0)
#time.sleep(1)
#screenRSTPin.value(1)
#time.sleep(1)


screen1 = ssd1306.SSD1306_SPI(128,32, screenspi,screenDCPin,screenRSTPin,screen1Pin)

time.sleep(1)

screen1.fill(1)
screen1.show()

#maths from: https://www.arduino.cc/reference/en/language/functions/math/map/
def convert_temp(x, in_min, in_max, out_min, out_max):   
    return((x - in_min)*(out_max - out_min)/(in_max - in_min) + out_min)

#Check the current temp set pot position
tempValue = tempSetPot.read_u16()
targetTemp = round(convert_temp(tempValue, 100, 65500, 50, 200))

elementOnPin.value(0)

screen1.fill(0)
screen1.text('Starting up',0,0,1)
screen1.show()


#load temperature list for 10 values to initilise
for i in range(10):
    val = max31855.read_celsius()
    tempArray.append(val)
    time.sleep(0.1)
print(tempArray)

while True:
    
    #check current Temp
    for x in range(10):
        tempArray[tempArrayPointer]= max31855.read_celsius()
        #print(tempArray)
        if tempArrayPointer <9:
            tempArrayPointer = tempArrayPointer + 1
        else:
            tempArrayPointer = 0
        tempArraySum = 0
        time.sleep(0.01)
    for i in range(10):
        tempArraySum = tempArraySum  + tempArray[i]
    #tempAverage = tempArraySum / 10
    currentTemp = tempArraySum / 10
    print(round(currentTemp))
    
    currentTemp = max31855.read_celsius()
    print("Current Temp")
    print(currentTemp)
    if setTempPin.value() == 1:
        print("Set Value")
        screen1.fill(0)
        screen1.text('Set Temp: ',0,0,1)
        screen1.text(str(targetTemp) ,80,0,1)
        screen1.show()
        tempValue = tempSetPot.read_u16()
        targetTemp = round(convert_temp(tempValue, 100, 65500, 50, 200))
        print(tempValue)
        print(targetTemp)
        
        
    else:
        #print("Temp set")
        #print(targetTemp)
        screen1.fill(0)
        screen1.text('Target: ',0,0,1)
        screen1.text(str(targetTemp) ,80,0,1)        
        screen1.show()
    
    screen1.text('Current Temp: ',0,10,1)
    screen1.text(str(currentTemp),0,20,1)
    screen1.show()
    
    if ovenOnPin.value() == 1:
        if currentTemp < targetTemp:
            elementOnPin.value(1)
            print("Element On")
            #print(currentTemp)
        else:
            elementOnPin.value(0)
            print("Element Off")
    else:
        elementOnPin.value(0)
        print("Element Off")    

    time.sleep(1)																															