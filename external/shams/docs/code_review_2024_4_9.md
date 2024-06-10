# Code review commit [5bc22b9] del 9 April 2024 at 16:59:11 CEST

## File ullage/ullage_operation.py

### Line 54

with Session(self.production_models.engine) as session:

We don't need a session for this method. All reading and writing are through model methods.

### Line 61

initial_df.reset_index(inplace=True)

It is standard for us to set the df index as the timeserie values. So we think is better to maintain this rule.

So:

This would be the preferred way:

                           r1qja10aa001  r1qja12aa001  r1qja78cp001
timestamp
2024-02-10 08:00:00+00:00     61.203910     88.299835      0.286448
2024-02-10 08:00:10+00:00     73.142746     94.876686      0.243221
2024-02-10 08:00:20+00:00     85.627250     73.406570      0.275546
2024-02-10 08:00:30+00:00     49.741695     52.122970      0.188826
2024-02-10 08:00:40+00:00     97.113140     43.186867      0.162526
...                                 ...           ...           ...
2024-02-10 17:59:10+00:00     67.841720     60.696670      0.168905
2024-02-10 17:59:20+00:00     72.926230     57.684060      0.130395
2024-02-10 17:59:30+00:00     48.503376     55.958820      0.105552
2024-02-10 17:59:40+00:00     38.187992     68.806610      0.184853
2024-02-10 17:59:50+00:00     97.696990     24.362967      0.205707

Instead of this:

                         index  r1qja10aa001  r1qja12aa001  r1qja78cp001
0    2024-02-10 08:00:00+00:00     61.203910     88.299835      0.286448
1    2024-02-10 08:00:10+00:00     73.142746     94.876686      0.243221
2    2024-02-10 08:00:20+00:00     85.627250     73.406570      0.275546
3    2024-02-10 08:00:30+00:00     49.741695     52.122970      0.188826
4    2024-02-10 08:00:40+00:00     97.113140     43.186867      0.162526
...                        ...           ...           ...           ...
3595 2024-02-10 17:59:10+00:00     67.841720     60.696670      0.168905
3596 2024-02-10 17:59:20+00:00     72.926230     57.684060      0.130395
3597 2024-02-10 17:59:30+00:00     48.503376     55.958820      0.105552
3598 2024-02-10 17:59:40+00:00     38.187992     68.806610      0.184853
3599 2024-02-10 17:59:50+00:00     97.696990     24.362967      0.205707

Important: 

To have the df index with the correct name you should use the index_name parameter:

initial_df = self.raw_models.KKSDescription.get_kkses_df(
    [('r1qja10aa001', 'r1qja10aa001'), ('r1qja12aa001', 'r1qja12aa001'), ('r1qja78cp001', 'r1qja78cp001')],
    selected_date,
    index_name = 'timestamp'  <--------------------------
)


You must set the parameter index to True in the following code to use the index as a field in the table.

self.production_models.UllageOperation.write_df(
    initial_df.loc[:, ['timestamp', 'r1qja10aa001', 'r1qja12aa001', 'r1qja78cp001', 'operation']],
    only_insert=False, 
    index=True  <---------------------------
)

## Line 61

     except Exception as e:
         print("An error occurred during calculation:", e)
         return None


We have a special exception that is raised when no raw data are found in the raw database. So, the preferred way to manage this exception would be:

try:
    initial_df = self.raw_models.KKSDescription.get_kkses_df(
        [('r1qja10aa001', 'r1qja10aa001'), ('r1qja12aa001', 'r1qja12aa001'), ('r1qja78cp001', 'r1qja78cp001')],
        selected_date,
        index_name = 'timestamp'
    )
except self.raw_models.NoKksData as e:
    print('Missing KKS: %s - %s' % (e.tag_name, e.message))
    exit(-1)
