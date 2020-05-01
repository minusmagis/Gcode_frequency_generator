from scipy.io.wavfile import read
import numpy
from tkinter import filedialog
import Small_Functions as sf
import matplotlib.pyplot as plt
from statistics import mean
import matplotlib

Wave_File_undampened = filedialog.askopenfilename(title='Select the Wav undampened spectrum you want to analyze', initialdir=r'C:\Users\minus\Documents\Fedellando\Video 6 Anti vibration feet',
                                                   filetypes=(('wav files', '*.wav'), ('All files', '*.*')))  # Prompt the user to open a file that contains the EQE curve file of the spectrum to be analyzed, and import it as a txt file into the EQE_curve variable
raw_undampened_data = read(Wave_File_undampened)
values_array_undampened = numpy.array(raw_undampened_data[1],dtype=float)
values_array_undampened = sf.Extract_Column(values_array_undampened,0)

Wave_File_dampened = filedialog.askopenfilename(title='Select the Wav dampened spectrum you want to analyze', initialdir=r'C:\Users\minus\Documents\Fedellando\Video 6 Anti vibration feet',
                                                   filetypes=(('wav files', '*.wav'), ('All files', '*.*')))  # Prompt the user to open a file that contains the EQE curve file of the spectrum to be analyzed, and import it as a txt file into the EQE_curve variable
raw_dampened_data = read(Wave_File_dampened)
values_array_dampened = numpy.array(raw_dampened_data[1],dtype=float)
values_array_dampened = sf.Extract_Column(values_array_dampened,0)

Wave_File_full_dampened = filedialog.askopenfilename(title='Select the Wav full dampened spectrum you want to analyze', initialdir=r'C:\Users\minus\Documents\Fedellando\Video 6 Anti vibration feet',
                                                   filetypes=(('wav files', '*.wav'), ('All files', '*.*')))  # Prompt the user to open a file that contains the EQE curve file of the spectrum to be analyzed, and import it as a txt file into the EQE_curve variable
raw_full_dampened_data = read(Wave_File_full_dampened)
values_array_full_dampened = numpy.array(raw_full_dampened_data[1],dtype=float)
values_array_full_dampened = sf.Extract_Column(values_array_full_dampened,0)

feedrate_values_undampened = numpy.logspace(2.903089987, 4.176091259056, len(values_array_undampened),base=10)
feedrate_values_dampened = numpy.logspace(2.903089987, 4.176091259056, len(values_array_dampened),base=10)
feedrate_values_full_dampened = numpy.logspace(2.903089987, 4.176091259056, len(values_array_full_dampened),base=10)

volume_undampened = list()
values_array_undampened_absolute = list()
Timer1 = sf.Timer()
for index,value in enumerate(values_array_undampened):
    values_array_undampened_absolute.append(abs(value))
    if index % 100000 == 0:
        Timer1.Update_progress(index,len(values_array_undampened),True)

# print(*values_array_undampened_absolute,sep='\n')


Timer2 = sf.Timer()
for index,value in enumerate(values_array_undampened_absolute):
    if index % 500 == 0 and index != 0:
        volume_temp = mean(values_array_undampened_absolute[index-500:index])
        volume_undampened.append(volume_temp)
    if index % 10000 == 0:
        Timer2.Update_progress(index, len(values_array_undampened_absolute), True)

# print(volume_undampened)


volume_dampened = list()
values_array_dampened_absolute = list()
Timer1 = sf.Timer()
for index,value in enumerate(values_array_dampened):
    values_array_dampened_absolute.append(abs(value))
    if index % 100000 == 0:
        Timer1.Update_progress(index,len(values_array_dampened),True)

# print(*values_array_undampened_absolute,sep='\n')


Timer2 = sf.Timer()
for index,value in enumerate(values_array_dampened_absolute):
    if index % 500 == 0 and index != 0:
        volume_temp = mean(values_array_dampened_absolute[index-500:index])
        volume_dampened.append(volume_temp)
    if index % 10000 == 0:
        Timer2.Update_progress(index, len(values_array_dampened_absolute), True)



volume_full_dampened = list()
values_array_full_dampened_absolute = list()
Timer1 = sf.Timer()
for index,value in enumerate(values_array_full_dampened):
    values_array_full_dampened_absolute.append(abs(value))
    if index % 100000 == 0:
        Timer1.Update_progress(index,len(values_array_full_dampened),True)

# print(*values_array_undampened_absolute,sep='\n')


Timer2 = sf.Timer()
for index,value in enumerate(values_array_full_dampened_absolute):
    if index % 500 == 0 and index != 0:
        volume_temp = mean(values_array_full_dampened_absolute[index-500:index])
        volume_full_dampened.append(volume_temp)
    if index % 10000 == 0:
        Timer2.Update_progress(index, len(values_array_full_dampened_absolute), True)

volume_dampened = sf.smooth(volume_dampened,80)
volume_undampened = sf.smooth(volume_undampened,80)
volume_full_dampened = sf.smooth(volume_full_dampened,80)

volume_dampened = sf.smooth(volume_dampened,50)
volume_undampened = sf.smooth(volume_undampened,50)
volume_full_dampened = sf.smooth(volume_full_dampened,50)

# print(volume_dampened)

feedrate_values_undampened_volume = numpy.logspace(2.903089987, 4.176091259056, len(volume_undampened),base=10)
feedrate_values_dampened_volume = numpy.logspace(2.903089987, 4.176091259056, len(volume_dampened),base=10)
feedrate_values_full_dampened_volume = numpy.logspace(2.903089987, 4.176091259056, len(volume_dampened),base=10)



# plt.figure()  # Plot one of the random generated curves
# plt.plot(feedrate_values_undampened,values_array_undampened , label='undampened')
# plt.plot(feedrate_values_dampened,values_array_dampened , label='dampened')
# plt.title('Jitter test sound levels')
# plt.legend(loc='upper right')
# plt.xlabel('Feedrate u/min')
# plt.ylabel('Sound amplitude /a.u.')
# plt.xscale("log")

plt.figure()  # Plot one of the random generated curves
plt.plot(feedrate_values_undampened_volume,volume_undampened , label='Not dampened')
plt.plot(feedrate_values_dampened_volume,volume_dampened , label='Nylon dampened')
plt.plot(feedrate_values_full_dampened_volume,volume_full_dampened , label='Flexible filament dampened')
plt.title('Feedrate spectrum sound levels')
plt.legend(loc='upper right')
plt.xlabel('Feedrate u/min')
plt.ylabel('Sound amplitude /a.u.')
plt.xlim(left=805, right=14900)

fig1, ax1 = plt.subplots()
ax1.set_title('Feedrate spectrum sound levels')
ax1.legend(loc='upper right')
ax1.set_xlabel('Feedrate u/min')
ax1.set_ylabel('Sound amplitude /a.u.')
ax1.plot(feedrate_values_undampened_volume,volume_undampened , label='undampened')
ax1.plot(feedrate_values_dampened_volume,volume_dampened , label='dampened')
ax1.set_xscale('log')
ax1.set_xticks(numpy.logspace(2.903089987, 4.176091259056, 10,base=10))
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.set_xlim(left=805, right=14900)

plt.show()



print(*c,sep='\n')