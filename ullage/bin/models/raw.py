import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
from sqlalchemy import Table, select, text
from sqlalchemy.orm import Session
from datetime import datetime

from bin.models.base import BaseRaw as Base
from bin.models.base import raw_engine as engine


class NoKksData(Exception):
    """Raised when there is not kks defined or it has no data"""

    def __init__(self, tag_name, message="Tag not found in kks_description"):
        self.tag_name = tag_name
        self.message = message
        super().__init__(self.message)


class KKSDescription(Base):
    # {{{

    __table__ = Table(
        "kks_description",
        Base.metadata,
        autoload_with=engine,
    )
    __mapper_args__ = {
        'primary_key': [__table__.c.id]
    }

    @classmethod
    def get_kks_description(cls, kks):
        # {{{

        stmt = select(cls).where(cls.kks == kks)

        with Session(engine) as session:
            for kks_description in session.scalars(stmt):
                return kks_description

        raise NoKksData(kks)
        # }}}

    @classmethod
    def get_kks_values(cls, kks, date, requested_timestep=None):
        # {{{

        kks_description = cls.get_kks_description(kks)

        with engine.connect() as conn:

            # We can have several records for this date. Every record with a timestep value.
            # So we have to decide which one to use.

            timesteps = conn.execute(
                text(
                    """SELECT distinct timestep FROM "%s" WHERE date_trunc('day', date) = :date order by timestep ASC"""
                    % kks_description.table_name
                ),
                {"date": date.strftime("%Y-%m-%d")}
            ).scalars().all()

            if len(timesteps) == 0:
                raise NoKksData(kks)
            elif len(timesteps) == 1:
                selected_timestep = timesteps[0]
            else:
                # We have to decide which timestep use:
                #  - The requested_timestep passed will by use if exits.
                #  - If no requested_timestep is passed. The min timestep will be use.
                if requested_timestep and requested_timestep in timesteps:
                    selected_timestep = requested_timestep
                else:
                    selected_timestep = timesteps[0]

            query = """SELECT date, timestep, value FROM "%s" WHERE date_trunc('day', date) = :date and timestep = :timestep""" % kks_description.table_name

            result = conn.execute(
                text(query),
                {"date": date.strftime("%Y-%m-%d"), "timestep": selected_timestep},
            )

            for row in result:
                return row[0], row[1], row[2]

        raise NoKksData(kks)

        # }}}

    @classmethod
    def get_kks_df(cls, kks, date, column_name=None, index_name=None, resample_to=None, truncate_seconds=False,
                   requested_timestep=None):
        # {{{

        initial_date, timestep, kks_values = cls.get_kks_values(kks, date, requested_timestep)

        if truncate_seconds:
            initial_date = initial_date.replace(second=0)

        df = pd.DataFrame(
            kks_values,
            columns=[column_name if column_name else kks.lower()],
            index=pd.date_range(
                start=initial_date,
                periods=len(kks_values),
                freq="%sS" % timestep,
                tz="UTC"
            )
        )

        if resample_to and resample_to != timestep:
            df = df.resample(str(resample_to) + "S").ffill()

        if index_name:
            df.rename_axis(index_name, axis=0, inplace=True)
        print("create df from raw db in get_kks_df classmethod for kks_description class: ",df)
        print()
        return df
        # }}}

    @classmethod
    def get_kkses_df(cls, kkses_definitions, date, index_name=None):
        # {{{

        dfs = []  # We vill add all df retrieve here in this list.

        for kks_name, column_name in kkses_definitions:
            df = cls.get_kks_df(kks_name, date, column_name=column_name, index_name=index_name)
            # print(df)
            dfs.append(df)

        if len(dfs) > 0:
            final_df = pd.concat(dfs, axis=1)

            # Mask to be sure only data from the selected date is taken
            # date_window_mask = (dni_df.index >= selected_date.replace(hour=0, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")) & (dni_df.index <= selected_date.replace(hour=23, minute=59, second=59).strftime("%Y-%m-%d %H:%M:%S"))
            print("final df from raw db in get_kkses_df classmethod for kks_description class: ",final_df)


            return final_df


# }}}

# # Sample Output for KKSDescription Class Sequences
# kks_description = KKSDescription.get_kks_description('r1qja10aa001')
# print(kks_description)
# # Output: <bin.models.raw.KKSDescription object at 0x000002448703CF50>

# initial_date, timestep, kks_values = KKSDescription.get_kks_values('r1qja10aa001', datetime(2024, 2, 4))
# print(initial_date, timestep, kks_values)
# # Output: 2024-02-04 08:00:00+00:00 10 [58.362930, 16.950370, ...]

# df = KKSDescription.get_kks_df('r1qja10aa001', datetime(2024, 2, 4))
# print(df)
# # Output: DataFrame with KKS values for 'r1qja10aa001'

# final_df = KKSDescription.get_kkses_df([('r1qja10aa001', 'column1'), ('r1qja12aa001', 'column2')], datetime(2024, 2, 4))
# print(final_df)
# # Output: DataFrame with multiple KKS values


