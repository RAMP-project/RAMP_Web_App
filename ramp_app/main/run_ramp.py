import numpy as np
from ramp import User,calc_peak_time_range,yearly_pattern
from datetime import datetime

def run_ramp(name, list_of_appliances):
    # Create a user category
    myuser = User(
        user_name=name,
        num_users=1,  # Specifying the number of specific user category in the community
    )

    for app in list_of_appliances:
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

        a = myuser.add_appliance(name=app['name'], number=app['number'], power=app['P'], num_windows=app['num_windows'], func_time=app['func_time'],
                             time_fraction_random_variability=app['r_t']/100, func_cycle=app['func_cycle'], occasional_use=app['occasional_use']/100,
                             wd_we_type=app['wd_we'])
        a.windows(window_1=[window_1_start_minutes, window_1_end_minutes], window_2=[window_2_start_minutes, window_2_end_minutes],
                  random_var_w=app['r_w']/100, window_3=[window_3_start_minutes, window_3_end_minutes])

    whole_year_profile = []
    Year_behaviour = yearly_pattern()
    ptr = calc_peak_time_range(user_list=[myuser])
    for i in range(365):
        whole_year_profile.extend(
            myuser.generate_single_load_profile(
                prof_i=i,
                peak_time_range=ptr,
                day_type=Year_behaviour[i],
            )
        )
    # convert from minutes and W to hours and kW profile
    yearly_profile_in_minutes = np.array(whole_year_profile)
    yearly_profile_in_hours = np.zeros(8760)
    for i in range(8760):
        yearly_profile_in_hours[i] = sum(yearly_profile_in_minutes[i*60:(i+1)*60-1]) / 60
    yearly_profile_in_hours_in_kW = yearly_profile_in_hours / 1000
    load_elec = yearly_profile_in_hours_in_kW.tolist()

    return load_elec
