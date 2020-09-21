
'''
Auther: Alex Chu
Website: www.smart-prototyping.com
Email: shop@smart-prototyping.com
product link: https://www.smart-prototyping.com/Zio-Qwiic-PM-Air-Quality-Sensor-and-Adapter-Board
PMSA003I datasheet: https://github.com/ZIOCC/Zio-Qwiic-PM2.5-Air-Quality-Sensor-Adapter-Board/blob/master/PMSA003%20series%20data%20manua_English_V2.6.pdf

'''

class PMSA003I:

    def __init__(self, i2c, addr = 0x12):
        self.i2c = i2c
        self.addr = addr
        #cf=1, unit: ug/m^3
        self.pm1_0_cf = 0
        self.pm2_5_cf = 0
        self.pm10_0_cf = 0
        #Atmospheric environment data， ug/m^3
        self.pm1_0 = 0
        self.pm2_5 = 0
        self.pm10_0 = 0
        # quantity of different diameter particulates in 100ml air
        self.pm0_3_qty = 0      #bigger than 0.3um
        self.pm0_5_qty = 0      #bigger than 0.5um
        self.pm1_0_qty = 0      #bigger than 1.0um
        self.pm2_5_qty = 0      #bigger than 2.5um
        self.pm5_0_qty = 0      #bigger than 5.0um
        self.pm10_0_qty = 0     #bigger than 10.0um
        #error code
        self.error_code=0

    def read(self):
        data = self.i2c.readfrom(self.addr,32)
        if self.checkdata(data) == True:
            self.get_cf_data(data)
            self.get_at_pm_data(data)
            self.get_pm_qty_data(data)
        else:
            self.get_errro_code(data)
            return False


    def checkdata(self, data):
        if data[0] == 0x42:
            if data[1] == 0x4d:
                if (data[2] << 8) | data[3] == 28:
                    check_sum = (data[30]<<8) | data[31]
                    t= 0
                    for i in range(0,30):
                         t += data[i]
                    if check_sum == t:
                        return True
                    else:
                        return False

    # cf=1, unit: ug/m^3
    def get_cf_data(self, data):
        self.pm1_0_cf = (data[4] << 8) | data[5]
        self.pm2_5_cf = (data[6] << 8) | data[7]
        self.pm10_0_cf = (data[8] << 8) | data[9]

    # Atmospheric environment data， ug/m^3
    def get_at_pm_data(self,data):
        self.pm1_0 = (data[10] << 8) | data[11]
        self.pm2_5 = (data[12] << 8) | data[13]
        self.pm10_0 = (data[14] << 8) | data[15]

    # quantity of different diameter particulates in 100ml air
    def get_pm_qty_data(self,data):
        self.pm0_3_qty = (data[16] << 8) | data[17]      #bigger than 0.3um
        self.pm0_5_qty = (data[18] << 8) | data[19]      #bigger than 0.5um
        self.pm1_0_qty = (data[20] << 8) | data[21]      #bigger than 1.0um
        self.pm2_5_qty = (data[22] << 8) | data[23]      #bigger than 2.5um
        self.pm5_0_qty = (data[24] << 8) | data[25]      #bigger than 5.0um
        self.pm10_0_qty = (data[26] << 8) | data[27]     #bigger than 10.0um

    def get_errro_code(self,data):
        self.error_code = data[29]
