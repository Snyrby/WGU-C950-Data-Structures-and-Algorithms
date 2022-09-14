import readCSV
import calculateDistances
import datetime

# lists for each truck
first_delivery_list = []
second_delivery_list = []
third_delivery_list = []

# dictionary for each truck containing hash key and distance index
truck_one_list = {}
truck_two_list = {}
truck_three_list = {}

# Departure time for each truck
first_departure = ['8:00:00']
second_departure = ['9:05:00']
third_departure = ['10:20:00']


# function used to do everything related to truck 1 O(n)
def first_truck_data():
    # truck starts at home
    next_key = 0
    # sets up address deleted list
    address_deleted_list = []
    # sets every delivery time on the first truck to 8am O(n) and makes truck dictionary
    for index, value in enumerate(readCSV.get_first_delivery()):
        value.delivery_start = first_departure[0]
        first_delivery_list.append(readCSV.get_first_delivery()[index])
        calculateDistances.get_row_column(value, truck_one_list)
        calculateDistances.my_hash.insert(str(value.package_id), readCSV.get_first_delivery()[index])
    # calculates the truck length and calls the function to find next location until there are none left
    length = len(first_delivery_list)
    while len(address_deleted_list) < length:
        next_key = calculateDistances.put_row_column(truck_one_list, next_key, address_deleted_list,
                                                     first_delivery_list)
    # calls function to add home and print the data
    calculateDistances.add_home(next_key)
    calculateDistances.print_data(1, first_departure[0])


# function used to do everything for truck 2 and is the exact same as truck 1 O(n)
def second_truck_data():
    next_key = 0
    address_deleted_list = []
    for index, value in enumerate(readCSV.get_second_delivery()):
        value.delivery_start = second_departure[0]
        second_delivery_list.append(readCSV.get_second_delivery()[index])
        calculateDistances.get_row_column(value, truck_two_list)
        calculateDistances.my_hash.insert(str(value.package_id), readCSV.get_second_delivery()[index])
    length = len(second_delivery_list)
    while len(address_deleted_list) < length:
        next_key = calculateDistances.put_row_column(truck_two_list, next_key, address_deleted_list,
                                                     second_delivery_list)
    calculateDistances.add_home(next_key)
    calculateDistances.print_data(2, second_departure[0])


# function used to do everything for truck 3 and is the exact same as truck 1 O(n)
def third_truck_data():
    next_key = 0
    address_deleted_list = []
    # corrects the 'wrong address' and updates it in the hash table
    value_to_correct = calculateDistances.my_hash.search('9')
    value_to_correct.address = '410 S State St'
    value_to_correct.city = 'Salt Lake City'
    value_to_correct.state = 'UT'
    value_to_correct.address_zip = '84111'
    calculateDistances.my_hash.insert(value_to_correct.package_id, value_to_correct)
    for index, value in enumerate(readCSV.get_final_delivery()):
        value.delivery_start = third_departure[0]
        third_delivery_list.append(readCSV.get_final_delivery()[index])
        calculateDistances.get_row_column(value, truck_three_list)
        calculateDistances.my_hash.insert(str(value.package_id), readCSV.get_final_delivery()[index])
    length = len(third_delivery_list)
    while len(address_deleted_list) < length:
        next_key = calculateDistances.put_row_column(truck_three_list, next_key, address_deleted_list,
                                                     third_delivery_list)
    calculateDistances.add_home(next_key)
    calculateDistances.print_data(3, third_departure[0])


# function used to display each status of each package at different times O(n)
def screen_shot(time):
    print('\nScreenshot at', time)
    # loops through each value in the hash table and stores it as an object
    for i in range(1, 41):
        value = calculateDistances.my_hash.search(str(i))
        # splits the delivery time by :
        time_1 = value.delivery.split(':')
        # splits the delivery start by :
        time_2 = value.delivery_start.split(':')
        # splits the screenshot time by :
        time_3 = time.split(':')
        if len(time_3) < 3:
            time_3.append('00')
        # makes a time object for each time
        delivery_time = datetime.timedelta(hours=int(time_1[0]), minutes=int(time_1[1]), seconds=int(time_1[2]))
        delivery_start = datetime.timedelta(hours=int(time_2[0]), minutes=int(time_2[1]), seconds=int(time_2[2]))
        time_comparison = datetime.timedelta(hours=int(time_3[0]), minutes=int(time_3[1]), seconds=int(time_3[2]))

        # checks if the screenshot time is before the delivery time and after the start time
        if delivery_start <= time_comparison <= delivery_time:
            # if it is, updates the package to en route and updates the package in hash table then prints
            value.delivery_status = 'En route'
            if value.package_id == '9':
                value.address = '410 S State St'
                value.address_zip = '84111'
            calculateDistances.my_hash.insert(str(value.package_id), value)
            print('Package:', value.package_id, 'is', value.delivery_status, 'and will be delivered at',
                  value.address, value.city + ',', value.state, value.address_zip, 'at', str(delivery_time)
                  + '. The weight is:', value.size)
        # if the screenshot time is after the delivery time then updates to delivered and updates hash table and prints
        elif time_comparison > delivery_time:
            value.delivery_status = 'Delivered'
            if value.package_id == '9':
                value.address = '410 S State St'
                value.address_zip = '84111'
            calculateDistances.my_hash.insert(str(value.package_id), value)
            print('Package:', value.package_id, 'was', value.delivery_status, 'at', value.address, value.city + ',',
                  value.state, value.address_zip, 'at', str(delivery_time) + '. The weight is:', value.size)
        else:
            # else shows package still at hub
            value.delivery_status = 'At hub'
            if value.package_id == '9':
                value.address = '300 State St (Wrong address)'
                value.address_zip = '84103'
            calculateDistances.my_hash.insert(str(value.package_id), value)
            print('Package:', value.package_id, 'is currently', value.delivery_status, 'and will be sent out at',
                  delivery_start, 'to', value.address, value.city + ',',
                  value.state, value.address_zip + '. The weight is:', value.size)
