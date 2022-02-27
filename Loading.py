
# This file is used to load packages into truck lists which will be used later during the delivery process.
import csv
from HashTable import *
import logging

# Logger used to confirm that this file is working as intended.
Loading_logger = logging.getLogger(__name__)
Loading_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('Loading_Main.log')
file_handler.setFormatter(formatter)

Loading_logger.addHandler(file_handler)

# The test message for the logger.
Loading_logger.debug('__________________Loading LOGGER PROCESS STARTING!____________________________')

# Used to confirm Loading.py was successfully started/imported.
print("Loading started")

# Declarations
# Uses the Hashmap class to create an object of Hashmap.
addedToHashMap = HashTable()

# A simple list for the first truck delivery.
firstTruckList = []

# A simple list for the second truck delivery.
secondTruckList = []

# A simple list for the third truck delivery.
firstDriver_ThirdTruckList = []


# A very simple function used to read the complete list of values at the start of the day.
# O(1) is both the space and time complexity.
def getter_HashMap() -> HashTable: return addedToHashMap


# A very simple function used to read the list of packages loaded in a specific truck.
# O(1) is both the space and time complexity.
def checkLoadedPkgsTruckList(x:int) -> list:
    match x:
        case 1:
            return firstTruckList

        case 2:
            return secondTruckList

        case 3:
            return firstDriver_ThirdTruckList


