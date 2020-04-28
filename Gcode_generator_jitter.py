import numpy as np


min_coordinates = (5, 5)
max_coordinates = (300, 300)  # Max X Y coordinates of your machine
Reverse_direction = False  # Set the derection if the machine reaches the coordinate limits

total_frequency_analysis_duration = 30
steps_desired = 120

Step_period = total_frequency_analysis_duration/steps_desired

feedrate_values = np.logspace(2.903089987, 4.176091259056, steps_desired,base=10)  # These result in 500 steps, if we want the sweep to last 25 seconds then each step must be 50 ms (0.05 s)
movement_needed = list()
movement_coordinates_list = [[(max_coordinates[0]-min_coordinates[0])/2, (max_coordinates[1]-min_coordinates[1])/2]]


# print(*feedrate_values,sep='\n')

# We loop through all feedrate values and assign the needed movement for each feedrate step
for feedrate in feedrate_values:
    movement_needed.append(Step_period * feedrate / 60)  # The movement needed is basically the feedrate converted to mm/s times the step period in s

# print(*movement_needed,sep='\n')


# We loop through all needed movements and we add new coordinates that will be the
# original ones adding the needed movement needed
for index,movement in enumerate(movement_needed):
    # print(movement)
    # If the derection is not reversed it means that we need to go forward. That is why the new x coordinate will be the old one with the needed movement ADDED to it
    if not Reverse_direction:
        temp_new_x_coordinate = min(round((movement_coordinates_list[-1][0] + movement),3),max_coordinates[0])
        temp_new_y_coordinate = min(round((movement_coordinates_list[-1][1] + movement),3),max_coordinates[1])
        Reverse_direction = True
        movement_coordinates_list.append([temp_new_x_coordinate, temp_new_y_coordinate])
        print(int(feedrate_values[index]))
        continue  # We set a continue to avoid going through the reversed statement

    # If the derection is reversed it means that we need to go backwards. That is why the new x coordinate will be the old one with the needed movement SUBSTRACTED to it
    else:
        temp_new_x_coordinate = max(round((movement_coordinates_list[-1][0] - movement),3),min_coordinates[0])
        temp_new_y_coordinate = max(round((movement_coordinates_list[-1][1] - movement),3),min_coordinates[1])
        Reverse_direction = False
        movement_coordinates_list.append([temp_new_x_coordinate, temp_new_y_coordinate])
        print(int(feedrate_values[index]))
        continue  # We set a continue to avoid going through the non reversed statement

    # We finally append the new coordinates to the movement coordinate list which will be used as the next starting coordinates until the whole spectrum is covered
    movement_coordinates_list.append([temp_new_x_coordinate, temp_new_y_coordinate])

# print(*movement_coordinates_list, sep='\n')
# print(len(movement_coordinates_list))
# print(len(feedrate_values))

print('G1 F' + str(1500) + ' X' + str(movement_coordinates_list[0][0]) + ' Y' + str(movement_coordinates_list[0][1]))
for index, feedrate in enumerate(feedrate_values):
    print('G1 F' + str(int(feedrate)) + ' X' + str(movement_coordinates_list[index][0]) + ' Y' + str(movement_coordinates_list[index][1]))

