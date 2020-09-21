from machine import Pin,I2C
import pmsa003i
import ssd1327

i2c = I2C(sda=Pin("Y10"), scl=Pin("Y9"),freq=10000)

pmsensor = pmsa003i.PMSA003I(i2c, 0x12)
display = ssd1327.QWIIC_128X128_OLED(i2c)

while True:
    pmsensor.read()
    display.fill(0)
    display.text('PM 2.5 cf: ' + str(pmsensor.pm2_5_cf),0,10,15)
    display.text('PM 10.0: ' + str(pmsensor.pm10_0),0,30,15)
    display.text('pm2.5 per 0.1L: ',0,50,15)
    display.text(str(pmsensor.pm2_5_qty), 0, 62, 15)
    display.show()
    pyb.delay(1000)
