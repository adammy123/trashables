from cv2 import *
from clarifai.rest import ClarifaiApp
import serial
from twilio.rest import TwilioRestClient
import os

def load_twilio_config():
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_NUMBER')

    if not all([twilio_account_sid, twilio_auth_token, twilio_number]):
        logger.error(NOT_CONFIGURED_MESSAGE)
        raise MiddlewareNotUsed

    return twilio_number, twilio_account_sid, twilio_auth_token

def load_clarifai_config():
	clarifai_client_id = os.environ.get('CLARIFAI_CLIENT_ID')
	clarifai_client_secret = os.environ.get('CLARIFAI_CLIENT_SECRET')
	clarifai_model = os.environ.get('CLARIFAI_MODEL')
	return clarifai_client_id, clarifai_client_secret, clarifai_model

def load_my_number():
	return os.environ.get('MY_NUMBER')

def send_sms(message):
	twilio_number, account_sid, auth_token = load_twilio_config()
	client = TwilioRestClient(account_sid, auth_token)
	my_number = load_my_number()
	message = client.messages.create(to=my_number, from_=twilio_number, body=message)

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
	CLIENT_ID, CLIENT_SECRET, clarifai_model = load_clarifai_config()
	app = ClarifaiApp(CLIENT_ID, CLIENT_SECRET)
	model = app.models.get(clarifai_model)
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

			if data == 'fullwaste':
				print 'Waste bin is full. Message sent'
				#ADD code for twilio msg
				send_sms('Waste bin is full. Please empty trash, thank you :)')
				
			if data == 'fullrecycle':
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
