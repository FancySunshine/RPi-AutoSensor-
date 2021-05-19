import time
import VL53L0X
import paho.mqtt.client as mqtt


def on_connect(client, userdata, rc, properties=None):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client(client_id="auto")
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.191.248", 1883, 60)

client.loop_start()

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x42)
tof2 = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)
# I2C Address can change before tof.open()
tof.open()
tof2.open()

# Start ranging
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
tof2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing / 1000))

# 센서 감지되었을 때 시간 간격(ms 기준, 1초)
interval = 1000

# 센서 변화 기준 거리(mm 기준, 1cm)
diff = 10

# 초기 before 값
before1 = tof.get_distance()
before2 = tof2.get_distance()

# 라즈베리 파이가 켜져있는 한 계속 실행
while True:
    # 현재 각 센서 거리 측정
    distance1 = tof.get_distance()
    distance2 = tof2.get_distance()

    # 밖 센서와 이전 측정 값의 차가 기준 값보다 클때(하나의 센서에서 출입 감지)
    if distance1 - before1 > diff:
        print("tof 1 is : %d mm, %d cm" % (distance1, (distance1 / 10)))
        print("PERSON IN")
        # 1초 동안 다른 센서로 출입 감지
        t_end = time.time() + (interval / 1000)
        before2 = tof2.get_distance()
        while time.time() < t_end:
            distance2 = tof2.get_distance()
            if distance2 - before2 > diff:
                print("CHECKED!!")
    if distance2 - before2 > diff:
        print("2 is : %d mm, %d cm" % (distance2, (distance2 / 10)))
        print("PERSON OUT")
        t_end = time.time() + (interval / 1000)
        before1 = tof.get_distance()
        while time.time() < t_end:
            distance1 = tof.get_distance()
            if distance1 - before1 > diff:
                print("CHECKED!!")

    before1 = distance
    before2 = distance2

    time.sleep(timing / 1000000.00)


