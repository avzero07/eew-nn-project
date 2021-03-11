'''
Collection of code to interact with
EQ event lists.
'''

import datetime
import pandas as pd

class eq_events:
    def __init__(self,path_to_event_csv):
        self.data_frame = pd.read_csv(path_to_event_csv,sep='|')

    def add_column(self,col_name,init_val):
        self.data_frame[col_name] = init_val

    def get_date_time(self,row_num,dt_col_name='Time'):
        dt = self.data_frame[dt_col_name][row_num]
        dt_list = dt.split('T')
        date_list = dt_list[0].split('-')
        time_list = dt_list[1].split(':')

        dt_obj = datetime.datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]),
                          int(time_list[0]),int(time_list[1]),int(time_list[2]))
        return dt_obj
