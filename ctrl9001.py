from socket import create_connection
from json import dumps, JSONEncoder

class StateEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, State):
			return {
				"power" : obj.power,
				"cycle_time" : obj.cycle_time,
				"operating_ratios" : obj.operating_ratios
			}
		return JSONEncoder.default(self, obj)


class State:
	def __init__(self, power=False, cycle_time=100,
		operating_ratios=None):

		self.power = power
		self.cycle_time = cycle_time
		if operating_ratios is None:
			self.operating_ratios = [1.0, 1.0]
		else:
			self.operating_ratios = operating_ratios


class Pigeon:
	def __init__(self, address=("pigeon9001.local", 1631)):
		self.sock = create_connection(address)

	def push(self, state):
		if type(state) is State:
			self.sock.send(
				dumps(state, cls=StateEncoder).encode() + b"\n")
		else:
			raise TypeError(
				"expected type '%s', got '%s'" % (
					State.__name__, type(state).__name__))