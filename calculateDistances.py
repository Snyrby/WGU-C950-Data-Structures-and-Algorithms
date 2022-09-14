import datetime
from builtins import str, print
import csv
from HashTable import ChainingHashTable
import readCSV

# opens the distance table csv file delimits it with a ','
with open('./Data/WGUPS Distance Table with column headers.csv') as csv_file:
    distance_csv = list(csv.reader(csv_file, delimiter=','))

my_hash = ChainingHashTable()
# Load packages to Hash Table
readCSV.load_data('./Data/WGUPS Package File.csv', my_hash)

# dictionary that stores each hash key and each index for the distance table
distance_list = {}

# address list used to store each address for a truck
address_list = []

# list used to store each of the shortest distance used for each truck
all_distance_list = []

# list used to calculate the distance used for all trucks
all_package_total_distance = []


# function that is used to find each index on the distance table for each hash key and stores the hash key
# and index in a dictionary O(n)
def get_row_column(value, truck_list):
    # sets first value to 0:0
    truck_list['0'] = 0
    for row in range(1, 28):
        distance = distance_csv[row][1]
        if value.address in distance:
            truck_list[value.package_id] = row
            break


# function used to look up and verify if package has been delivered or not O(n)
def look_up_package(j, truck_delivery_list):
    # loops through each package in each truck's delivery list O(n)
    for package in truck_delivery_list:
        # if the package id on the truck = the package id being looked up then returns true
        if package.package_id == str(j):
            return True
        else:
            continue


# function is exactly the same as previous function but will delete the package from the truck if found O(N)
def look_up_and_remove_package(j, truck_delivery_list):
    count = 0
    # O(n)
    for package in truck_delivery_list:
        count += 1
        if package.package_id == str(j):
            del truck_delivery_list[count - 1]
            return True
        else:
            continue


# Nearest Neighbor Algorithm
# The following algorith uses the 'nearest neighbor' approach. It loops through each dictionary entry for hash key
# and distance index. For each entry, it will check if the value has already been delivered. If the value has not
# been delivered then the distance to the next location is stored to be sorted. After the distance list has been sorted
# it will re-loop through the dictionary by the indexes to find and remove the package being delivered from the truck
# list

# Base Case: Length of the truck list is 0 or null.
# Space-Time Complexity O(n^2)
def put_row_column(truck_list, search_key, address_deleted_list, truck_delivery_list):
    # loops through each dictionary entry O(n)
    for i, j in truck_list.items():
        # passes each key to the lookup function to check if the package has been delivered
        if look_up_package(i, truck_delivery_list):
            # if the entry is 0(hub)
            if search_key > 0:
                # distance = the value at previous location's address, to new location
                distance = distance_csv[search_key][j + 1]
                # address will equal the address associated with the distance
                address = distance_csv[0][j + 1]
                # if the address is null then it flips the row with the column
                if distance == '':
                    distance = distance_csv[j][search_key + 1]
            # if the current location is null then it will only look for distances under the home column
            else:
                distance = distance_csv[j][search_key + 2]
                address = distance_csv[j][search_key + 1]
            # tries to convert the distance to float
            try:
                float(distance)
                # compares if the float distance is 0, so it doesn't add the current location as a next location
                if float(distance) != float(0):
                    distance_list[address] = float(distance)
            except:
                continue
    # sorts the distance dictionary values and stores it as a sorted list
    sorted_distance_list = sorted(distance_list.values())

    # stores the lowest distance to an all distance list used for printing
    all_distance_list.append(sorted_distance_list[0])

    # stores the address associated with that distance in an address list
    address = list(distance_list.keys())[list(distance_list.values()).index(sorted_distance_list[0])]
    address_list.append(address)

    # loops through each truck dictionary entry O(n)
    for key, value in truck_list.items():
        # checks if the previous location is not at the hub, and it's next location is not the same location
        if search_key > 0 and value != 0:
            # selects distance from distance table
            distance = distance_csv[search_key][value + 1]
            # if distance is null then flips the row and column
            if distance == '':
                distance = float(distance_csv[value][search_key + 1])
            # checks if the lowest distance is = to the distance found
            if sorted_distance_list[0] == float(distance):
                # if they do equal, then confirms if the address associated = the lowest distance address
                if distance_csv[0][value + 1] == address:
                    # looks up if that package has been delivered and if not, removes it from the truck list
                    if look_up_and_remove_package(key, truck_delivery_list):
                        # stores the current location as the location of the package being delivered
                        next_key = int(value)
                        # adds value to a deleted list
                        address_deleted_list.append(key)
                        # calls the function to add the delivery time to total time
                        add_delivery_time(sorted_distance_list[0], key)
        else:
            # if the search key is 27, then prevents program from exited out of bounds
            if search_key >= 27:
                continue
            else:
                try:
                    float(distance_csv[value][search_key + 2])
                    if str(sorted_distance_list[0]) == str(float(distance_csv[value][search_key + 2])):
                        if look_up_and_remove_package(key, truck_delivery_list):
                            next_key = int(value)
                            address_deleted_list.append(key)
                            add_delivery_time(sorted_distance_list[0], key)

                except:
                    continue
    # clears the sorted distance list and returns the search key
    distance_list.clear()
    return next_key


