import serial

def main():
	ser = serial.Serial('/dev/tty.usbmodem1411', 9600)
	classification = ''

	#####CODE TO CLASSIFY TRASH

	if classification == 'trash':
		ser.write('0')
	else:
		ser.write('1')


if __name__ == '__main__':
    main()