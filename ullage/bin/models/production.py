import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

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

from bin.models.base import BaseProduction as Base
from bin.models.base import production_engine as engine
from bin.models.base import reset_seconds_in_df_indexes
from bin.models import raw as raw_models


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


class UllageSensor(Base):
    # {{{

    __table__ = Table(
        "ullage_sensor",
        Base.metadata,
        autoload_with=engine,
    )
    __mapper_args__ = {
        'primary_key': [__table__.c.id]
    }
    alarm_definitions = relationship("UllageAlarmDefinition", back_populates="sensor")

    def get_raw_df(self, selected_date, fields_to_retrieve):
        # {{{
        dfs = []

        if 'kks' in fields_to_retrieve:
            flow_df = raw_models.KKSDescription.get_kks_df(
                self.kks.lower(),
                selected_date,
                column_name='value',
                index_name='timestamp'
            )

            dfs.append(flow_df)

        if len(dfs) > 0:
            df = pd.concat(dfs, axis=1)

            if 'id' in fields_to_retrieve:
                df['sensor_id'] = self.id
                # print(df)
            return df
        else:
            raise raw_models.NoKksData('generic_tag')
        # }}}

    # }}}


class UllageRawMeasurement(Base):
    # {{{

    __table__ = Table(
        "ullage_raw_measurement",
        Base.metadata,
        autoload_with=engine,
    )
    __mapper_args__ = {
        'primary_key': [__table__.c.id]
    }

    write_df_to_db_constraint = 'ullage_raw_measurement_pkey'
    write_df_to_db_constraint_fields = ['id']

    # }}}



class UllageAlarmDefinition(Base):
    # {{{

    __table__ = Table(
        "ullage_alarm_definition",
        Base.metadata,
        autoload_with=engine,
    )
    __mapper_args__ = {
        'primary_key': [__table__.c.id]
    }
    sensor = relationship("UllageSensor", back_populates="alarm_definitions")

    write_df_to_db_constraint = 'ullage_alarm_definition_pkey'
    write_df_to_db_constraint_fields = ['id']

    # }}}


class PumpAlarmRecord(Base):
    # {{{

    __table__ = Table(
        "ullage_alarm_record",
        Base.metadata,
        autoload_with=engine,
    )
    __mapper_args__ = {
        'primary_key': [__table__.c.id]
    }

    write_df_to_db_constraint = 'ullage_operation_pkey'
    write_df_to_db_constraint_fields = ['id']

    # }}}