# function used to calculate the distance from the last location back to home O(1)
def add_home(search_key):
    all_distance_list.append(distance_csv[search_key][2])
    address_list.append('Hub')


# function used to calculate the time it'll take for the distance O(1)
def calculate_time(total_distance, start_time):
    # divides the distance by 18 mph
    hours = total_distance / 18
    # calculates seconds by multiplying by 3600
    seconds = hours * 3600
    # runs modulus to calculate how many minutes and seconds are left over
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    # formats the time in HH:MM:SS
    new_distance_time = "%d:%02d:%02d" % (h, m, s)
    # prints how long it will take
    print('The total time will take: ' + new_distance_time)

    # adds the start time to the distance time
    time_list = [start_time, new_distance_time]
    my_sum = datetime.timedelta()
    for i in time_list:
        (h, m, s) = i.split(':')
        d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        my_sum += d
    # prints start time and added time
    print('The start time was: ' + start_time + '. The finish time is: ' + str(my_sum))


# prints each package on each truck with the distance to each location O(n)
def print_data(truck, start_time):
    # sets total distance
    total_distance = 0
    # print statement used to show which truck it is
    print('\nThe shortest path for truck ' + str(truck) + ' is: ')
    # loops through each address and prints the address and distance
    for i in range(0, len(address_list)):
        address = str(address_list[i]).split("\n")
        print(address[0] + ' with a distance of: ' + str(all_distance_list[i]) + ' miles.')
        # adds total distance
        total_distance += float(all_distance_list[i])
    # prints total distance
    print('The total distance is: ' + "{:.2f}".format(total_distance) + ' miles.')
    # adds the total distance to a list for the total distance of all 3 trucks
    all_package_total_distance.append(total_distance)
    # calls the calculate time function
    calculate_time(total_distance, start_time)
    # clears both lists
    address_list.clear()
    all_distance_list.clear()


# function used to calculate the total delivery distance for each package O(n)
def add_delivery_time(distance, key):
    total_distance = 0
    for i in range(0, len(all_distance_list)):
        total_distance += float(all_distance_list[i])
        if all_distance_list[i] == distance:
            if int(key) > 0:
                value = my_hash.search(key)
                add_time(total_distance, value.delivery_start, value, key)
                break


# function used to calculate time. This is the exact same as previous calculate time function but updates each hash
# entry with the delivery time O(1)
def add_time(total_distance, start_time, value, key):
    hours = total_distance / 18
    seconds = hours * 3600
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    new_distance_time = "%d:%02d:%02d" % (h, m, s)
    time_list = [start_time, new_distance_time]
    my_sum = datetime.timedelta()

    for i in time_list:
        (h, m, s) = i.split(':')
        d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        my_sum += d
    value.delivery = str(my_sum)
    my_hash.insert(key, value)


# returns combined value of all truck total distances O(n)
def get_total_distance():
    total_distance = 0
    for i in range(0, len(all_package_total_distance)):
        total_distance += all_package_total_distance[i]
    return "{:.2f}".format(total_distance)
