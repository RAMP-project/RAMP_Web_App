# -*- coding: utf-8 -*-

#%% Initialisation of a model instance

import numpy as np 
import importlib
from .core import User
from datetime import datetime

def yearly_pattern():
    '''
    Definition of a yearly pattern of weekends and weekdays, in case some appliances have specific wd/we behaviour
    '''
    #Yearly behaviour pattern
    Year_behaviour = np.zeros(365)
    Year_behaviour[5:365:7] = 1
    Year_behaviour[6:365:7] = 1
    
    return(Year_behaviour)


# def user_defined_inputs(j): # edited by NESSI Team
#     '''
#     Imports an input file and returns a processed User_list
#     '''
#
#     file_module = importlib.import_module(f'input_files.input_file_{j}')
#
#     User_list = file_module.User_list
#
#     return(User_list)

def user_defined_inputs(appliances_list):
    User_List = []
    myuser = User("my_user")
    User_List.append(myuser)
    for app in appliances_list:
        window_1_start_hours = datetime.strptime(app['window_1_start'], '%H:%M')
        window_1_start_minutes = int(window_1_start_hours.hour * 60 + window_1_start_hours.minute)
        window_1_end_hours = datetime.strptime(app['window_1_end'], '%H:%M')
        window_1_end_minutes = int(window_1_end_hours.hour * 60 + window_1_end_hours.minute)
        window_2_start_hours = datetime.strptime(app['window_2_start'], '%H:%M')
        window_2_start_minutes = int(window_2_start_hours.hour * 60 + window_2_start_hours.minute)
        window_2_end_hours = datetime.strptime(app['window_2_end'], '%H:%M')
        window_2_end_minutes = int(window_2_end_hours.hour * 60 + window_2_end_hours.minute)
        window_3_start_hours = datetime.strptime(app['window_3_start'], '%H:%M')
        window_3_start_minutes = int(window_3_start_hours.hour * 60 + window_3_start_hours.minute)
        window_3_end_hours = datetime.strptime(app['window_3_end'], '%H:%M')
        window_3_end_minutes = int(window_3_end_hours.hour * 60 + window_3_end_hours.minute)

        a = myuser.Appliance(myuser, n=app['number'], P=app['P'], w=app['num_windows'], t=app['func_time'],
                             r_t=app['r_t']/100, c=app['func_cycle'], occasional_use=app['occasional_use']/100,
                             wd_we_type=app['wd_we'])
        a.windows(w1=[window_1_start_minutes, window_1_end_minutes], w2=[window_2_start_minutes, window_2_end_minutes],
                  r_w=app['r_w']/100, w3=[window_3_start_minutes, window_3_end_minutes])

    return User_List


def Initialise_model():
    '''
    The model is ready to be initialised
    '''
    # num_profiles = int(input("please indicate the number of profiles to be generated: ")) #asks the user how many profiles (i.e. code runs) he wants
    # print('Please wait...')
    num_profiles = 365
    Profile = [] # creates an empty list to store the results of each code run, i.e. each stochastically generated profile
    
    return (Profile, num_profiles)
    
def Initialise_inputs(j):
    Year_behaviour = yearly_pattern()
    #user_defined_inputs(j)
    user_list = user_defined_inputs(j)
    
    # Calibration parameters
    '''
    Calibration parameters. These can be changed in case the user has some real data against which the model can be calibrated
    They regulate the probabilities defining the largeness of the peak window and the probability of coincident switch-on within the peak window
    '''
    peak_enlarg = 0.15 #percentage random enlargement or reduction of peak time range length
    mu_peak = 0.5 #median value of gaussian distribution [0,1] by which the number of coincident switch_ons is randomly selected
    s_peak = 0.5 #standard deviation (as percentage of the median value) of the gaussian distribution [0,1] above mentioned
    op_factor = 0.5 #off-peak coincidence calculation parameter

    return (peak_enlarg, mu_peak, s_peak, op_factor, Year_behaviour, user_list)

