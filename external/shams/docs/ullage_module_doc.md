# Module description

## Tanks Levels

The goal is to record the `HTF Condensate Tank` levels (in Volume (m3) and mass (tn)).

### KKSes:

- R1QJA80CL001: HTF Condensate Tank Level
- R1QJA80CT001: HTF Condensate Tank Temperature


### Calculations:

Volume [m3] = R1QJA80CL001 * 6,0 m3

Mass volume [tn] = (Volumen [m3] * HTF density(R1QJA80CT001)) / 1000 

Where HTF density(Temp):

HTF density(Temp) [Kg/m3] = 1065.05375654492 - 0.595426707667444 * Temp - 0.000893338489101383 * (Temp ** 2)

NOTE: This should be data taken only once a day, following the same criteria as the HTF Inventory KPI.

TODO: When do we get the measure?



## Temperature follow up

The aims is to evaluate and monitor the temperatures recorded in the system, in order to determine the correct functioning of the HTF recovery systems.

Temperatures will be monitored whenever the system is in operation. 

### KKSes:

- R1QJA78CT001: Inlet temperature HTF Exchanger 
- R1QJA78CT002: Outlet temperature HTF Exchanger 
- R1QJA82CT001: Inlet temperature AC Filter 
- R1QJA80CT001: HTF Condensate Tank temperature 

The system has 2 high temperature trips:

- R1QJA10AA001: System inlet high temperature trip
- R1QJA12AA001: Carbon filter inlet high temperature trip



## VOC values

The main objective of this submodule is to know the values of emissions into the atmosphere once the gases have passed through the active carbon filter.

### KKSes:

- R1QJA82CQ001: Active carbon filter analyzer



## Recovered mass

The objective is to evaluate the mass returned to the main oil system, associated with the KPI HTF Inventory.

### KKSes:

- R1JE_40CF001: Ullage pumps flow
- R1QJA80CT001: HTF Condensate Tank Temperature

### Calculations:

Flow [m3/h] = R1JE_40CF001

Recovered mass [tn] = Flow * HTF density(R1QJA80CT001) * Time

Where HTF density(Temp):

HTF density(Temp) = 1065.05375654492 - 0.595426707667444 * Temp - 0.000893338489101383 * (Temp ** 2)



## CA Filter Weight 

The objective is to define the evolution of the saturation of the active carbon filters and proceed with their change once the benzene absorption is saturated. 

SHAMS does not have a weight transmitter to count the weight of the activated carbon. The saturation of the filter is determined based on the specifications of the activated carbon supplier, the differential pressure and the gas meter.

### KKSes:

- R1QJA82CP001: Active carbon filter inlet pressure
- R1QJA82CP002: Active carbon filter inlet pressure
- R1QJA82CP003: Active carbon filter differential pressure


## Alarms

The objective is to replicate the significant alarms of the system to count the number of alarms and be able to determine if there is any malfunction of the system or any specific equipment.


| Signal        | Description                                | LL     | L      | H       | HH      |
|---------------|--------------------------------------------|--------|--------|---------|---------|
| R1QJA78CT001  | Vent stream temperature                    | -      | -      | 307 ºC  | 350 ºC  |
| R1QJA78CT002  | Ullage condenser temperature               | -      | -      | 307 ºC  | -       |
| R1PGB18CT001  | Exchanger water supply temperature         | -      | -      | 60 ºC   | -       |
| R1PGB31CT001  | Exchanger water return temperature         | -      | -      | 100 ºC  | -       |
| R1QJA80CT001  | Separator tank temperature                 | -      | -      | 65 ºC   | -       |
| R1QJA82CT001  | Active carbon filter inlet temperature     | -      | -      | 65 ºC   | -       |
| R1QJA78CP001  | Vent stream pressure                       | -      | -      | 12 bar  | 13 bar  |
| R1PGB18CP001  | Exchanger water supply pressure            | -      | -      | 8 bar   | -       |
| R1PGB31CP001  | Exchanger water return pressure            | -      | -      | 8 bar   | -       |
| R1QJA80CP001  | Separator tank pressure                    | -      | 10 bar | 12 bar  | -       |
| R1QJA82CP001  | Active carbon filter inlet pressure        | -      | -      | 12 bar  | -       |
| R1QJA82CP002  | Active carbon filter inlet pressure        | -      | -      | 1,5 bar | 2,0 bar |
| R1QJA82CP003  | Active carbon filter differential pressure | -      | -      | TBD     | TBD     |
| R1JE_96CP001  | Discharge pressure pump 96                 | 10 bar | 12 bar | -       | -       |
| R1JE_98CP001  | Discharge pressure pump 98                 | 10 bar | 12 bar | -       | -       |
| R1QJA80 CL001 | HTF tank level                             | -      | 17%    | 67%     | 100%    |
| R1QJA82CQ001  | Active carbon filter analyzer              | -      | -      | TBD     | TBD     |



