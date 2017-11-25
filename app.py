from time import sleep
from enum import Enum

from ctrl9001 import Pigeon, State
from gpiozero import Button, LED
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008 as MCP3008

GPIO_POWER_BUTTON = 24

SPI_PORT = 0
SPI_DEVICE = 0

MAX_SLIDE_VALUE = 1023

SLIDE_MODIFIER = 400

CYCLE_TIME = 100

class Color(Enum):
	RED = 1
	GREEN = 2


class RGLED:
	def __init__(self, red, green):
		self.red_led = red
		self.green_led = green
		self.color = None


	def toggle(self):
		if self.color is Color.RED:
			self.green()
		elif self.color is Color.GREEN:
			self.red()
		elif self.color is None:
			self.red()


	def green(self):
		self.red_led.off()
		self.green_led.on()
		self.color = Color.GREEN


	def red(self):
		self.green_led.off()
		self.red_led.on()
		self.color = Color.RED


pigeon = Pigeon()
state = State()

mcp = MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

power_button = Button(GPIO_POWER_BUTTON)

rgled = RGLED(LED(22), LED(27))
rgled.red()


def calc_operating_ratio(slide_state):
	# Calculate slide state in percent
	return (100 - (100 / (MAX_SLIDE_VALUE + (SLIDE_MODIFIER * 2))) * \
		(slide_state + SLIDE_MODIFIER)) * 0.01



def switch_power():
	state.power = not state.power
	rgled.toggle()
	pigeon.push(state)

power_button.when_pressed = switch_power

try:
	while True:
		ratio_slide_state_1 = mcp.read_adc(0)
		ratio_slide_state_2 = mcp.read_adc(1)

		print(ratio_slide_state_1)
		print(ratio_slide_state_2)

		state.cycle_time = CYCLE_TIME
		state.operating_ratios = [
			calc_operating_ratio(ratio_slide_state_1),
			calc_operating_ratio(ratio_slide_state_2)
		]
		
		pigeon.push(state)

		sleep(0.5)

except KeyboardInterrupt:
	state.power = False
	pigeon.push(state)