import matplotlib.pyplot as plt
import numpy as np

cpu_cores = [1, 2, 3, 4, 5, 8, 16, 32]
c_sharp_big_image_times = [858372, 458208, 359402, 277815, 277922, 219620, 218689, 218238]
c_sharp_medium_image_times = [233898, 122484, 86515, 70802, 68839, 56439, 55602, 51971]
c_sharp_small_image_times = [36071, 18566, 13889, 10869, 10701, 8569, 8558, 8794]

python_big_image_times = []
python_medium_image_times = []
python_small_image_times = [74069.00835037231, 39445.00946998596, 32286.998987197876, 30332.001209259033, 27704.00357246399, 26261.000156402588, 26640.00153541565, 27612.998723983765]

levels = list(range(2, 33))


# c# data
c_sharp_speedup_big_image = []
for time in c_sharp_big_image_times:
    if time == c_sharp_big_image_times[0]:
        continue
    speedup = float(c_sharp_big_image_times[0])/float(time)
    c_sharp_speedup_big_image.append(speedup)

c_sharp_speedup_medium_image = []
for time in c_sharp_medium_image_times:
    if time == c_sharp_medium_image_times[0]:
        continue
    speedup = float(c_sharp_medium_image_times[0])/float(time)
    c_sharp_speedup_medium_image.append(speedup)

c_sharp_speedup_small_image = []
for time in c_sharp_small_image_times:
    if time == c_sharp_small_image_times[0]:
        continue
    speedup = float(c_sharp_small_image_times[0])/float(time)
    c_sharp_speedup_small_image.append(speedup)

c_sharp_effectiveness_big_image = []
for i in range(len(c_sharp_speedup_big_image)):
    effectiveness = float(c_sharp_speedup_big_image[i])/cpu_cores[i+1]
    c_sharp_effectiveness_big_image.append(effectiveness)

c_sharp_effectiveness_medium_image = []
for i in range(len(c_sharp_speedup_medium_image)):
    effectiveness = float(c_sharp_speedup_medium_image[i])/cpu_cores[i+1]
    c_sharp_effectiveness_medium_image.append(effectiveness)

c_sharp_effectiveness_small_image = []
for i in range(len(c_sharp_speedup_small_image)):
    effectiveness = float(c_sharp_speedup_small_image[i])/cpu_cores[i+1]
    c_sharp_effectiveness_small_image.append(effectiveness)

# run times c# cpu
plt.plot(cpu_cores, c_sharp_big_image_times)
plt.plot(cpu_cores, c_sharp_medium_image_times)
plt.plot(cpu_cores, c_sharp_small_image_times)
plt.legend(['Big Image', 'Medium Image', 'Small Image'])

plt.ticklabel_format(axis='both', style='sci', scilimits=(4, 4))
plt.xticks(cpu_cores, cpu_cores)
plt.title('C# Execution times on multiple threads')
plt.ylabel('Execution time [ms]')
plt.xlabel('Number of threads')
plt.grid()
plt.savefig('Figures\c_sharp_times.png')
plt.show()



# speedup c#
plt.plot(cpu_cores[1:], c_sharp_speedup_big_image)
plt.plot(cpu_cores[1:], c_sharp_speedup_medium_image)
plt.plot(cpu_cores[1:], c_sharp_speedup_small_image)
plt.legend(['Big Image', 'Medium Image', 'Small Image'])


plt.xticks(cpu_cores[1:], cpu_cores[1:])
plt.title('C# Speedup on multiple threads')
plt.ylabel('Speedup')
plt.xlabel('Number of threads')
plt.grid()
plt.savefig('Figures\c_sharp_speedup.png')
plt.show()


# effecivness c#
plt.plot(cpu_cores[1:], c_sharp_effectiveness_big_image)
plt.plot(cpu_cores[1:], c_sharp_effectiveness_medium_image)
plt.plot(cpu_cores[1:], c_sharp_effectiveness_small_image)
plt.legend(['Big Image', 'Medium Image', 'Small Image'])


plt.xticks(cpu_cores[1:], cpu_cores[1:])
plt.title('C# Effectiveness on multiple threads')
plt.ylabel('Effectiveness')
plt.xlabel('Number of threads')
plt.grid()
plt.savefig('Figures\c_sharp_effectiveness.png')
plt.show()


# python data

python_speedup_small_image = []
for time in python_small_image_times:
    if time == python_small_image_times[0]:
        continue
    speedup = float(python_small_image_times[0])/float(time)
    python_speedup_small_image.append(speedup)

