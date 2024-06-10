# Code review commit [de7b4a3] del 5 April 2024 at 11:36:07 CEST



## File scripts/launch_ullage_operation.py

### Line 43: final_df = raw_models.raw_kks(selected_date.strftime('%Y-%m-%d')) 
You are creating a df with ALL kkses from the kks_description. That tabla will have around 2000 items. You only have to create the final_df with only 3 kks for this submodule: r1qja10aa001, r1qja12aa001 and r1qja78cp001.
With the second demo we sent you a real kks_description table with thousands of records.
Why are you getting the final_df in the launch script instead of in the UllageONOFFOperation class. All logic, including this of retrieving the df must be inside the class. You could create a class method called getInitialdf to get the data.


## File models/raw.py

### Line 154: def raw_kks(date_data, index_name=None): 
Again, with this function, you are creating a df with ALL kkses for the kks_description table instead of using only the 3 kkses required.
This function is offside any class. The correct place would be inside the KKSDescription class as a classmethod. 
But you don't need to create any method like this. It would be enough to use this:
    self.raw_models.get_kkses_df(['r1qja10aa001', 'r1qja12aa001', 'r1qja78cp001'], selected_date)


## File ullage/ullage_operation.py

### Line 44: try:
You are using a try block wrapping all the methods and only except for the global Exception. I don´t see any value of this. You must use concrete exception instances. You have to have a reason to use the try. Perhaps you are expecting some error and want the manage that.

### Line 50

             for col in required_columns:
                 if col not in self.final_df.columns:
                     raise ValueError(f"Column '{col}' not found in the DataFrame.")


This code makes no any sense. You are building a df with all the kks in the system and then you are testing again checking it has all those columns. Could you elaborate on the reason for this?

### Line 54

    for col in required_columns:
        if col[7:9] == "aa" and any(c[7:9] == "cp" for c in required_columns):
            on_condition = True
            break

I suppose this code is trying to find the 3 kkses (r1qja10aa001, r1qja12aa001 and r1qja78cp001) in that huge df. Why are you not using the completed name instead of this slice tests.
This code always would set the on_condition variable at True and break, because the kkses must be always in the required_columns. Could you elaborate on the reason for this?


### Line 62

    if on_condition:
        on_condition = (((self.final_df[required_columns[0]] >= 1.0) & (
                self.final_df[required_columns[2]] >= 0.3)) |
                        ((self.final_df[required_columns[1]] >= 1.0) & (
                                self.final_df[required_columns[2]] >= 0.3)))
    else:
        off_condition = ~on_condition


I'm having trouble trying to understand the way you are doing the test for on_condition. As I said before, the on_codition would be always True in your code. 
In order to this test to work correctly the kkses must be in a certain order inside the required_columns list. You don't have any security of that. Why are you using that system?

You can do all this functionality with only:


initial_df = self.raw_models.get_kkses_df(['r1qja10aa001', 'r1qja12aa001', 'r1qja78cp001'], selected_date)

initial_df['operation'] = 'OFF'
initial_df['operation'] = 'OFF'


initial_df.loc[((initial_df['r1qja12aa001'] >= 1) | (initial_df['r1qja10aa001'] >= 1)) & (initial_df['r1qja78cp001'] >= 0.3), 'operation'] = 'ON'

