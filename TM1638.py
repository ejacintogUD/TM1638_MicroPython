from machine import Pin
import time

class TM1638:
    def __init__(self, stb_pin, clk_pin, dio_pin):
        self._stb = Pin(stb_pin, Pin.OUT)
        self._clk = Pin(clk_pin, Pin.OUT)
        self._dio = Pin(dio_pin, Pin.OUT)
        self.digit = [0] * 8
        self.digitToSegment = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]
        self.init()

    def init(self):
        self.clearDisplay()
        self.clearLeds()
        self.setBrightness(7)  # Brillo máximo por defecto

    def setBrightness(self, brightness):
        if brightness > 7:
            brightness = 7
        command = 0x88 | brightness
        self.sendCommand(command)

    def displayDigit(self, position, data):
        if position < 0 or position >= 8:
            return
        self.digit[position] = self.digitToSegment[data] if data < len(self.digitToSegment) else 0
        self.sendData(position << 1, self.digit[position])

    def displayLed(self, led, state):
        if led < 0 or led >= 8:
            return
        self.sendData((led << 1) + 1, 0x01 if state else 0x00)

    def displayNumber(self, number):
        for i in range(8):
            if number > 0:
                self.displayDigit(7-i, number % 10)
                number //= 10
            else:
                self.displayDigit(7-i, 0)

    def clearDisplay(self):
        for i in range(8):
            self.displayDigit(i, 0)

    def clearLeds(self):
        for i in range(8):
            self.displayLed(i, False)

    def readKeys(self):
        keys = 0
        
        self.sendCommand(0x42)
        self._stb.off()
        self.sendByte(0x42)
        self._dio.init(Pin.IN)  # Cambiar a modo entrada
        for i in range(4):
            value = 0
           
            for j in range(8):
                if (self._dio.value()):
                    value |= (1 << j)
                self._clk.on()
                time.sleep_us(1)
                self._clk.off()
            keys |= (value << i)
        self._dio.init(Pin.OUT)  # Volver a salida
        self._stb.on()
        return keys

    def sendCommand(self, command):
        self._stb.off()
        self.sendByte(command)
        self._stb.on()

    def sendData(self, address, data):
        self.sendCommand(0x44)
        self._stb.off()
        self.sendByte(0xC0 | address)
        self.sendByte(data)
        self._stb.on()

    def sendByte(self, data):
        for i in range(8):
            self._dio.value(data & 0x01)
            self._clk.on()
            self._clk.off()
            data >>= 1
