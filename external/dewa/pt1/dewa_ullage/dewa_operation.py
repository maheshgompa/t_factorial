import os
import sys

import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import select, text, func, delete

from rich import print
from rich.pretty import pprint
from rich.console import Console
from rich.table import Table
from rich.pretty import Pretty
from rich.text import Text

from models.pt1 import production as production_models
from models.pt1 import raw as raw_models

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone


class NotValidTestConditions(Exception):
    """Raised when there is not valid conditions to make the test"""

    # {{{

    def __init__(self, message="Not valid test conditions"):
        self.message = message
        super().__init__(self.message)

    # }}}


class UllageONOFFOperation:
    def __init__(self):
        # {{{

        self.raw_models = raw_models
        self.production_models = production_models

        # }}}

    def process(self, selected_date, update_database=True):
        # {{{
        self.perform_calculation(selected_date)
        self.write_raw_measures_and_set_alarms(selected_date)
        # self.ullageAlarmDefinitions(selected_date)
        # self.calculate_pump_regimen(selected_date)

        # }}}

    def perform_calculation(self, selected_date):
        # {{{

        try:
            initial_df = self.raw_models.KKSDescription.get_kkses_df(
                [ ('12wta07aa201', '12wta07aa201'),  ('12wta07aa202', '12wta07aa202'),  
                  ('12wta07aa203', '12wta07aa203'),  ('12wta07aa204', '12wta07aa204'),  
                  ('12wtu01cp901', '12wtu01cp901')
                   ],
                selected_date,
                index_name='timestamp'
            )
            # print(initial_df)
        except self.raw_models.NoKksData as e:
            print('Missing KKS: %s - %s' % (e.tag_name, e.message))
            exit(-1)

        initial_df['operation'] = 'OFF'
        initial_df.loc[((initial_df['12wta07aa201'] >= 1) | (initial_df['12wta07aa202'] >= 1) | 
                (initial_df['12wta07aa203'] >= 1) | (initial_df['12wta07aa204'] >= 1)) & (
                initial_df['12wtu01cp901'] >= 0.3), 'operation'] = 'ON'
        # print(initial_df)
                    
        self.production_models.UllageOperation.write_df(
            initial_df.loc[:, ['12wta07aa201', '12wta07aa202', '12wta07aa203', '12wta07aa204',
                '12wtu01cp901', 'operation']],
            only_insert=False, index=True
        )

    # }}}

    def write_raw_measures_and_set_alarms(self, selected_date):
        # {{{

        dfs = []
        with Session(self.production_models.engine) as session:
            for sensor in session.scalars(select(self.production_models.UllageSensor)):

                try:
                    sensor_raw_df = sensor.get_raw_df(selected_date, ['kks', 'id'])
                except self.raw_models.NoKksData:
                    # self.missing_kkses.append(kks1)
                    print('Missing kks: %s' % sensor.kks)
                    continue

                sensor_raw_df['sensor_id'] = sensor.id

                sensor_raw_df_timestep = (sensor_raw_df.index[1] - sensor_raw_df.index[0]).seconds

                # Write raw measures to UllageRawMeasurement
                sensor_raw_df.dropna(inplace=True)
                self.production_models.UllageRawMeasurement.write_df(
                    sensor_raw_df,
                    only_insert=True
                )

                high_alarm_columns = []
                low_alarm_columns = []

                for alarm_definition in sensor.alarm_definitions:
                    if alarm_definition.definition_valid_to == None: # We try only the actived alarm definitions
                        if alarm_definition.is_high_alarm:
                            high_alarm_columns.append(alarm_definition.name)
                            sensor_raw_df[alarm_definition.name] = (sensor_raw_df['value'] > alarm_definition.value)
                        else:
                            low_alarm_columns.append(alarm_definition.name)
                            sensor_raw_df[alarm_definition.name] = (sensor_raw_df['value'] < alarm_definition.value)


                # The AHH alarms with True values have to set the corresponding AH alarms to False value. 
                # The same for ALL and AL alarms.

                high_alarm_columns.reverse()
                low_alarm_columns.reverse()

                while len(high_alarm_columns) > 1:
                    test_column = high_alarm_columns.pop(0)
                    sensor_raw_df.loc[sensor_raw_df[test_column] == True, high_alarm_columns] = False

                while len(low_alarm_columns) > 1:
                    test_column = low_alarm_columns.pop(0)
                    sensor_raw_df.loc[sensor_raw_df[test_column] == True, low_alarm_columns] = False



                for alarm_definition in sensor.alarm_definitions:
                    for k, v in sensor_raw_df.groupby((sensor_raw_df[alarm_definition.name].shift() != sensor_raw_df[alarm_definition.name]).cumsum()):
                        if v[alarm_definition.name].iloc[0] == True:
                            sensor_alarm = self.production_models.PumpAlarmRecord(
                                alarm_definition_id = alarm_definition.id,
                                alarm_start = v.index[0].to_pydatetime(),
                                duration = len(v) * sensor_raw_df_timestep,
                                value = v['value'].mean()
                            )
                            session.add(sensor_alarm)

            session.flush()
            session.commit()

        # }}}
    

        