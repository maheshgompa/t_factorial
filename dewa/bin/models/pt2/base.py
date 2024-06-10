import sqlalchemy

from sqlalchemy.orm import DeclarativeBase

from config.pt2.config import RAW_DATABASE_CONNECTION, PRODUCTION_DATABASE_CONNECTION

production_engine = sqlalchemy.create_engine(
    'postgresql://%s:%s@localhost:5432/%s' % (
        PRODUCTION_DATABASE_CONNECTION.get('user'), 
        PRODUCTION_DATABASE_CONNECTION.get('password'), 
        PRODUCTION_DATABASE_CONNECTION.get('database')
    ),
    connect_args={"options": "-c timezone=utc"},
    echo=False
)

raw_engine = sqlalchemy.create_engine(
    'postgresql://%s:%s@localhost:5432/%s' % (
        RAW_DATABASE_CONNECTION.get('user'), 
        RAW_DATABASE_CONNECTION.get('password'), 
        RAW_DATABASE_CONNECTION.get('database')
        #'nomac_dewa_pt2_raw_2'
    ),
    connect_args={"options": "-c timezone=utc"},
    echo=False
)


def reset_seconds_in_df_indexes(df):
    # {{{
    """
    Sometime the data is ingested with a time seconds part distinct than zero.
    We need to set thats time seconds to zero.
    But only when all indexes have the same seconds and that values is not zero.
    """

    if len(set(df.index.second.to_list())) == 1 and df.index.second[0] > 0:
        df.index = df.index.floor('Min')

    return df
    # }}}


class Common():
    @classmethod
    def get_engine(cls):
        # {{{
        
        if cls.__module__ == 'models.pt2.production':
            return production_engine
        elif cls.__module__ == 'models.pt2.raw':
            return raw_engine

        # }}}

    @classmethod
    def write_df(cls, df, only_insert=True, index=True):
        # {{{

        def create_upsert_method(only_insert, constraint, constraint_fields):
            def upsert_method(table, conn, keys, data_iter):
                # {{{
                
                # NOTE: some table field has a \ character. This character create an error
                # when used as parameter name. So, we need to do some cleaning before.
                fixed_keys = [i.replace('_from_/to_', '_from_to_') for i in keys]



                # update_fields would be the df columns with the constraint_fields removed.
                update_fields = list(set(keys) - set(constraint_fields))


                if only_insert:
                    sql = """
                        INSERT INTO "%s" (%s)
                        VALUES(%s) 
                        ON CONFLICT ON CONSTRAINT %s
                        DO NOTHING;
                    """ % (
                            table.name, 
                            ', '.join(keys), 
                            ', '.join([':%s' % i for i in keys]), 
                            constraint
                        )
                else:
                    sql = """
                        INSERT INTO "%s" (%s)
                        VALUES(%s) 
                        ON CONFLICT ON CONSTRAINT %s
                        DO
                           UPDATE SET %s;
                    """ % (
                            table.name, 
                            ', '.join(['"%s"' % i for i in keys]), 
                            ', '.join([':%s' % i for i in fixed_keys]), 
                            constraint,
                            ', '.join(['"%s" = :%s' % (i, i.replace('_from_/to_', '_from_to_')) for i in update_fields])
                        )

                value_list = []
                for i in data_iter:
                    value_list.append(dict(zip([i.replace('_from_/to_', '_from_to_') for i in keys],i)))

                try:
                    conn.execute(
                        sqlalchemy.text(sql),
                        value_list
                    )
                except Exception as e:
                    # import ipdb; ipdb.set_trace()
                    raise Exception('Error writing data to table %s' % table.name)

                # }}}
            return upsert_method

        # We need to create a cloesure to past additional variables to the function.
        upsert_method = create_upsert_method(
            only_insert=only_insert, 
            constraint=cls.write_df_to_db_constraint, 
            constraint_fields=cls.write_df_to_db_constraint_fields
        )

        df.to_sql(
            cls.__table__.name,
            cls.get_engine(),
            if_exists='append', 
            index=index,
            chunksize=200, # it's recommended to insert data in chunks
            method=upsert_method
        )

        # }}}


class BaseProduction(DeclarativeBase, Common):
    pass

class BaseRaw(DeclarativeBase, Common):
    pass
