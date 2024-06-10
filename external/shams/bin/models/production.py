import pandas as pd
import suncalc
import math
import datetime
import matplotlib.pyplot as plt
import numpy as np

from typing import List
from typing import Optional
from sqlalchemy import Table, select, func
from sqlalchemy.orm import Session, relationship, Mapped

from models.base import BaseProduction as Base
from models.base import production_engine as engine
from models.base import reset_seconds_in_df_indexes
from models import raw as raw_models


# Ullage module
# --------------------------------------

class UllageOperation(Base):
    # {{{

    __table__ = Table(
        "ullage_operation",
        Base.metadata,
        autoload_with=engine,
    )
    __mapper_args__ = {
        'primary_key': [__table__.c.timestamp]
    }

    write_df_to_db_constraint = 'ullage_operation_pkey'
    write_df_to_db_constraint_fields = ['timestamp']

    # }}}








# Solar Field Definitions
# --------------------------------------

# class Sector(Base):
#     # {{{
#     __table__ = Table(
#         "sector_sensors",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.sector_id]
#     }
#
#     subfields = relationship("Subfield")
#
#     def get_raw_df(self, selected_date, fields_to_retrieve):
#         # {{{
#
#         dfs = [] # We vill add all df retrieve here in this list.
#
#         if 'flow' in fields_to_retrieve:
#             flow_df = raw_models.KKSDescription.get_kks_df(
#                 self.flow.lower(),
#                 selected_date,
#                 column_name='flow',
#                 index_name='timestamp'
#             )
#
#             dfs.append(flow_df)
#
#         if 'temp_in_01' in fields_to_retrieve:
#             temp_in_01_df = raw_models.KKSDescription.get_kks_df(
#                 self.temp_in_01.lower(),
#                 selected_date,
#                 column_name='temp_in_01',
#                 index_name='timestamp'
#             )
#
#             dfs.append(temp_in_01_df)
#
#         if 'temp_in_02' in fields_to_retrieve:
#             temp_in_02_df = raw_models.KKSDescription.get_kks_df(
#                 self.temp_in_02.lower(),
#                 selected_date,
#                 column_name='temp_in_02',
#                 index_name='timestamp'
#             )
#
#             dfs.append(temp_in_02_df)
#
#         if 'temp_out_01' in fields_to_retrieve:
#             temp_out_01_df = raw_models.KKSDescription.get_kks_df(
#                 self.temp_out_01.lower(),
#                 selected_date,
#                 column_name='temp_out_01',
#                 index_name='timestamp'
#             )
#
#             dfs.append(temp_out_01_df)
#
#         if 'temp_out_02' in fields_to_retrieve:
#             temp_out_02_df = raw_models.KKSDescription.get_kks_df(
#                 self.temp_out_02.lower(),
#                 selected_date,
#                 column_name='temp_out_02',
#                 index_name='timestamp'
#             )
#
#             dfs.append(temp_out_02_df)
#
#
#         if len(dfs) > 0:
#
#             sector_df = pd.concat(dfs, axis=1)
#
#             if 'sector_id' in fields_to_retrieve:
#                 sector_df['sector_id'] = self.sector_id
#
#             return sector_df
#
#         else:
#             raise raw_models.NoKksData('generic_tag')
#
#         # }}}
#
#     # }}}
#
# class Subfield(Base):
#     # {{{
#
#     __table__ = Table(
#         "subfield_sensors",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.subfield_id]
#     }
#
#     sector = relationship("Sector", back_populates="subfields")
#     scas = relationship("SCA")
#     loops = relationship("Loop")
#
#     def get_raw_df(self, selected_date, fields_to_retrieve):
#         # {{{
#
#         dfs = []
#
#         if 'flow' in fields_to_retrieve:
#             flow_df = raw_models.KKSDescription.get_kks_df(
#                 self.flow_sensor.lower(),
#                 selected_date,
#                 column_name='flow',
#                 index_name='timestamp'
#             )
#
#             dfs.append(flow_df)
#
#         if 'temp_in' in fields_to_retrieve:
#             temp_in_df = raw_models.KKSDescription.get_kks_df(
#                 self.temp_in_sensor.lower(),
#                 selected_date,
#                 column_name='temperature_in',
#                 index_name='timestamp'
#             )
#
#             dfs.append(temp_in_df)
#
#         if 'temp_out' in fields_to_retrieve:
#             temp_out_df = raw_models.KKSDescription.get_kks_df(
#                 self.temp_out_sensor.lower(),
#                 selected_date,
#                 column_name='temperature_out',
#                 index_name='timestamp'
#             )
#
#             dfs.append(temp_out_df)
#
#         if len(dfs) > 0:
#             df = pd.concat(dfs, axis=1)
#
#             if 'subfield_id' in fields_to_retrieve:
#                 df['subfield_id'] = self.subfield_id
#
#             return df
#         else:
#             raise raw_models.NoKksData('generic_tag')
#         # }}}
#
#     # }}}
#
# class SubfieldMeasurement(Base):
#     # {{{
#
#     __table__ = Table(
#         "subfield_measurements",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.subfield_id]
#     }
#
#     write_df_to_db_constraint = 'subfield_measurements_pkey'
#     write_df_to_db_constraint_fields = ['timestamp', 'subfield_id']
#
#     # }}}
#
# class Loop(Base):
#     # {{{
#
#     __table__ = Table(
#         "loop_sensors",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.loop_id]
#     }
#
#     scas = relationship("SCA")
#
#     def get_raw_df(self, selected_date, fields_to_retrieve, requested_timestep=None):
#         # {{{
#
#         dfs = [] # We vill add all df retrieve here in this list.
#
#         for sca in self.scas:
#             for i in range(1,5):
#                 if sca.sca_position == i and 'sca_%s_temperature' % i in fields_to_retrieve:
#                     sca_df = sca.get_raw_df(selected_date, ['temperature'])
#                     sca_df.rename({'temperature': 'sca_%s_temperature' % i}, axis=1, inplace=True)
#                     dfs.append(sca_df)
#
#                 if sca.sca_position == i and 'sca_%s_mode' % i in fields_to_retrieve:
#                     # DEWA is not sharing the MODE tags. We do this trick.
#                     sca_df = sca.get_raw_df(selected_date, ['temperature'])
#                     sca_df.rename({'temperature': 'sca_%s_mode' % i}, axis=1, inplace=True)
#                     sca_df['sca_%s_mode' % i] = 0
#                     dfs.append(sca_df)
#
#         if 'temp_out' in fields_to_retrieve:
#             temp_out_df = raw_models.KKSDescription.get_kks_df(
#                 self.temp_out_sensor.lower(),
#                 selected_date,
#                 column_name='temp_out',
#                 index_name='timestamp',
#                 requested_timestep=requested_timestep
#             )
#
#             temp_out_df = reset_seconds_in_df_indexes(temp_out_df)
#             dfs.append(temp_out_df)
#
#         if len(dfs) > 0:
#             loop_df = pd.concat(dfs, axis=1)
#
#             for i in range(1,5):
#                 if 'sca_%s_id' % i in fields_to_retrieve:
#                     loop_df['sca_%s_id' % i] = self.get_sca_by_position(i).sca_id
#
#             return loop_df
#         else:
#             raise raw_models.NoKksData('generic_tag')
#
#         # }}}
#
#     def get_sca_by_position(self, position):
#         # {{{
#
#         for sca in self.scas:
#             if sca.sca_position == position:
#                 return sca
#         raise raw_models.NoKksData('generic_tag')
#
#         # }}}
#
#     # }}}
#
# class SCA(Base):
#     # {{{
#
#     __table__ = Table(
#         "sca_sensors",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.sca_id]
#     }
#
#     subfield = relationship("Subfield", back_populates="scas")
#
#     def get_raw_df(self, selected_date, fields_to_retrieve, requested_timestep=None):
#         # {{{
#
#         dfs = [] # We vill add all df retrieve here in this list.
#
#         if 'temperature' in fields_to_retrieve:
#             temperature_df = raw_models.KKSDescription.get_kks_df(
#                 self.temperature_sensor.lower(),
#                 selected_date,
#                 column_name='temperature',
#                 index_name='timestamp',
#                 requested_timestep=requested_timestep
#             )
#
#             temperature_df = reset_seconds_in_df_indexes(temperature_df)
#             dfs.append(temperature_df)
#
#         if 'position' in fields_to_retrieve:
#             position_df = raw_models.KKSDescription.get_kks_df(
#                 self.position_sensor.lower(),
#                 selected_date,
#                 column_name='position',
#                 index_name='timestamp',
#                 requested_timestep=requested_timestep
#             )
#
#             position_df = reset_seconds_in_df_indexes(position_df)
#             position_df['position'] = 90 - position_df['position']
#
#             dfs.append(position_df)
#
#         if 'sun':
#             # DEWA doesn't give us this data
#             pass
#
#         if len(dfs) > 0:
#
#             sca_df = pd.concat(dfs, axis=1)
#
#
#             if 'theoretical_sun' in fields_to_retrieve:
#                 sun_calculator = SunCalculator()
#
#                 # We need to align the calculated sun with the real one.
#                 # We will request the calculated sun an hour before and after the current pediod.
#                 # We will need this data in a timestep of 1 sec.
#
#                 period = pd.date_range(
#                     start=sca_df.index[0].to_pydatetime() - datetime.timedelta(hours=1),
#                     end=sca_df.index[len(sca_df) - 1].to_pydatetime() + datetime.timedelta(hours=1),
#                     freq='1s'
#                 )
#
#                 sun_df = sun_calculator.get_df(
#                     period - pd.Timedelta(hours=4), # We need to subtract 4 hour from the local time to get the UTC time.
#                     latitude=self.latitude, #24.75806,
#                     longitude=self.longitude, #55.46162,
#                     refraction=True,
#                     desviation_azimuth=self.azimuth_desviation * 3.1415926535/180,
#                     desviation_elevation=self.elevation_desviation * 3.1415926535/180
#                 )
#
#                 sun_df.index = sun_df.index + pd.Timedelta(hours=4) # Convert again to localtime.
#                 mask = (sca_df.position > 70) & (sca_df.position < 110)
#
#                 # We are going to offset some seconds and calculate the mean of all diff
#                 # The aim is to minimize this diff mean to find the right alignement.
#
#                 offsets = [90, 300, 600]
#                 for initial_offset in offsets:
#                     iterations = {}
#                     for offset in range(-initial_offset, initial_offset, 1):
#                         sca_df['theoretical_sun'] = sun_df['sun_angle'].shift(periods=offset)
#                         sca_df['diff'] = sca_df['position'] - sca_df['theoretical_sun']
#                         iterations[offset] = sca_df['diff'][mask & (sca_df['diff'].abs() < 2)].mean()
#
#                     iterations_df = pd.DataFrame(data=iterations.values(), index=iterations.keys(), columns=['diff'])
#                     iterations_df.dropna(inplace=True)
#
#                     if iterations_df['diff'].abs().min() < 0.005:
#                         best_offset = iterations_df[iterations_df['diff'].abs() == iterations_df.abs().min()['diff']].index[0]
#                         sca_df['theoretical_sun'] = sun_df['sun_angle'].shift(periods=best_offset)
#                         break
#                     elif initial_offset == offsets[-1]: # We are in the last iteration
#                         sca_df['theoretical_sun'] = sun_df['sun_angle'] # Use the default align
#
#                 sca_df.drop('diff', axis=1, inplace=True)
#
#
#             if 'sca_id' in fields_to_retrieve:
#                 sca_df['sca_id'] = self.sca_id
#
#             if 'mode' in fields_to_retrieve:
#                 sca_df['mode'] = 5
#
#             return sca_df
#
#         else:
#             raise raw_models.NoKksData('generic_tag')
#
#         # }}}
#
#     # }}}
#
# class SCAMeasurement(Base):
#     # {{{
#
#     __table__ = Table(
#         "sca_measurements",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.id]
#     }
#
#     write_df_to_db_constraint = 'sca_measurements_un'
#     write_df_to_db_constraint_fields = ['timestamp', 'sca_id']
#
#     # }}}
#
# class SFHTFRawMeasurement(Base):
#     # {{{
#
#     __table__ = Table(
#         "sf_htf_raw_measurements",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.id]
#     }
#
#     write_df_to_db_constraint = 'sf_htf_raw_measurements_un'
#     write_df_to_db_constraint_fields = ['timestamp']
#
#     # }}}
#
#
# # Solar Field Variables
# # --------------------------------------
#
# class DNIMeasurement(Base):
#     # {{{
#
#     __table__ = Table(
#         "dni_measurements",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.dni_id]
#     }
#
#     @classmethod
#     def get_df(cls, selected_date):
#         # {{{
#
#         df = pd.read_sql(
#             select(cls).where(cls.dni_id == 1, cls.timestamp >= selected_date.replace(hour=0, minute=0, second=0), cls.timestamp <= selected_date.replace(hour=23, minute=59, second=59)).order_by(cls.timestamp),
#             con=engine.connect(),
#             index_col='timestamp'
#         )
#
#         if len(df) > 0:
#             return df
#         else:
#             raise raw_models.NoKksData('generic_tag')
#
#         # }}}
#
#     # }}}
#
# class DNIFinalMeasurement(Base):
#     # {{{
#
#     __table__ = Table(
#         "dni_final_measurements",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.id]
#     }
#
#     write_df_to_db_constraint = 'dni_final_measurements_un'
#     write_df_to_db_constraint_fields = ['timestamp']
#
#     # }}}
#
# class SunPosition(Base):
#     # {{{
#
#     __table__ = Table(
#         "sun_position",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.id]
#     }
#
#     # }}}
#
#
# # Temperature increase shortfall
# #---------------------------------------------------
#
# class TemperatureDTSCASTest(Base):
#     # {{{
#
#     __table__ = Table(
#         "temperature_dt_scas_test",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.id]
#     }
#
#     # }}}
#
# class TemperatureDTSCASDaily(Base):
#     # {{{
#
#     __table__ = Table(
#         "temperature_dt_scas_daily",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.id]
#     }
#
#     write_df_to_db_constraint = 'temperature_dt_scas_daily_un'
#     write_df_to_db_constraint_fields = ['test_id', 'loop_id']
#
#     # }}}
#
# class TemperatureDTSCASAlarm(Base):
#     # {{{
#
#     __table__ = Table(
#         "temperature_dt_scas_alarms",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.id]
#     }
#
#     write_df_to_db_constraint = 'temperature_dt_scas_alarms_un'
#     write_df_to_db_constraint_fields = ['test_id', 'loop_id', 'sca_id']
#
#     # }}}
#
# class TemperatureDTSCASAvg(Base):
#     # {{{
#
#     __table__ = Table(
#         "temperature_dt_scas_avg",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.id]
#     }
#
#     write_df_to_db_constraint = 'temperature_dt_scas_avg_un'
#     write_df_to_db_constraint_fields = ['test_id', 'subfield_id']
#
#     # }}}
#