# Some ideas for data management.


## Table: ullage_sensor


| kks           | Description                                | ID     |
|---------------|--------------------------------------------|--------|
| R1QJA78CT001  | Vent stream temperature                    | 1      |
| R1QJA78CT002  | Ullage condenser temperature               | 2      |
| R1PGB18CT001  | Exchanger water supply temperature         | 3      |
| R1PGB31CT001  | Exchanger water return temperature         | 4      |
| R1QJA80CT001  | Separator tank temperature                 | 5      |
| R1QJA82CT001  | Active carbon filter inlet temperature     | 6      |
| R1QJA78CP001  | Vent stream pressure                       | 7      |
| R1PGB18CP001  | Exchanger water supply pressure            | 8      |
| R1PGB31CP001  | Exchanger water return pressure            | 9      |
| R1QJA80CP001  | Separator tank pressure                    | 10     |
| R1QJA82CP001  | Active carbon filter inlet pressure        | 11     |
| R1QJA82CP002  | Active carbon filter inlet pressure        | 12     |
| R1QJA82CP003  | Active carbon filter differential pressure | 13     |
| R1JE_96CP001  | Discharge pressure pump 96                 | 14     |
| R1JE_98CP001  | Discharge pressure pump 98                 | 15     |
| R1QJA80 CL001 | HTF tank level                             | 16     |
| R1QJA82CQ001  | Active carbon filter analyzer              | 17     |


## Table: ullage_raw_measurement


| id     | timestamp              | value     | sensor_id |
|--------|------------------------|-----------|-----------|
| 416215 | 2024-01-29 06:01:00+01 | 0.0307436 |         1 |
| 416216 | 2024-01-29 06:02:00+01 | 0.0307436 |         1 |
| 416217 | 2024-01-29 06:03:00+01 | 0.0307436 |         1 |
| 416218 | 2024-01-29 06:04:00+01 | 0.0307436 |         1 |
| 416219 | 2024-01-29 06:05:00+01 | 0.0298394 |         1 |
| 416220 | 2024-01-29 06:06:00+01 | 0.0298394 |         1 |


## Table: ullage_alarm_definition

| id | definition_valid_from  | definition_valid_to | name | unit | value | sensor_id | order | is_high_alarm |
|----|------------------------|---------------------|------|------|-------|-----------|-------|---------------|
|  1 | 2024-01-01 01:00:00+01 |                     | H    | ºC   |   307 |         1 |     1 | t             |
|  2 | 2024-01-01 01:00:00+01 |                     | HH   | ºC   |   350 |         1 |     2 | t             |
|  3 | 2024-01-01 01:00:00+01 |                     | H    | ºC   |   307 |         2 |     1 | t             |

## Table: ullage_alarm_record

| id  | alarm_start            | duration | value     | alarm_definition_id |
|-----|------------------------|----------|-----------|---------------------|
| 564 | 2024-01-29 13:21:00+01 |       60 | 343.52777 |                 390 |
| 565 | 2024-01-29 13:42:00+01 |       60 | 343.66827 |                 390 |
| 566 | 2024-01-29 14:27:00+01 |       60 |  344.6519 |                 390 |
| 567 | 2024-01-29 14:44:00+01 |      120 | 343.57794 |                 390 |
| 568 | 2024-01-29 14:51:00+01 |      120 | 343.68835 |                 390 |
| 569 | 2024-01-29 14:55:00+01 |       60 | 344.61176 |                 390 |
| 570 | 2024-01-29 15:24:00+01 |       60 | 344.77234 |                 390 |
| 571 | 2024-01-29 15:35:00+01 |      240 |  343.6181 |                 390 |


# Related module

You can use this module as template:

```

class Pumps():

    def __init__(self):
        # {{{

        self.raw_models = raw_models
        self.production_models = production_models

        # }}}

    def process(self, selected_date, update_database=True):
        # {{{

        self.write_raw_measures_and_set_alarms(selected_date)
        self.calculate_pump_regimen(selected_date)

        # }}}

    def write_raw_measures_and_set_alarms(self, selected_date):
        # {{{

        dfs = []
        with Session(self.production_models.engine) as session:
            for sensor in session.scalars(select(self.production_models.PumpSensor)):

                try:
                    sensor_raw_df = sensor.get_raw_df(selected_date)
                except self.raw_models.NoKksData:
                    #self.missing_kkses.append(kks1)
                    print('Missing kks: %s' % sensor.kks)
                    continue

                sensor_raw_df['sensor_id'] = sensor.id

                sensor_raw_df_timestep = (sensor_raw_df.index[1] - sensor_raw_df.index[0]).seconds

                # Write raw measures to PumpRawMeasurement
                sensor_raw_df.dropna(inplace=True)
                self.production_models.PumpRawMeasurement.write_df(
                    sensor_raw_df,
                    only_insert=True
                )

                # Manage the alarms for this sensor

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

```