python_effectiveness_small_image = []
for i in range(len(python_speedup_small_image)):
    effectiveness = float(python_speedup_small_image[i])/cpu_cores[i+1]
    python_effectiveness_small_image.append(effectiveness)



plt.plot(cpu_cores, c_sharp_small_image_times)
plt.plot(cpu_cores, python_small_image_times)
plt.legend(['C#', 'Python'])

plt.ticklabel_format(axis='both', style='sci', scilimits=(4, 4))
plt.xticks(cpu_cores, cpu_cores)
plt.title('C# and Python Execution times on multiple threads - (2560x1600) image')
plt.ylabel('Execution time [ms]')
plt.xlabel('Number of threads')
plt.grid()
plt.savefig('Figures\c_sharp_python_times.png')
plt.show()



plt.plot(cpu_cores[1:], c_sharp_speedup_small_image)
plt.plot(cpu_cores[1:], python_speedup_small_image)

plt.legend(['C#', 'Python'])


plt.xticks(cpu_cores[1:], cpu_cores[1:])
plt.title('C#  and Python Speedup on multiple threads - (2560x1600) image')
plt.ylabel('Speedup')
plt.xlabel('Number of threads')
plt.grid()
plt.savefig('Figures\c_sharp_python_speedup.png')
plt.show()


plt.plot(cpu_cores[1:], c_sharp_effectiveness_small_image)
plt.plot(cpu_cores[1:], python_effectiveness_small_image)
plt.legend(['C#', 'Python'])


plt.xticks(cpu_cores[1:], cpu_cores[1:])
plt.title('C# and PythonEffectiveness on multiple threads - (2560x1600) image')
plt.ylabel('Effectiveness')
plt.xlabel('Number of threads')
plt.grid()
plt.savefig('Figures\c_sharp_python_effectiveness.png')
plt.show()

x_axis_label = ['Small_Image', 'Medium_Image', 'Big_Image']
x_axis = [1,2,3]
y_axis_1cpu = [36071, 233898, 858372]
y_axis_4cpu = [10869, 70802, 277815]
y_axis_8cpu = [8569, 56439, 219620]
y_axis_gpu = [6196, 31672, 123607]


plt.plot(x_axis, y_axis_1cpu, 'o')
plt.plot(x_axis, y_axis_4cpu, 'o')
plt.plot(x_axis, y_axis_8cpu, 'o')
plt.plot(x_axis, y_axis_gpu, 'o')

plt.legend(['C# 1 CPU', 'C# 4 CPU', 'C# 8 CPU', 'Python  GPU'])

plt.ticklabel_format(axis='both', style='sci', scilimits=(4, 4))
plt.title('C# CPU and Python GPU Execution time for different images')
plt.xticks(x_axis, x_axis_label)
plt.yscale("log")
plt.ylabel('Execution time [ms]')
plt.xlabel('Figures')
plt.grid()
plt.savefig('Figures\cpu_gpu_comparison.png')
plt.show()
# GPU PLOT

levels = list(range(2, 33))
gpu_big_image_level_times = [755,1117,1955,3112,4490,5832,7598,9724,11970,14424,17178,20223,23332,26761,31436,37043,41190,46007,51406,56277,62429,67804,72725,80139,87148,94159,101456,107820,115534, 120739,128375]

gpu_medium_image_level_times = [170,279,492,763,1092,1481,1959,2649,3013,3643,4341,5088,5903,6772,7702,8698,9739,10860,12057,13278,14610,16265,17570,19009,20399,22262,23859,27293,29586,31527,33105]

gpu_small_image_level_times = [413,55,93,142,197,276,353,445,546,663,788,922,1069,1226,1404,1660,1776,1991,2191,2395,2636,2893,3149,3413,3682,3964,4325,4813,4955,5236,5587]


plt.plot(levels, gpu_big_image_level_times)
plt.plot(levels, gpu_medium_image_level_times)
plt.plot(levels, gpu_small_image_level_times)

plt.legend(['Big Image', 'Medium Image', 'Small Image'])
plt.ticklabel_format(axis='y', style='sci', scilimits=(4, 4))

plt.title('Python GPU Execution time')
plt.ylabel('Execution time [ms]')
plt.xlabel('Number of levels')
plt.grid()
plt.savefig('Figures\gpu_times.png')
plt.show()

