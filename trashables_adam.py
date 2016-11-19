import cv2
from clarifai.rest import ClarifaiApp
import serial

def get_image(camera):
	retval, im = camera.read()
	return im

def photo():

	camera_port = 0
	ramp_frames = 30
	camera = cv2.VideoCapture(camera_port)
 
	for i in xrange(ramp_frames):
		temp = get_image(camera)
	print("Taking image...")
	camera_capture = get_image(camera)
	cv2.imwrite("test_adam.jpg", camera_capture)
	del(camera)

def predict():
	#for better security, we could put the CLIENT_ID and CLIENT_SECRET into another file
	CLIENT_ID = '-kJkjcvdqlynN1-cWy4rZwOdztrOwc_vt5QAd5RF'
	CLIENT_SECRET = 'hmS1WDSfn2W4d35Mh1sR1l8N9e_eRsb0OVMvfkd_'
	app = ClarifaiApp(CLIENT_ID, CLIENT_SECRET)
	model = app.models.get('b9f4b8160f9747cb8e11df787d77a5e5')
	prediction = model.predict_by_filename('test_adam.jpg')

	return prediction

def main():
	ser = serial.Serial('/dev/tty.usbmodem1411', 9600)
	classification = ''

	#####CODE TO CLASSIFY TRASH
	photo()
	prediction = predict()

	#manipulate the prediction to get classification
	
	classification = 'trash'
	if classification == 'trash':
		ser.write('0')
	else:
		ser.write('1')


if __name__ == '__main__':
    main()