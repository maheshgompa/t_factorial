import pandas as pd

from sqlalchemy import Table, select, text
from sqlalchemy.orm import Session
from datetime import datetime

from models.base import BaseRaw as Base
from models.base import raw_engine as engine



class NoKksData(Exception):
    "Raised when there is not kks defined or it has no data"

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
        'primary_key':[__table__.c.id]
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
    def get_kks_df(cls, kks, date, column_name=None, index_name=None, resample_to=None, truncate_seconds=False, requested_timestep=None):
        # {{{

        initial_date, timestep, kks_values = cls.get_kks_values(kks, date, requested_timestep)

        if truncate_seconds:
            initial_date = initial_date.replace(second=0)

        df = pd.DataFrame(
            kks_values,
            columns = [column_name if column_name else kks.lower()],
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

        return df

        # }}}

    @classmethod
    def get_kkses_df(cls, kkses_definitions, date, index_name=None):
        # {{{

        dfs = [] # We vill add all df retrieve here in this list.

        for kks_name, column_name in kkses_definitions:
            df = cls.get_kks_df(kks_name, date, column_name=column_name, index_name=index_name)
            dfs.append(df)

        if len(dfs) > 0:
            final_df = pd.concat(dfs, axis=1)

        # Mask to be sure only data from the selected date is taken
        # date_window_mask = (dni_df.index >= selected_date.replace(hour=0, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")) & (dni_df.index <= selected_date.replace(hour=23, minute=59, second=59).strftime("%Y-%m-%d %H:%M:%S"))

            return final_df

        # }}}

    @classmethod
    def get_kkss(cls):
        # {{{

        with engine.connect() as conn:
            data_kks = conn.execute(
                text("SELECT distinct kks FROM kks_description")).scalars().all()

            ls = []
            for row in data_kks:
                ls.append((row, None))
            return ls

        # }}}


    # }}}

# class AllDownloadedKKSes(Base):
#     # {{{
#
#     __table__ = Table(
#         "all_downloaded_kkses",
#         Base.metadata,
#         autoload_with=engine,
#     )
#     __mapper_args__ = {
#         'primary_key':[__table__.c.id]
#     }
#
#     write_df_to_db_constraint = 'all_downloaded_kkses_un'
#     write_df_to_db_constraint_fields = ['kks']
#
#     # }}}

"""
# SQL to get the kks tables not created:
# -------------------------------------

select k.kks, k.table_name 
from kks_description k
left join information_schema.tables i ON i.table_schema='public' and i.table_type='BASE TABLE' and i.table_name = k.table_name 
where i.table_name is null;


# SQL to get a create-table statement for every table_name missing:
# -----------------------------------------------------------------

SELECT
	concat('CREATE TABLE "', a.table_name, '" (id serial4 NOT NULL, "date" timestamp NOT NULL, value _float4 NOT NULL, CONSTRAINT "', a.table_name, '_pk" PRIMARY KEY (id), CONSTRAINT "', a.table_name, '_un" UNIQUE (date));')
FROM (
	SELECT
		k.table_name AS table_name
	FROM
		kks_description k
	LEFT JOIN information_schema.tables i ON i.table_schema = 'public'
		AND i.table_type = 'BASE TABLE'
		AND i.table_name = k.table_name
    WHERE
        i.table_name IS NULL
) a;


# SQL to create a kks table:
# -------------------------

CREATE TABLE "t_10wsn20at001" (
    id serial4 NOT NULL,
    "date" timestamp NOT NULL,
    value _float4 NOT NULL,
    CONSTRAINT "t_10wsn20at001_pk" PRIMARY KEY (id),
    CONSTRAINT "t_10wsn20at001_un" UNIQUE (date)
);


# To list all tables in the database:
# -----------------------------------

SELECT table_name
  FROM information_schema.tables
 WHERE table_schema='public'
   AND table_type='BASE TABLE';


# To create new entries in the kks_description using data from the production database
# ------------------------------------------------------------------------------------

nomac_dewa_pt1_raw=# CREATE EXTENSION dblink;
CREATE EXTENSION

nomac_dewa_pt1_raw=# SELECT * FROM dblink('dbname=nomac_dewa_pt1', 'select distinct temperature_sensor from sca_sensors') AS t1(kks text);

To check for all temperature_sensor in the all_downloaded_kkses table:

SELECT
    t1.kks,
    a.kks,
    a.description
FROM 
    dblink('dbname=nomac_dewa_pt1', 'select distinct temperature_sensor from sca_sensors') AS t1(kks text)
    left join all_downloaded_kkses a on lower(t1.kks) = lower(a.kks)
WHERE
    a.kks is null
;

To check for all temperature_sensor in the kks_description table:

SELECT
    t1.kks,
    a.kks,
    a.description
FROM 
    dblink('dbname=nomac_dewa_pt1', 'select distinct temperature_sensor from sca_sensors') AS t1(kks text)
    left join kks_description a on lower(t1.kks) = lower(a.kks)
WHERE
    a.kks is not null
;


To create the new entries in the kks_description table using all_downloaded_kkses:

INSERT INTO "kks_description" ("kks", "file", "timestep", "description", "table_name")
SELECT
    lower(a.kks),
    a.file,
    60,
    a.description,
    concat('t_', lower(a.kks))
FROM 
    dblink('dbname=nomac_dewa_pt1', 'select distinct temperature_sensor from sca_sensors') AS t1(kks text)
    left join all_downloaded_kkses a on lower(t1.kks) = lower(a.kks)
WHERE
    a.kks is not null
;



"""
