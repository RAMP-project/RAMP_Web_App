import numpy as np
from .RAMPedited.ramp.core.stochastic_process import Stochastic_Process

def run_ramp(list_of_appliances):
    profile = Stochastic_Process(appliances_list=list_of_appliances)
    # convert from 365 day profiles in minutes to one hourly profile
    yearly_profile_in_minutes = np.zeros(0)
    for prof in profile:
        yearly_profile_in_minutes = np.append(yearly_profile_in_minutes, prof)
    yearly_profile_in_hours = np.zeros(8760)
    for i in range(8760):
        yearly_profile_in_hours[i] = sum(yearly_profile_in_minutes[i*60:(i+1)*60-1]) / 60
    yearly_profile_in_hours_in_kW = yearly_profile_in_hours / 1000
    load_elec = yearly_profile_in_hours_in_kW.tolist()

    return load_elec
