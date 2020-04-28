import numpy as np


min_coordinates = (5, 5)
max_coordinates = (300, 300)  # Max X Y coordinates of your machine
Reverse_direction = False  # Set the derection if the machine reaches the coordinate limits

total_frequency_analysis_duration = 60
steps_desired = 600

Step_period = total_frequency_analysis_duration/steps_desired

feedrate_values = np.logspace(2.903089987, 4.176091259056, steps_desired,base=10)  # These result in 500 steps, if we want the sweep to last 25 seconds then each step must be 50 ms (0.05 s)
movement_needed = list()
movement_coordinates_list = [[min_coordinates[0], min_coordinates[1]]]


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
        temp_new_x_coordinate = round((movement_coordinates_list[-1][0] + movement),3)
        temp_new_y_coordinate = round((movement_coordinates_list[-1][1] + movement),3)

        # In the case that we reach the maximum coordinates we need to change direction and we can already set the new reversed direction coordinates, and also we set the direction to be reversed so that in the next loop we jump to the reversed statement directly
        if temp_new_x_coordinate > max_coordinates[0] or temp_new_y_coordinate > max_coordinates[1]:
            temp_new_x_coordinate = round((movement_coordinates_list[-1][0] - movement),3)
            temp_new_y_coordinate = round((movement_coordinates_list[-1][1] - movement),3)

            # If when trying to substract we exceed the min coordinates just limit the printer movement to the min coordinates
            if temp_new_x_coordinate < min_coordinates[0] or temp_new_y_coordinate < min_coordinates[1]:
                temp_new_x_coordinate = min_coordinates[0]
                temp_new_y_coordinate = min_coordinates[1]
            Reverse_direction = True
            movement_coordinates_list.append([temp_new_x_coordinate, temp_new_y_coordinate])
            print(int(feedrate_values[index]))
            continue  # We set a continue to avoid going through the reversed statement

    # If the derection is reversed it means that we need to go backwards. That is why the new x coordinate will be the old one with the needed movement SUBSTRACTED to it
    else:
        temp_new_x_coordinate = round((movement_coordinates_list[-1][0] - movement),3)
        temp_new_y_coordinate = round((movement_coordinates_list[-1][1] - movement),3)

        # In the case that we reach the minimum coordinates we need to change direction and we can already set the new non reversed direction coordinates, and also we set the direction to be non reversed so that in the next loop we jump to the non reversed statement directly
        if temp_new_x_coordinate < min_coordinates[0] or temp_new_y_coordinate < min_coordinates[1]:
            temp_new_x_coordinate = round((movement_coordinates_list[-1][0] + movement),3)
            temp_new_y_coordinate = round((movement_coordinates_list[-1][1] + movement),3)

            # If when trying to add we exceed the max coordinates just limit the printer movement to the max coordinates
            if temp_new_x_coordinate > max_coordinates[0] or temp_new_y_coordinate > max_coordinates[1]:
                temp_new_x_coordinate = max_coordinates[0]
                temp_new_y_coordinate = max_coordinates[1]

            Reverse_direction = False
            movement_coordinates_list.append([temp_new_x_coordinate, temp_new_y_coordinate])
            print(int(feedrate_values[index]))
            continue  # We set a continue to avoid going through the non reversed statement

    # We finally append the new coordinates to the movement coordinate list which will be used as the next starting coordinates until the whole spectrum is covered
    movement_coordinates_list.append([temp_new_x_coordinate, temp_new_y_coordinate])

# print(*movement_coordinates_list, sep='\n')
# print(len(movement_coordinates_list))
# print(len(feedrate_values))

for index, feedrate in enumerate(feedrate_values):
    print('G1 F' + str(int(feedrate)) + ' X' + str(movement_coordinates_list[index][0]) + ' Y' + str(movement_coordinates_list[index][1]))

