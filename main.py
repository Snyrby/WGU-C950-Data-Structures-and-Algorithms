# Shawn Ruby Student ID: 001345550
import time

import package_delivery
from calculateDistances import get_total_distance
if __name__ == '__main__':
    print("\nWelcome to C950: Shortest Path:")
    # calls each function to calculate the shortest path for each truck
    package_delivery.first_truck_data()
    package_delivery.second_truck_data()
    package_delivery.third_truck_data()

    # loop until user is satisfied O(1)
    def first_input():
        is_exit = True
        while is_exit:
            print("\nOptions:")
            print("1. View Screenshots")
            print("2. View packages at a specific time")
            print("3. View total route distance")
            print("4. Exit the Program")
            option = input("Choose an option (1, 2, 3, or 4): ")
            if option == "1":
                screenshot_input()
            elif option == "2":
                certain_package_input()
            elif option == "3":
                print("\nThe total route distance is:", get_total_distance())
            elif option == "4":
                is_exit = False
                exit()
            else:
                print("Wrong option, please try again!")

    # input regarding screenshots O(1)
    def screenshot_input():
        is_exit = True
        while is_exit:
            print("\nOptions:")
            print("1. Screenshot at 08:45")
            print("2. Screenshot at 09:50")
            print("3. Screenshot at 12:45")
            print("4. Go back to previous selection")
            print("5. Exit the Program")
            option = input("Chose an option (1,2,3,4 or 5): ")
            if option == "1":
                # calls the function that shows screenshot at 8:45
                package_delivery.screen_shot('08:45:00')
            elif option == "2":
                # calls the function that shows screenshot at 9:50
                package_delivery.screen_shot('09:50:00')
            elif option == "3":
                # calls the function that shows screenshot at 12:45
                package_delivery.screen_shot('12:45:00')
            elif option == "4":
                first_input()
            elif option == "5":
                is_exit = False
                exit()
            else:
                print("Wrong option, please try again!")

    # input regarding certain time O(1)
    def certain_package_input():
        incorrect = True
        while incorrect:
            option = input("\nEnter the time you would like to view (HH:MM) or (HH:MM:SS): ")
            try:
                time.strptime(option, '%H:%M:%S')
                package_delivery.screen_shot(option)
                incorrect = False
            except:
                try:
                    time.strptime(option, '%H:%M')
                    package_delivery.screen_shot(option)
                    incorrect = False
                except:
                    print("Wrong option, please try again!")
    first_input()
