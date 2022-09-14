import csv
from HashTable import ChainingHashTable


class Package:
    def __init__(self, package_id, address, city, state, address_zip, delivery, size, note, delivery_start,
                 current_location, delivery_status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.address_zip = address_zip
        self.delivery = delivery
        self.size = size
        self.note = note
        self.delivery_start = delivery_start
        self.current_location = current_location
        self.delivery_status = delivery_status

    def __str__(self):  # overwite print(Package) otherwise it will print object reference
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address, self.city, self.state,
                                                               self.address_zip, self.delivery, self.size, self.note,
                                                               self.delivery_start, self.current_location,
                                                               self.delivery_status)


# Read CSV files
def load_data(file_name, package_hash):
    with open(file_name) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        next(read_csv)  # skip header

        # Insert values from csv file into key/value pairs of the hash table -> O(n)
        for package in read_csv:
            package_id = package[0]
            address = package[1]
            city = package[2]
            state = package[3]
            address_zip = package[4]
            delivery = package[5]
            size = package[6]
            note = package[7]
            delivery_start = ''
            current_location = ''
            delivery_status = 'At hub'

            # package object
            value = Package(package_id, address, city, state, address_zip, delivery, size, note, delivery_start,
                            current_location, delivery_status)

            # insert each package into hash
            package_hash.insert(package_id, value)

            # Conditional statements to determine which truck a package should be located and
            # put these packages into a nested list for quick indexing

            # Correct incorrect package details
            if package_id == '9':
                final_delivery.append(value)

            # First truck's first delivery
            if delivery != 'EOD':
                if note.__contains__('Must') or note.__contains__('None'):
                    if len(first_delivery) <= 16:
                        first_delivery.append(value)
                    else:
                        second_delivery.append(value)

            # Second truck's delivery
            if note.__contains__('Can only be') or note.__contains__('Delayed'):
                second_delivery.append(value)

            # Check remaining packages
            if value not in first_delivery and value not in second_delivery and value not in final_delivery:
                if len(second_delivery) < len(final_delivery):
                    second_delivery.append(value)
                else:
                    final_delivery.append(value)


first_delivery = []  # first truck delivery
second_delivery = []  # second truck delivery
final_delivery = []  # final truck delivery


# Get packages on the first delivery -> O(1)
def get_first_delivery():
    return first_delivery


# Get packages on the second delivery -> O(1)
def get_second_delivery():
    return second_delivery


# Get packages on the final delivery -> O(1)
def get_final_delivery():
    return final_delivery


