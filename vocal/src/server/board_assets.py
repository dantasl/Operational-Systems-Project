import Adafruit_BBIO.GPIO as GPIO

# Dictionary with the PIN number associated to each room
house = {
	"KITCHEN": "P9_12",
	"BATHROOM": "P9_15",
	"LIVINGROOM": "P9_42"
}


def get_status(pin_number):
	"""Verify the status of the GPIO pin with number equal to `pin_number`.

	Parameters
	----------
	pin_number : str
		The PIN to check the status.

	Returns
	-------
	str
		String with information if the GPIO pin is ON or OFF.
	"""

	if GPIO.input(pin_number):
		return "ON"
	return "OFF"


def compose_status():
	"""Compose a string with the status of all the rooms (i.e. if they are turned on or off).

	Returns
	-------
	str
		String with information if the room's LED is turned on or off.
	"""

	return "KITCHEN {}, BATHROOM {}, LIVING ROOM {}".format(
		get_status(house["KITCHEN"]),
		get_status(house["BATHROOM"]),
		get_status(house["LIVINGROOM"])
	)


def decode_command(command):
	"""Decode command from the user and call the appropriate function.

	After receiving the command from the user, this function will try to decode
	to the available sentences supported by the application. If there is a match,
	this function will call the appropriate function to perform the requested
	action.

	Parameters
	----------
	command : bytes
		The command spoken by the user.

	Returns
	-------
	bool
		True if the command could be performed and False otherwise.
	"""

	command = command.decode().lower()
	if command == "kitchen on":
		turn_on("KITCHEN")
	elif command == "kitchen off":
		turn_off("KITCHEN")
	elif command == "bathroom on":
		turn_on("BATHROOM")
	elif command == "bathroom off":
		turn_off("BATHROOM")
	elif command == "living room on":
		turn_on("LIVINGROOM")
	elif command == "living room off":
		turn_off("LIVINGROOM")
	elif command == "all on":
		turn_all_on()
	elif command == "all off":
		turn_all_off()
	else:
		print("Could not decode command.")
		return False
	return True	


def init_leds():
	"""Set all GPIO pins associated to the rooms as output."""

	for room in house:
		print("Component from {} configured, mode out.".format(room))
		GPIO.setup(house[room], GPIO.OUT)


def turn_on(room):
	"""Turn on the LED of a specific room.

	Parameters
	----------
	room : str
		Name of the room to turn on the LED.
	"""

	print("Turning on {}".format(room))
	GPIO.output(house[room], GPIO.HIGH)


def turn_off(room):
	"""Turn off the LED of a specific room.

	Parameters
	----------
	room : str
		Name of the room to turn off the LED.
	"""

	print("Turning off {}".format(room))
	GPIO.output(house[room], GPIO.LOW)


def turn_all_on():
	"""Turn on the LEDs of all the rooms."""

	for room in house:
		turn_on(room)


def turn_all_off():
	"""Turn off the LEDs of all the rooms."""

	for room in house:
		turn_off(room)
