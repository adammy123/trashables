from cv2 import *
from clarifai.rest import ClarifaiApp
import serial
from twilio.rest import TwilioRestClient

def send_sms(message):
	account_sid = "AC4108caa8ac86a72b977586da0ca3aeba"
	auth_token = "5b77b5abbc7f8546e8764d27a9805957"
	client = TwilioRestClient(account_sid, auth_token)

	message = client.messages.create(to="+17737077025", from_="+18472609589", body=message)

def photo(cam):
	s, img = get_image(cam)

	if s:    # frame captured without any errors
		namedWindow("cam-test")
		imshow("cam-test",img)
		waitKey(1)
		destroyWindow("cam-test")
		imwrite("test.jpg",img)

def get_image(camera):
	s, img = camera.read()
	return s, img

def predict():
	#for better security, we could put the CLIENT_ID and CLIENT_SECRET into another file
	CLIENT_ID = '-kJkjcvdqlynN1-cWy4rZwOdztrOwc_vt5QAd5RF'
	CLIENT_SECRET = 'hmS1WDSfn2W4d35Mh1sR1l8N9e_eRsb0OVMvfkd_'
	app = ClarifaiApp(CLIENT_ID, CLIENT_SECRET)
	model = app.models.get('b9f4b8160f9747cb8e11df787d77a5e5')
	prediction = model.predict_by_filename('test.jpg')
	outputs = prediction['outputs'][0]['data']['concepts']
	output = []
	for concept in outputs:
		if len(output) < 5:
			output.append({'name': concept['name'], 'value': concept['value']})
	return output	

def main():
	camera_port = 0
	ramp_frames = 30
	cam = VideoCapture(camera_port)

	for i in range(ramp_frames):
		s, temp = get_image(cam)
	ser = serial.Serial('/dev/tty.usbmodem1411', 9600)

	#loop this indefinitely
	while True:
		arduino = True

		#loop here until arduino prints python, fullwaste or fullrecycle
		while arduino:
			data = ser.readline()[:-2]
			if data == 'python':
				arduino = False
			elif data == 'fullwaste':
				print 'Waste bin is full. Message sent'
				#ADD code for twilio msg
				send_sms('Waste bin is full. Please empty trash, thank you :)')
				
			elif data == 'fullrecycle':
				print 'Recycling bin is full'
				#Add code for twilio msg
				send_sms('Recycling bin is full. Please empty trash, thank you :)')
			

		photo(cam)
		prediction = predict()
	
		label = prediction[1]['name'].split(' ', 1)[0]
		print label

		if label == 'recyclable':
			ser.write('0')#left
		else:
			ser.write('1')#right


if __name__ == '__main__':
    main()
