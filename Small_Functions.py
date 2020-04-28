
# ----------------------------------------------- The main function of this script is to store tidily all the Small functions, hence the name, that were originally scattered throughout the scripts and made it difficult to
# ----------------------------------------------- reference them properly and to access them easily. The recommended import method for this script is the following: import Small_Functions as sf

import numpy as np                                                                      # First we import the necessary libraries
import time

# This first function is very simple. It basically returns the division of the provided numbers except when d is 0
def division_possible_zero(n, d):                                                       # This function needs two numbers
    return (n / d) if d else 0                                                          # This function returns (n/d) if d (d is not equal to 0, if d is 0 the statement 'if d' becomes false) and if d is equal to 0 the else condition is fulfilled and it returns a 0

# This function takes two 1D lists and adds their individual values row by row and then outputs a 1d list with each row values added together
# If the two lists are not equal in length the shortest list will determine the length of the output list
def add_two_1D_number_lists(List1,List2):                                               # The function takes two 1D list
    Longest_list_count  = min([len(List1),len(List2)])                                  # First we determine the length of the output list with the shortest of the input lists
    Out_list = list()                                                                   # And we initialize the list that will hold the output values

    # Now we loop through the range of the shortest list adding the values of each list row together and appending them to the new list
    for i in range(Longest_list_count):
        Out_list.append((List1[i]+List2[i]))                                            # We just add the two list i row values and append the result to Out_list
    return Out_list                                                                     # Finally we return the Out_list

# This function takes a 2D list and extracts one column returning it as a 1D list. The column to extract can be specified
def Extract_Column(list_to_extract_from,column_to_extract = 0):                         # This function takes a 2D list and an optional term with the column one desires to extract
    return [row[column_to_extract] for row in list_to_extract_from]                     # For each row within the list to extract we append the row[column_to_extract] to the returned list and when it is done we return the list

# This function calculates the Overlap percentage of two EQE curves. To do so it basically runs through all the EQE values and calculates the difference
# at each point and stores it as the non_overlapped_area, and the sum of all the EQE values is the total area of both curves
# To calculate the overlap we just need to divide the non_overlapped_area by the total area and subtract it from one
# IMPORTANT WARNING!!!!!!!!!!!!! If the Wavelength steps are not the same within both wavelengths there will be a problem calculating the Overlap
def Calc_2_function_overlap_percent(EQE_curve1,EQE_curve2):                             # This function takes two EQE curves as inputs, they are 2D lists containing wavelength and EQE values
    if len(EQE_curve1) == len(EQE_curve2):                                              # We first make sure that they are equal in length
        not_overlapped_area = 0                                                         # Afterwards we initialize the variables that will be used for the calculations
        total_area = 0

        # Now we loop through one of the EQE curves and we integrate the non overlapped area and the total area
        for index,row in enumerate(EQE_curve1):
            not_overlapped_area = not_overlapped_area + abs(row[1]-EQE_curve2[index][1])    # The not_overlapped_area is defined by the absolute of the difference of these two EQE values
            total_area = total_area + abs(row[1]+EQE_curve2[index][1])                      # The total area is the addition of the two EQE values
        overlap_percentage = 100*(1-(not_overlapped_area/total_area))                       # Finally the overlap percentage is calculated as 1 minus the not_overlapped_area ratio times 100 to put it in a percentage
        return overlap_percentage                                                           # If all went well we return the percentage

    # If their lengths are not the same we return an error message saying so and the value -1
    else:
        print("Error, in Calc_2_function_overlap_percent. EQEs provided are different in size")
        return -1

# This function takes a 1D list of values and averages them within the specified smooth_points
def smooth(List_1D, smooth_points):                             # Not entirely sure how it does what it does, but it works
    box = np.ones(smooth_points)/smooth_points
    y_smooth = np.convolve(List_1D, box, mode='same')
    return y_smooth

# This function takes a 1D list and checks if it is a list of zeros or not
def list_of_zeros(List_0):                                      # This function takes a 1D list as an input
    for item in List_0:                                         # For each item in the list
        if item != 0:                                           # If any of the items is zero it returns a False statement
            return False
    return True                                                 # Otherwise it returns a True statement

