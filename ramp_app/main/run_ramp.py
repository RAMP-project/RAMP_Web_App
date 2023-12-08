import numpy as np
from ramp import User, UseCase
from datetime import datetime

def run_ramp(list_of_appliances):
    year = datetime.today().year

    # Create a user category
    myuser = User(
        num_users=1,  # Specifying the number of specific user category in the community
    )
    myusecase = UseCase(date_start=datetime(year, 1, 1), date_end=datetime(year, 12, 31), users=myuser)

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

        a = myuser.add_appliance(number=app['number'], power=app['P'], num_windows=app['num_windows'], func_time=app['func_time'],
                             time_fraction_random_variability=app['r_t']/100, func_cycle=app['func_cycle'], occasional_use=app['occasional_use']/100,
                             wd_we_type=app['wd_we'])
        a.windows(window_1=[window_1_start_minutes, window_1_end_minutes], window_2=[window_2_start_minutes, window_2_end_minutes],
                  random_var_w=app['r_w']/100, window_3=[window_3_start_minutes, window_3_end_minutes])


    whole_year_profile = myusecase.generate_daily_load_profiles()

    # convert from minutes and W to hours and kW profile
    yearly_profile_in_minutes = np.array(whole_year_profile)
    yearly_profile_in_hours = np.zeros(8760)
    for i in range(8760):
        yearly_profile_in_hours[i] = sum(yearly_profile_in_minutes[i*60:(i+1)*60-1]) / 60
    yearly_profile_in_hours_in_kW = yearly_profile_in_hours / 1000
    load_elec = yearly_profile_in_hours_in_kW.tolist()

    return load_elec
