import numpy as np
import pandas as pd 

# data = {245: 'LD', 118: 'LC', 100: '9L', 96: 'VA', 93: 'EM', 72: 'CL', 50: 'AT', 49: 'BZ', 47: 'LB', 45: 'EN', 44: 'LA', 43: 'TY', 38: 'T2', 37: 'NP', 36: 'NR', 32: 'DF', 29: 'AR', 26: 'SN', 24: 'BY', 23: 'FD', 22: '4Z', 21: 'J2', 20: 'LM', 19: 'SM', 17: 'L4', 16: 'SB', 14: 'SL', 13: 'AU', 12: 'PR', 11: 'CM', 9: 'EF', 8: 'TX', 7: 'LU', 6: 'EK', 5: '2Z', 4: 'LP', 3: 'BP', 2: 'AN', 1: '24'}
my_img = [
['451', '645', '451', '3768'],
['645', '841', '3032', '317'],
['3860', '611', '779', '779'],
['646', '842', '611', '844' ],
['840', '3790', '840', '779'],
]
my_dict  = {
'key1': 1, 
'key2': 2,
'key3': 3,
'key4': 4,
'key5': 5,
'key6': 6, 
    }
# def unique_count(a):
#     unique_value, counts = np.unique(a, return_counts=True)
#     a_dict = dict(zip(unique_value, counts))
#     print(a_dict) 
#     sort_a = sorted(a_dict.items(), key=lambda item: item[1])[::-1]
#     return dict(sort_a)
df = pd.DataFrame(list(my_dict.values()))


print(df)
