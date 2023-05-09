"""
Pulse extraction using POS algorithm (%(version)s)
"""
from scipy.signal import welch
import cv2
import numpy as np
from scipy import signal
import time
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
import pyqtgraph as pg
import matplotlib.pyplot as plt
from signal_processing import Signal_processing
from face_utilities import Face_utilities
import mediapipe as mp
from scipy.signal import savgol_filter
import padasip as pa
import scipy as sp
import matplotlib
import os
import sys
# sys.path.insert(0, './SkinDetector')
sys.path.append('C:/Users/kik/OneDrive/เดสก์ท็อป/POS_implementation/rppg-pos/SkinDetector')
# print(sys.path)
import skin_detector
import pkg_resources
from scipy.interpolate import CubicSpline

# import skin_detector

print("passed all import")

mp_facedetector = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils



def main(user_input=None):

    BUFFER_SIZE = 300
    sp = Signal_processing()
    framerate = 30
    l = int(framerate * 1.6)
    t = time.time()
    times = []
    filtered_data = []
    nsegments = 8
    fft_of_interest = []
    freqs_of_interest = []
    savitskized_data = []
    # with mp_facedetector.FaceDetection(min_detection_confidence = 0.7) as face_detection:
    #plotting
    app = QApplication([])
    win = pg.GraphicsLayoutWidget()    
    #win = pg.GraphicsLayoutWidget(title="plotting")
    p1 = win.addPlot(title="detrend")
    p2 = win.addPlot(title ="filterd&savitskized")
    win.resize(1400,400)
    # win.show()
    S = []
    # p3 = win.addPlot(title="pure green channel")

    # win.resize(600,600)
    win.show()

    # def masking() :
    #     mask = np.zeros_like()
    #     mask = cv2.fillPoly(mask,[point],(255,255,255))
    #     masked = cv2.bitwise_and(image,mask)

    def update():
        p1.clear()
        p1.plot(np.column_stack((freqs_of_interest,fft_of_interest)), pen = 'g')
        # p1.plot(np.column_stack((green_f,green_psd)), pen = 'g')

            
        p2.clear()
        p2.plot(normalized_data[20:],pen='g') 
        
        app.processEvents()
                
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(300) # update grapg ทุก ๆ 300ms

    # FREQUENCY ANALYSIS
    nsegments = 4
    # As increasing segments, f less resolution
    plot =  False
    image_show = True
    camera = cv2.VideoCapture(0)
     
    # loop on video frames
    frame_counter = 0

    with mp_facedetector.FaceDetection(min_detection_confidence = 0.7) as face_detection:        
    #  while camera.isOpened():
        while True:
            (grabbed, frame) = camera.read()
        
            if not grabbed:
                continue
           
            h,w,_ = frame.shape
            # convert frame to gray scale 
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)
            # convert back 
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            # rects = detector(gray, 0)

            # if len(rects)==0:
            if not(results.detections) :
                # if no face detected --> read next frame
                continue

            if image_show:
                show_frame = frame.copy()
        
            if results.detections:
                for id, detection in  enumerate(results.detections):
                    mp_draw.draw_detection(image, detection)
                    bBox = detection.location_data.relative_bounding_box
                    h,w,c = image.shape

                    boundBox = int(bBox.xmin*w),int(bBox.ymin*h),int(bBox.width*w),int(bBox.height*h)
                    cv2.putText(image,f'{int(detection.score[0]*100)}%',(boundBox[0],boundBox[1]-20),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)
                    ROI = image[boundBox[1]:boundBox[1]+boundBox[3],boundBox[0]:boundBox[0]+boundBox[2]]  

                mask = skin_detector.process(ROI)           
                
                masked_face = cv2.bitwise_and(ROI, ROI, mask=mask)
                # count only > 0 value (not black)
                number_of_skin_pixels = np.sum(mask>0)

                #compute mean
                r = np.sum(masked_face[:,:,2])/number_of_skin_pixels
                g = np.sum(masked_face[:,:,1])/number_of_skin_pixels 
                b = np.sum(masked_face[:,:,0])/number_of_skin_pixels

                if frame_counter==0:
                    mean_rgb = np.array([r,g,b])
                else:
                    mean_rgb = np.vstack((mean_rgb,np.array([r,g,b])))
                   
            times.append(time.time() - t)            
                
            L = len(mean_rgb)
            # L = 1,2,3,4,... ไล่ค่า frame เเต่ละเฟรมที่จะไปใส่ใน buffer
            #print("buffer length: " + str(L))
                
            if L > BUFFER_SIZE:
                mean_rgb = mean_rgb[-BUFFER_SIZE:]
                # green_background_buffer = green_background_buffer[-BUFFER_SIZE:]
                times = times[-BUFFER_SIZE:]
                #bpms = bpms[-BUFFER_SIZE//2:]
                L = BUFFER_SIZE
            #print(times)
            if L==300: # ถ้ามีเฟรมครบ 300 เฟรม
                fps = float(L) / (times[-1] - times[0])
                # บอก framerate ใน frame 
                cv2.putText(image, "fps: {0:.2f}".format(fps), (30,int(image.shape[0]*0.95)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                projection_matrix = np.array([[3,-2,0],[1.5,1,-1.5]])
                X_Y = np.matmul(projection_matrix,mean_rgb.T)
                std = np.array([1,-np.std(X_Y[0,:])/np.std(X_Y[1,:])])
                S = np.matmul(std,X_Y) # <----- h = tuning 
                S = S/np.std(S) 
                S = S.tolist()
                detrended_data = sp.signal_detrending(S)
                #print(len(detrended_data))
                #print(len(times))
                filtered_data = sp.butter_bandpass_filter(detrended_data,0.7,4,fps, order = 3)
                # savitskized_data  = savgol_filter(filtered_data,11,3)
                # interpolated_data =  spline(filtered_data, times)
                print(f'len_time = {len(times)}')
                print(f'len filtered = {len(filtered_data)}')
                # peform linear interpolation 
                interpolated_data = sp.interpolation(filtered_data, times)
                savitskized_data  = savgol_filter(interpolated_data,11,3)
                normalized_data = sp.normalization(savitskized_data)                

                '''
                detrended_data = sp.signal_detrending(S)
                filtered_data = sp.butter_bandpass_filter(detrended_data,0.7,4,fps, order = 3)
                resampling_time,even_time,interpolated_data = sp.mi_interpolation(filtered_data,times)
                # perform cubic spline interpolation
                cs =  CubicSpline(even_time,interpolated_data)
                # savitskized_data  = savgol_filter(interpolated_data,11,3)
                normalized_data = sp.normalization(np.hamming(len(resampling_time))*cs(resampling_time))
                # normalized_data = sp.normalization(savitskized_data)
                segment_length = (2*len(resampling_time)) // (nsegments + 1)

                
                green_f, green_psd = welch(normalized_data, 30, 'hamming', nperseg=segment_length) #, scaling='spectrum',nfft=2048)
                # scipy.signal.welch(x, fs=1.0, window='hann', nperseg=None, noverlap=None, nfft=None, detrend='constant', return_onesided=True, scaling='density', axis=-1, average='mean')[source]
                # window = flattop 
                # return freq range and PSD
                
                # npersegint, optional
                # Length of each segment. Defaults to None, but if window is str or tuple, is set to 256, and if window is array_like, is set to the length of the window.
                print("Green F, Shape",green_f,green_f.shape)
                print("Green PSD, Shape",green_psd,green_psd.shape)

                #green_psd = green_psd.flatten()
                # return index of f that is greater than 0.9 Hz 
                first = np.where(green_f > 0.9)[0] #0.8 for 300 frames 
                last = np.where(green_f < 1.8)[0]

                # >>> x = np.array([1,2,3,4,5])
                # >>> np.where(x>2)
                # (array([2, 3, 4], dtype=int64),)
                # >>> np.where(x>2)[0]
                # array([2, 3, 4], dtype=int64)

                first_index = first[0]
                last_index = last[-1]
                range_of_interest = range(first_index, last_index + 1, 1)

                max_idx = np.argmax(green_psd[range_of_interest])
                f_max = green_f[range_of_interest[max_idx]]
                hr = f_max*60.0
                
                # max_arg = np.argmax(fft_of_interest)
                # bpm = freqs_of_interest[max_arg]
                cv2.putText(image, "HR: {}".format(round(hr)), (int(image.shape[1]*0.8),int(image.shape[0]*0.95)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                '''

                
                # filtered_data = sp.butter_bandpass_filter(interpolated_data,0.7,4,fps, order = 3)
                print(f'fps = {fps}')
                fft_of_interest, freqs_of_interest = sp.fft(normalized_data, fps)
                
                max_arg = np.argmax(fft_of_interest)
                bpm = freqs_of_interest[max_arg]
                cv2.putText(image, "HR: {}".format(round(bpm)), (int(image.shape[1]*0.8),int(image.shape[0]*0.95)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                #print(detrended_data)

                #cv2.imshow("frame",show_frame)
                


            cv2.imshow("Masked face",masked_face)
            cv2.imshow('ROI',ROI)
            cv2.imshow('show',image)
            key = cv2.waitKey(1)
            if key == ord('x'):
                break

            frame_counter +=1
        
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
	main()