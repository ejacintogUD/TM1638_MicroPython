from TM1638 import TM1638
from machine import Pin
from time import sleep

# Define los pines que uses para el módulo TM1638
stb_pin = 8    # Pin de STB
clk_pin = 21   # Pin de CLK
dio_pin = 20   # Pin de DIO

# Crea una instancia del objeto TM1638
tm1638 = TM1638(stb_pin, clk_pin, dio_pin)

# Inicializa el display
tm1638.init()
print("Arranque del programa")
# Muestra un número en el display
tm1638.displayNumber(12345678)
sleep(2)

# Enciende un LED en la posición 0
#tm1638.displayLed(2, True)
#sleep(2)

# Limpia el display
#tm1638.clearDisplay()
#sleep(2)
# Limpia los LEDs
#tm1638.clearLeds()
#sleep(2)

a = 0

while True:
    keys = tm1638.readKeys()
    if (keys != 0):
        print(f"Boton {keys} presionado")
    
    tm1638.displayNumber(a)
    a += 1
    
    sleep(0.1)
    
    
    