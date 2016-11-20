from cv2 import *
from clarifai.rest import ClarifaiApp
import serial

def photo():
	# initialize the camera

	camera_port = 0
	ramp_frames = 30

	cam = VideoCapture(camera_port)

	for i in range(ramp_frames):
		s, temp = get_image(cam)

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
	while True:
		ser = serial.Serial('/dev/tty.usbmodem1411', 9600)
		classification = ''

		arduino = True

		#loop here until arduino prints python
		while arduino:
			data = ser.readline()[:-2]
			if data == 'python':
				arduino = False

		photo()
		prediction = predict()
	
		label = prediction[1]['name'].split(' ', 1)[0]
		print label

		if label == 'recyclable':
			ser.write('0')
		else:
			ser.write('1')


if __name__ == '__main__':
    main()
