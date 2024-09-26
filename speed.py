import Jetson.GPIO as GPIO
import time

# GPIO 핀 설정
Sigpin1 = 8
Sigpin2 = 12
speed_pin = 9
In1 = 5
In2 = 6

# 초기값 설정
isOverspeed = False
isEmergency = False
v1 = 0
v2 = 0
overSpeed = 5

# GPIO 모드 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Sigpin1, GPIO.IN)
GPIO.setup(Sigpin2, GPIO.IN)
GPIO.setup(speed_pin, GPIO.OUT)
GPIO.setup(In1, GPIO.OUT)
GPIO.setup(In2, GPIO.OUT)

# 액추에이터 상승
def actuatorUp():
    GPIO.output(In1, GPIO.LOW)
    GPIO.output(In2, GPIO.HIGH)
    GPIO.output(speed_pin, GPIO.HIGH)

# 액추에이터 하강
def actuatorDown():
    GPIO.output(In1, GPIO.HIGH)
    GPIO.output(In2, GPIO.LOW)
    GPIO.output(speed_pin, GPIO.HIGH)

# 속도센서 1 측정
def speedCheck1():
    global v1
    start_time = time.time()

    while GPIO.input(Sigpin1):
        pass
    while not GPIO.input(Sigpin1):
        pass
    duration = time.time() - start_time

    if duration != 0:
        frequency = 1.0 / duration
        v1 = int((frequency * 1e6) / 33.0)
        print("speed : ", v1)

        if v1 > 120:
            v1 = 0
            print("speed : ", v1)
    else:
        v1 = 0
        print("speed : ", v1)

# 속도센서 2 측정
def speedCheck2():
    global v2
    start_time = time.time()

    while GPIO.input(Sigpin2):
        pass
    while not GPIO.input(Sigpin2):
        pass
    duration = time.time() - start_time

    if duration != 0:
        frequency = 1.0 / duration
        v2 = int((frequency * 1e6) / 33.0)
        print("speed : ", v2)

        if v2 > 120:
            v2 = 0
            print("speed : ", v2)
    else:
        v2 = 0
        print("speed : ", v2)

# AI 인식
def detectEmergency():
    # 추후 추가

# LCD 버퍼 클리어
def clear_serial_buffer():
    # 추후 추가

def drawMessage():
    # 추후 추가

def loop():
    global isOverspeed

    speedCheck1()
    speedCheck2()

    # detectEmergency()

    isOverspeed = v1 >= overSpeed or v2 >= overSpeed

    if isOverspeed:
        if not isEmergency:
            actuatorDown()
            time.sleep(3)
            actuatorUp()

if __name__ == '__main__':
    try:
        actuatorUp()  # 초기 액츄에이터 상태
        while True:
            loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