# Main function loop for Loading. Used for reading in csv values and loading packages.
# O(N) is the space and time complexity respectively.
def Loading_Main() -> None:
    with open('PackagesData.csv') as pkgCSV:
        readCSV = csv.reader(pkgCSV, delimiter=',')

        #Package limit for all trucks is 16 as stated in Assumptions.
        Package_Space_Truck1 = 16
        Package_Space_Truck2 = 16
        Package_Space_Truck3 = 16

        # O(1) is the space and time complexity respectively.
        def PrioritizePkgs(cases:int,value:list) -> None:
            global Package_Space_Truck1
            global Package_Space_Truck2
            global Package_Space_Truck3
            # Match case function used for logging every possible case and adding values to truck lists.
            match cases:
                case 1 :
                    secondTruckList.append(value) # added to the list that represents the second truck
                    Loading_logger.debug('stuffed in the SECOND(#2) truck,Case statement 1: %s', row[0])

                case 2 :
                    firstTruckList.append(value)  # added to the list that represents the first truck
                    Loading_logger.debug('stuffed in the FIRST(#1) truck, Case statement 2: %s', row[0])

                case 3 :
                    secondTruckList.append(value) # added to the list that represents the second truck
                    Loading_logger.debug('stuffed in the SECOND(#2) truck,Case statement 3: %s', row[0])

                case 4 :
                    value[2] = '410 S State St'
                    value[5] = '84111'
                    firstDriver_ThirdTruckList.append(value) # added to the list that represents the third truck
                    Loading_logger.debug('stuffed in the THIRD(#3) truck for wrong address or pkg 9,Case statement 4: %s', row[0])

                case 5 :
                    firstDriver_ThirdTruckList.append(value) # added to the list that represents the third truck
                    Loading_logger.debug('stuffed in the THIRD(#3) truck as it had more space than truck2,Case statement 5: %s', row[0])

                case 6 :
                    secondTruckList.append(value) # added to the list that represents the second truck
                    Loading_logger.debug('stuffed in the SECOND(#2) truck as it had more space than truck3,Case statement 6: %s', row[0])


        # Reads in values from the CSV file and then inserts them into a key-value pairs hashmap.
        # The nested dictionary inside the Hash Table is composed of the scanned CSV file values.
        # O(N) is the Space and time complexity respectively.

        for row in readCSV:
            packageID_rowValue = row[0]
            address_rowValue = row[1]
            city_rowValue = row[2]
            state_rowValue = row[3]
            zip_rowValue = row[4]
            delivery_rowValue = row[5]
            size_rowValue = row[6]
            note_rowValue = row[7]
            deliveryStart = ''
            addressLocation = ''
            deliveryStatus = 'At hub'

            #11 fields in iterate value(0<->10 index)
            iterateValue = [packageID_rowValue, addressLocation, address_rowValue, city_rowValue, state_rowValue,
                             zip_rowValue, delivery_rowValue, size_rowValue, note_rowValue, deliveryStart,
                             deliveryStatus]
            key = packageID_rowValue
            value = iterateValue

            Loading_logger.debug('The iteration value being logged,%s', iterateValue)


            # This is a sequence of if statements which help fill up the packages holding list for each truck.
            # All data is later stored in the hashtable for quick lookup and sorting times for any and all package information.

            # Used to make sure that packages for Truck 2 only go on truck 2.
            if 'Can only be on truck 2' in value[8]:
                if Package_Space_Truck2 > 0:
                    PrioritizePkgs(1,value)
                    Package_Space_Truck2 = Package_Space_Truck2 - 1

            # Used to make sure that packages that must go together, do go together.
            if value[6] != 'EOD':
                if 'Must be delivered with 15 & 19' in value[8] or 'None' in value[8] or 'Must be delivered with 13 & 19' in value[8] or 'Must be delivered with 13 & 15' in value[8]:
                    if  Package_Space_Truck1 > 0:
                        PrioritizePkgs(2, value)
                        Package_Space_Truck1 = Package_Space_Truck1 - 1

            # Used to make sure that delayed packages go on truck 2 as it leaves at 9:05(see Delivery.py)
            if 'Delayed on flight---will not arrive to depot until 9:05 am' in value[8]:
                if Package_Space_Truck2 > 0:
                    PrioritizePkgs(3, value)
                    Package_Space_Truck2 = Package_Space_Truck2 - 1

            # Wrong address correction occurs at 10:20 AM and third truck leaves at 11 AM, see #Delivery.
            if 'Wrong address listed' in value[8]:
                if Package_Space_Truck3 > 0:
                    # value[2] = '410 S State St'
                    # value[5] = '84111'
                    # firstDriver_ThirdTruckList.append(value)
                    PrioritizePkgs(4,value)
                    Package_Space_Truck3 = Package_Space_Truck3 - 1

            # Final group of if statements to store packages that are left over to either Truck 2 or Truck 3.
            # Following if statements try to make sure secondTruckList and third_truck remain equally balanced.
            if value not in firstTruckList and value not in secondTruckList and value not in firstDriver_ThirdTruckList:
                if len(secondTruckList) >= len(firstDriver_ThirdTruckList):
                    if Package_Space_Truck3 > 0:
                        # firstDriver_ThirdTruckList.append(value)
                        PrioritizePkgs(5, value)
                        Package_Space_Truck3 = Package_Space_Truck3 - 1
                else:
                    if Package_Space_Truck2 > 0:
                        PrioritizePkgs(6, value)
                        # secondTruckList.append(value)
                        Package_Space_Truck2 = Package_Space_Truck2 - 1

            addedToHashMap.add(key, value)  # Inserts all values to the hash table

        # used to confirm in logs that only 16 packages at best are stored in any one truck.
        Loading_logger.debug('Space remaining on Truck 1: %s', Package_Space_Truck1)
        Loading_logger.debug('Space remaining on Truck 2: %s', Package_Space_Truck2)
        Loading_logger.debug('Space remaining on Truck 3: %s', Package_Space_Truck3)

        # used to see each truck list's total entries
        Loading_logger.debug('Truck 1 list: %s', firstTruckList)
        Loading_logger.debug('Truck 2 list: %s', secondTruckList)
        Loading_logger.debug('Truck 3 list: %s', firstDriver_ThirdTruckList)


        Loading_logger.debug('___________________END OF Loading MAIN LOGGER THING____________________________')


# Function is called during the import statement in Delivery.py.
Loading_Main()