# This function takes Two 1D lists and averages them 'wisely'. That meaning that it also accepts an index so that one can average several incoming lists
# with already averaged lists and keep the weight of each list consistent within the average. To do so we basically take into account how many times we
# have averaged the main list as an index value. For example if the main list input is the result of 3 previously averaged lists we set the index to 3
# and we average the main list with weight 3/4 with the List to add with weight 1/4, this way all the lists that we average contribute in exactly the same way.
def list_averager_wise(Main_list,List_to_add,Main_list_weight_index = 1):                                # This function takes two 1D lists and an index value that is set to 1 by default
    if len(Main_list) == len(List_to_add):                                              # First we check if both lists are equal in length because otherwise they cannot be averaged
        Averaged_list = list()                                                          # We initialize the list that wil hold the averaged value

        # Now we loop through the Main list averaging all the values together with their corresponding weights
        for sub_index,Main_value in enumerate(Main_list):
            Main_list_weight_factor = (Main_list_weight_index/(Main_list_weight_index+1))               # We calculate the weight factors outside so that the average formula becomes clearer
            List_to_add_weight_factor = (1/(Main_list_weight_index+1))
            Averaged_list.append((Main_value*Main_list_weight_factor + List_to_add[sub_index]*List_to_add_weight_factor))    # We append the averaged value to the averaged list
        return Averaged_list                                                                            # Finally we return the averaged list

    # If the lists are not the same length we return an error and a value of -1
    else:
        print("Error, in Calc_2_function_overlap_percent. EQEs provided are different in size")
        return -1

# This function takes a filename and a file directory and adds them together to form a Full path filename
def Full_path_adder(Filename, File_directory):
    Full_path = (File_directory + '/' + Filename)       # Basically takes the File_directory and the filename and adds them with a backslash character in between
    return Full_path                                    # Return the Full_path variable with

# This function takes a 2D list with 2 columns and shifts one of the columns by a shift amount (up or down is defined by the sign), adding a specified value on the ends to keep the dimensions constant
# and returns the output 2D list.
def Column_Shifter_2D(List_to_shift2D, column_to_shift = 0, shift_amount = 1, Edge_value = 0):  # This function takes a 2D list with 2 columns as a required argument, and then as optional arguments it takes
                                                                                                # the specific column to be shifted, the shift amount and the value to append on the edges
    Unshifted_column = Extract_Column(List_to_shift2D,not column_to_shift)                      # We first store the values of both columns within two lists, one for the column that will be shifted and another
    To_shift_column = Extract_Column(List_to_shift2D,column_to_shift)                           # for the column that will remain unshifted

    # Now we check by how much the column is to be shifted and the direction in which we have to shift it
    # If we have to shift it "to the right" which is indicated by a positive shift_amount variable
    if shift_amount > 0:
        # What we do is to pop the last element as many times as the shift_amount variable indicates
        # and we also insert as many Edge_values to the beginning of the list as the shift_amount variable indicates to preserve the original length of the list
        for _ in range(int(shift_amount)):
            To_shift_column.insert(0,Edge_value)
            To_shift_column.pop(-1)

    # If, on the contrary, we need to shift the values "to the left", which is indicated by the shift_amount variable being negative
    elif shift_amount < 0:
        # What we do is to pop the first element from the list for as many times as indicated by the shift_amount variable and
        # add as many Edge_values to the end of the list as the shift_amount variable indicates to preserve the original length of the list
        for _ in range(int(abs(shift_amount))):
            To_shift_column.append(Edge_value)
            To_shift_column.pop(0)

    # If otherwise the shift_amount variable was set to 0 we just return the same input list
    else:
        return List_to_shift2D

    # Finally we have to reconstruct the 2D list with both the shifted and unshifted lists.
    # To preserve the original order we check which column was shifted (the 0th or the 1st) and we reconstruct the output list accordingly
    if column_to_shift == 0:                                                            # If the 0th column was shifted then the original 2D list order becomes (To_shift_column,Unshifted_column)
        Output_list = Lists_1D_to_2D_list_zipper(To_shift_column,Unshifted_column)
    else:                                                                               # If otherwise the 1st column was shifted then the original 2D list order becomes (Unshifted_column,To_shift_column)
        Output_list = Lists_1D_to_2D_list_zipper(Unshifted_column,To_shift_column)
    return Output_list                                                                  # We finally return the Output_list with the shifted column

# This function takes two 1D lists, ideally two columns, and transforms them into a 2d list appending each row item into a row of two items
def Lists_1D_to_2D_list_zipper(List_1,List_2):                              # This function only needs two 1D lists as inputs
    Output_list = list()                                                    # First we initialize the 2D list that will hold the output
    if len(List_1) == len(List_2):                                          # We also have to check that the two lists are equal in length otherwise they cannot be added

        # Now we loop through all the items in List_1 and we append the items in each row of List_1 and List_2 to the output list
        for index,_ in enumerate(List_1):
            Output_list.append([List_1[index],List_2[index]])               # We take the items on the current List_1 and List_2 row and append them to our Output_list
        return Output_list                                                  # We finally return our Output_list

    # If the lists are not equal in length we return -1 and print an error message
    else:
        raise Exception('Small functions; Lists_1D_to_2D_list_zipper; error: Lists are not equal in length')
        return -1


