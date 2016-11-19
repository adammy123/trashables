import serial
from cv2 import *
from clarifai.rest import ClarifaiApp

def photo():
	# initialize the camera
	cam = VideoCapture(0)   # 0 -> index of camera
	s, img = cam.read()
	if s:    # frame captured without any errors
		namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
		imshow("cam-test",img)
		waitKey(1)
		destroyWindow("cam-test")
		imwrite("test.jpg",img)

def predict():
	CLIENT_ID = '-kJkjcvdqlynN1-cWy4rZwOdztrOwc_vt5QAd5RF'
	CLIENT_SECRET = 'hmS1WDSfn2W4d35Mh1sR1l8N9e_eRsb0OVMvfkd_'
	app = ClarifaiApp(CLIENT_ID, CLIENT_SECRET)
	model = app.models.get('general-v1.3')
	prediction = model.predict_by_filename('test.jpg')
	print prediction
	return prediction

def main():
	ser = serial.Serial('/dev/tty.usbmodem1411', 9600)
	classification = ''

	#####CODE TO CLASSIFY TRASH
	photo()
	prediction = predict()
	#manipulate the prediction to get classification
	
	if classification == 'trash':
		ser.write('0')
	else:
		ser.write('1')


if __name__ == '__main__':
    main()