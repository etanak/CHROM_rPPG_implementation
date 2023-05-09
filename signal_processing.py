import cv2
import numpy as np
import time
from scipy import signal


class Signal_processing():
    def __init__(self):
        self.a = 1

    def extract_color(self, ROIs):
        '''
        extract average value of green color from ROIs
        '''
        
        #r = np.mean(ROI[:,:,0])
        g = []
        # cheeks

        for ROI in ROIs:
            g.append(np.mean(ROI[:,:,1]))

        # forehead
        # print(ROIs[:,:,1].shape)
        # print(ROIs[:,:,1])

        # # g.append(np.mean(ROIs[:,:,1]))
        # print((np.where(ROIs[:,:,1]!=0,ROIs[:,:,1],np.nan)))
        # g.append(np.nanmean(np.where(ROIs[:,:,1]!=0,ROIs[:,:,1],np.nan)))
        print(g)
        #b = np.mean(ROI[:,:,2])
        #return r, g, b
        output_val = np.mean(g)
        print(output_val)
        return output_val

    def extract_color_NaN(self, ROIs):
        '''
        extract average value of green color from ROIs
        '''
        
        #r = np.mean(ROI[:,:,0])
        g = []
        # cheeks

        # for ROI in ROIs:
        #     g.append(np.mean(ROI[:,:,1]))

        # forehead
        # print(ROIs[:,:,1].shape)
        # print(ROIs[:,:,1])

        # g.append(np.mean(ROIs[:,:,1]))
        print((np.where(ROIs[:,:,1]!=0,ROIs[:,:,1],np.nan)))
        g.append(np.nanmean(np.where(ROIs[:,:,1]!=0,ROIs[:,:,1],np.nan)))
        # print(g)
        #b = np.mean(ROI[:,:,2])
        #return r, g, b
        output_val = np.mean(g)
        print(output_val)
        return output_val
    
    def normalization(self, data_buffer):
        '''
        normalize the input data buffer
        '''
        
        #normalized_data = (data_buffer - np.mean(data_buffer))/np.std(data_buffer)
        normalized_data = data_buffer/np.linalg.norm(data_buffer)
        
        return normalized_data
    
    def signal_detrending(self, data_buffer):
        '''
        remove overall trending
        
        '''
        detrended_data = signal.detrend(data_buffer)
        
        return detrended_data
        
    def interpolation(self, data_buffer, times):
        '''
        interpolation data buffer to make the signal become more periodic (advoid spectral leakage)
        '''
        L = len(data_buffer)
        resampling_point =  L
        
        even_times = np.linspace(times[0], times[-1], resampling_point)
        
        interp = np.interp(even_times, times, data_buffer)
        interpolated_data = np.hamming(resampling_point) * interp
        return interpolated_data
    def mi_interpolation(self, data_buffer, times):
        '''
        interpolation data buffer to make the signal become more periodic (advoid spectral leakage)
        '''
        L = len(data_buffer)
        
        even_times = np.linspace(times[0], times[-1], L)
        resampling_time = np.linspace(times[0], times[-1], round(250*(times[-1]-times[0])))
        
        interp = np.interp(even_times, times, data_buffer)
        # interpolated_data = np.hamming(L) * interp

        return resampling_time,even_times,interp
        
    def fft(self, data_buffer, fps):
        '''
        
        '''
        
        L = len(data_buffer)
        
        freqs = float(fps) / L * np.arange(L / 2 + 1)
        
        freqs_in_minute = 60. * freqs
        
        raw_fft = np.fft.rfft(data_buffer*30)
        fft = np.abs(raw_fft)**2
        
        interest_idx = np.where((freqs_in_minute > 50) & (freqs_in_minute < 180))[0]
        print(freqs_in_minute)
        interest_idx_sub = interest_idx[:-1].copy() #advoid the indexing error
        freqs_of_interest = freqs_in_minute[interest_idx_sub]
        
        fft_of_interest = fft[interest_idx_sub]
        
        
        # pruned = fft[interest_idx]
        # pfreq = freqs_in_minute[interest_idx]
        
        # freqs_of_interest = pfreq 
        # fft_of_interest = pruned
        
        
        return fft_of_interest, freqs_of_interest
    def normalized_fft(self, data_buffer, fps):
        L = len(data_buffer)
            
        freqs = float(fps) / L * np.arange(L / 2 + 1)
            
        freqs_in_minute = 60. * freqs
            
        raw_fft = np.fft.rfft(data_buffer*30)
        fft = np.abs(raw_fft)**2
            
        interest_idx = np.where((freqs_in_minute > 50) & (freqs_in_minute < 180))[0]
        interest_idx_sub = interest_idx[:-1].copy() #advoid the indexing error
        freqs_of_interest = freqs_in_minute[interest_idx_sub]
            
        fft_of_interest = fft[interest_idx_sub]
            
        # Normalize the FFT
        normalized_fft = fft_of_interest / np.max(fft_of_interest)
        
        # Compute the RMS
        rms = np.sqrt(np.mean(np.square(normalized_fft)))
            
        return normalized_fft, freqs_of_interest, rms


    def butter_bandpass_filter(self, data_buffer, lowcut, highcut, fs, order=5):
        '''
        
        '''
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        # b, a = signal.butter(order, [low, high], btype='band')
       
        coefficients = signal.butter(order,[low, high], 'bandpass')

        return signal.filtfilt(*coefficients, data_buffer)
        
        # filtered_data = signal.lfilter(b, a, data_buffer)
        
        # return filtered_data
        
        
    
        
        
        
        
        
        
        
        