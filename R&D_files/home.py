import os
import pandas as pd
import numpy

states = ["California", "Texas", "Florida", "New York"]
population = [39614493, 29730311, 21944577, 19299981]
dict_states = {'States': states, 'Population': population}
df_states = pd.DataFrame.from_dict(dict_states)

#print(df_states)
#df_states.to_csv('states.csv', index=False)

#print(states[-2])
# for state in states:
#     if state == "Florida":
#         print(state)

# with open('test.txt', 'w') as file:
#     file.write("Data successfully scraped!")

new_list = [2, 4, 6, 'California']
for element in new_list:
    try:
        print(element / 2)
    except:
        print('The ' + element + 'is not a number')
n = 4

while n > 0:
    print(n)
    n = n - 1
    if n == 2:
        break
print('Loop Ended')
