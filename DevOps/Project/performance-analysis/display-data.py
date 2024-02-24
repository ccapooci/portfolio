import matplotlib.pyplot as plt
import csv

data_0 = []
data_1 = []

with open('results/results.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    complete = False
    for row in plots:
        for datum in row:
            if not complete:            
                data_0.append(float(datum))
        # Only do row 1
        complete = True


#https://matplotlib.org/stable/gallery/statistics/boxplot_color.html#sphx-glr-gallery-statistics-boxplot-color-py
fig, ax = plt.subplots(nrows=1, ncols=1, sharey=True)
fig.suptitle("Distribution of HTTP Response Times")
 # Creating plot
ax.boxplot(data_0)
ax.set_ylabel("Time to receive responses in msec")
# show plot
plt.savefig('results-plot.png')