# This class provides timer functionalities to any script that requires it. It provides with basic elapsed time functionality, with associated
# print functionality of the elapsed time. As well as more advanced progress management functionalities with its associated print functionality
class Timer:
    def __init__(self):                                                                          # To first define the timer we do not need to provide anything since the class will automatically store the time at which it has been initialized
        self.Start_time = time.time()
        self.elapsed_time = 0                                                                    # We also initialize other necessary variables
        self.elapsed_time_precise = 0
        self.Completion_percentage = 0
        self.Estimated_time = 0
        self.Progress_string = ''
        self.elapsed_time_string = ''
        self.elapsed_time_precise_string = ''

    def Update_elapsed_time(self,kronos = False):                                                             # This method updates the elapse_time variable that takes the current time (time.time()) and this is subtracted from the start_time
        self.elapsed_time_precise = (time.time() - self.Start_time)
        self.elapsed_time = int(round((time.time() - self.Start_time)))
        if kronos:
            self.elapsed_time_string = ('Elapsed time: '+str(self.elapsed_time)+' s. ')                         # It also provides a string print functionality for easier elapsed time management
            self.elapsed_time_precise_string = ('Elapsed time: '+str('{0:.6f}'.format(self.elapsed_time_precise)+' s. '))                         # It also provides a string print functionality for easier elapsed time management
        else:
            self.elapsed_time_string = ('Elapsed time: '+str(self.elapsed_time)+' s. ')                         # It also provides a string print functionality for easier elapsed time management
            self.elapsed_time_precise_string = ('Elapsed time: '+str('{0:.6f}'.format(self.elapsed_time_precise)+' s. '))                         # It also provides a string print functionality for easier elapsed time management


    def Update_progress(self,Current_step,Total_steps,Print_progress = False):                                        # This method more accurately tracks progress with both the steps and the time information it calculates the estimated time as well as the completion percentage
        self.elapsed_time = int(round((time.time() - self.Start_time)))
        self.Completion_percentage = round((division_possible_zero(Current_step,Total_steps))*100,2)
        self.Estimated_time = int(round(division_possible_zero((100*self.elapsed_time),self.Completion_percentage),0))
        self.Progress_string = (str('{0:.2f}'.format(self.Completion_percentage))+' % Elapsed time: '+str(self.elapsed_time)+' s, Estimated time: '+str(self.Estimated_time)+' s. ')   # We also provide print functionality for easier progress management
        if Print_progress:
            print(self.Progress_string)



# --------------------------------------------------------------------------------------------- sf tester program, uncomment if you want to debug this script: ---------------------------------------------------------------------------------------------------

# import Random_EQE_Generator as REG
# from tkinter import filedialog
# import Text_Importer as txtImp
# import matplotlib.pyplot as plt
# import os
#
# if __name__ == '__main__':
#
#     print(division_possible_zero(1, 0))                                            # Test the division_possible_zero function
#     print(division_possible_zero(1, 3))                                             # Test the division_possible_zero function
#
#     Solar_TXT = filedialog.askopenfilename(title='Select the Solar Curve Spectrum TXT ', initialdir=os.getcwd(), filetypes=(('txt files', '*.txt'), ('All files', '*.*')))  # Prompt the user to open a file that contains the Solar Curve txt files, and assign the file path to the variable Solar_TXT
#     Solar_Data = txtImp.import_txt(Solar_TXT)                        # Import the Solar curve data into the Solar_Data Variable
#
#     EQE1 = REG.Random_generated_EQE_curves(REG.EQE_Random_curve(),Solar_Data)                       # Random EQE class test
#     EQE2 = REG.Random_generated_EQE_curves(REG.EQE_Random_curve(),Solar_Data)
#
#     print(*EQE1.EQE_curve,sep='\n')
#
#     EQE1.EQE_curve = Column_Shifter_2D(EQE1.EQE_curve,1,200)                                        # Test for the column shifter
#
#     print(*EQE1.EQE_curve, sep='\n')
#
#     EQE_pair_1 = REG.Random_generated_EQE_Pair(EQE1,EQE1,Solar_Data)                                # Random EQE pair class test
#
#     print(EQE_pair_1.EQE_Overlap)                                                                   # Testing the Overlap function through the Random_generated_EQE_Pair class
#
#     plt.figure()                                                                                    # Plot one of the random generated curves
#     plt.plot(Extract_Column(EQE1.EQE_curve,0),Extract_Column(EQE1.EQE_curve,1), label = 'EQE 1')
#     plt.plot(Extract_Column(EQE2.EQE_curve,0),Extract_Column(EQE2.EQE_curve,1), label = 'EQE 2')
#     plt.title('Random EQE Curve')
#     plt.legend(loc='upper right')
#     plt.xlabel('Wavelength /nm')
#     plt.ylabel('EQE /%')
#
#     plt.show()

########################################################---------------------------------------------- Uncomment until here to test the script ---------------------------------------------------############################################################################################