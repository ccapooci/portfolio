import re, sys
import math, random
import numpy as np
import operator
import csv
import matplotlib.pyplot as plt


#### BEGIN----- additional functions ----- ####

## assisted from Python Docs
def csv_to_list(file_name):
    salaries = []
    first =- True
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:           
            if(not first):
                salaries.append(float(row[2]))
            first = False
    return salaries

#### END----- additional functions ----- ####

if __name__ == "__main__":
    salaries = csv_to_list("IL_employee_salary.csv")
    modified_bin_0_05 = []
    modified_bin_0_1 = []
    modified_bin_5_0 = []
    bins = [40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000]
    bin_sizes, a, b = plt.hist(salaries, bins=bins)
    bin_sizes_list = []
    for val in bin_sizes:
        bin_sizes_list.append(val)        

    epilson = 0.05
    for val in bin_sizes:
        if(not val == 0):
            noise = np.random.laplace(0, 1/epilson , 1)
            modified_bin_0_05.append(val + noise[0])
        else:
            modified_bin_0_05.append(val)

    epilson = 0.1
    for val in bin_sizes:
        if(not val == 0):
            noise = np.random.laplace(0, 1/epilson , 1)
            modified_bin_0_1.append(val + noise[0])
        else:
            modified_bin_0_1.append(val)

    epilson = 5
    for val in bin_sizes:
        if(not val == 0):
            noise = np.random.laplace(0, 1/epilson , 1)
            modified_bin_5_0.append(val + noise[0])
        else:
            modified_bin_5_0.append(val)

    plt.clf()
    bar_width = 0.25
    print(bin_sizes)
    print(bin_sizes_list)
    print(modified_bin_0_05)
    print(modified_bin_0_1)
    print(modified_bin_5_0)
    list_40_50 = []
    list_40_50.append(bin_sizes_list[0])
    list_40_50.append(modified_bin_0_05[0])
    list_40_50.append(modified_bin_0_1[0])
    list_40_50.append(modified_bin_5_0[0])
    list_50_60 = []
    list_50_60.append(bin_sizes_list[1])
    list_50_60.append(modified_bin_0_05[1])
    list_50_60.append(modified_bin_0_1[1])
    list_50_60.append(modified_bin_5_0[1])
    list_60_70 = []
    list_60_70.append(bin_sizes_list[2])
    list_60_70.append(modified_bin_0_05[2])
    list_60_70.append(modified_bin_0_1[2])
    list_60_70.append(modified_bin_5_0[2])
    list_70_80 = []
    list_70_80.append(bin_sizes_list[3])
    list_70_80.append(modified_bin_0_05[3])
    list_70_80.append(modified_bin_0_1[3])
    list_70_80.append(modified_bin_5_0[3])
    list_80_90 = []
    list_80_90.append(bin_sizes_list[4])
    list_80_90.append(modified_bin_0_05[4])
    list_80_90.append(modified_bin_0_1[4])
    list_80_90.append(modified_bin_5_0[4])
    list_90_100 = []
    list_90_100.append(bin_sizes_list[5])
    list_90_100.append(modified_bin_0_05[5])
    list_90_100.append(modified_bin_0_1[5])
    list_90_100.append(modified_bin_5_0[5])
    list_100_110 = []
    list_100_110.append(bin_sizes_list[6])
    list_100_110.append(modified_bin_0_05[6])
    list_100_110.append(modified_bin_0_1[6])
    list_100_110.append(modified_bin_5_0[6])
    bins_string = ["[40000,50000)", "[50000,60000)", "[60000,70000)", "[70000,80000)", "[80000,90000)", "[90000,100000)", "[100000,110000)"]
    bins_string1 = [1,    3,    5,    7    ]
    bins_string2 = [1.25, 3.25, 5.25, 7.25 ]
    bins_string3 = [1.5,  3.5,  5.5,  7.5  ]
    bins_string4 = [1.75, 3.75, 5.75, 7.75 ]
    bins_string5 = [2,    4,    6,    8    ]
    bins_string6 = [2.25, 4.25, 6.25, 8.25 ]
    bins_string7 = [2.5,  4.5,  6.5,  8.5  ]

    plt.bar(x=bins_string1, height=list_40_50, color='mintcream', width=bar_width, edgecolor='white', label='[40K,50K)')
    plt.bar(x=bins_string2, height=list_50_60, color='lime', width=bar_width, edgecolor='white', label='[50K,60K)')
    plt.bar(x=bins_string3, height=list_60_70, color='limegreen', width=bar_width, edgecolor='white', label='[60K,70K)')
    plt.bar(x=bins_string4, height=list_70_80, color='forestgreen', width=bar_width, edgecolor='white', label='[70K,80K)')
    plt.bar(x=bins_string5, height=list_80_90, color='darkgreen', width=bar_width, edgecolor='white', label='[80K,90K)')
    plt.bar(x=bins_string6, height=list_90_100, color='turquoise', width=bar_width, edgecolor='white', label='[90K,100K)')
    plt.bar(x=bins_string7, height=list_100_110, color='teal', width=bar_width, edgecolor='white', label='[100K,110K)')

    # Add xticks on the middle of the group bars
    plt.xlabel('Bar Charts', fontweight='bold')
    plt.xticks([1.75, 3.75, 5.75, 7.75], ['Normal', 'Epilson = 0.05', 'Epilson = 0.1', 'Epilson = 5.0'])

        
    plt.title("Histogram of Salaries")
    plt.legend()
    plt.show()
