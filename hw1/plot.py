import matplotlib.pyplot as plt
import os
import math
import numpy as np

dir_name = "output/05/"
XOs = ["op", "un", "ps"]
exp_time = 50
x_axis = {"op":list(), "un":list(), "ps":list(), "th":list()}
converge_times = {"op":list(), "un":list(), "ps":list(), "th":list()}

intensity_draw_size = 20
selection_intensities = {"op":np.zeros(intensity_draw_size), "un":np.zeros(intensity_draw_size), "ps":np.zeros(intensity_draw_size), "th":np.zeros(intensity_draw_size)}

filenames = os.listdir(dir_name)

for filename in filenames:
    if filename.startswith("plot"):
        continue

    XO_type = filename[:2]
    idx = filename.find(".")
    num = int(filename[len(XO_type):idx])
    x_axis[XO_type].append(num)
    converge_times[XO_type].append(0)
    with open(dir_name + filename, "r") as f:
        for line in f:
            data = np.fromstring(line, sep=',')
            converge_time = data[0]
            selection_intensities[XO_type] += data[-intensity_draw_size:]
            converge_times[XO_type][len(converge_times[XO_type])-1] += converge_time

    converge_times[XO_type][len(converge_times[XO_type])-1] /= exp_time

for XO_type in XOs:
    converge_times[XO_type] = [x for _,x in sorted(zip(x_axis[XO_type], converge_times[XO_type]))]
    x_axis[XO_type] = sorted(x_axis[XO_type])
    selection_intensities[XO_type] /= (exp_time * ( (500-50) / 25 + 1))
    print(converge_times[XO_type])
    print(x_axis[XO_type])

s = 2
selection_intensity = math.sqrt(2*(math.log(s) - math.log(math.sqrt(4.14*math.log(s)))))
print("selection_intensity:", selection_intensity)
selection_intensities["th"] = [selection_intensity for i in range(20)]
for i in range(50, 501, 50):
    x_axis["th"].append(i)

    converge_times["th"].append(math.pi/2*math.sqrt(i)/selection_intensity)
    print("t_conv:", math.pi/2*math.sqrt(i)/selection_intensity)

plt.scatter(x_axis["op"], converge_times["op"])
plt.scatter(x_axis["un"], converge_times["un"])
plt.scatter(x_axis["ps"], converge_times["ps"])
plt.scatter(x_axis["th"], converge_times["th"])

plt.xlabel('ell')
plt.ylabel('convergence time (generation)')
plt.legend(['one-pointXO', 'uniformXO', 'populationwise-shuffle', 'Thierens theorem'])

plt.savefig(dir_name + "plot_all.png")
plt.show()

plt.scatter([i for i in range(-20, 0, 1)], selection_intensities["op"])
plt.scatter([i for i in range(-20, 0, 1)], selection_intensities["un"])
plt.scatter([i for i in range(-20, 0, 1)], selection_intensities["ps"])
plt.scatter([i for i in range(-20, 0, 1)], selection_intensities["th"])

plt.xlabel('last 20 generation')
plt.ylabel('selection intensity')
plt.legend(['one-pointXO', 'uniformXO', 'populationwise-shuffle', 'Thierens theorem'])

plt.savefig(dir_name + "plot_last20.png")
plt.show()