import time
import VL53L0X

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x42)
tof2 = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
# I2C Address can change before tof.open()
tof.open()
tof2.open()

# Start ranging
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
tof2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing/1000))

for count in range(1, 101):
    distance = tof.get_distance()
    distance2 = tof2.get_distance()

    if distance > 0:
        print("tof 1 is : %d mm, %d cm, %d" % (distance, (distance/10), count))
    if distance2 > 0:
        print("2 is : %d mm, %d cm, %d" % (distance2, (distance2/10), count))

    time.sleep(timing/1000000.00)

tof.stop_ranging()
tof.close()
tof2.stop_ranging()
tof2.close()

