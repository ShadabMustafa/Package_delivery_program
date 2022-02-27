
# This file is used to execute the delivery process.
from Loading import *
import csv
import datetime
import logging


# A Total of three various loggers are setup here for debugging and confirming that the program is functioning as intended.

# A Logger used for various distance functions.
Distances_logger = logging.getLogger(__name__)

Distances_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('Distances.log')

file_handler.setFormatter(formatter)

Distances_logger.addHandler(file_handler)

#A test message for distance logger.
Distances_logger.debug('___________________Distances LOGGER PROCESS STARTING!____________________________')


# A Logger used for various delivery or higher level functions.
Delivery_logger = logging.getLogger('deli')

Delivery_logger.setLevel(logging.DEBUG)

formatter2 = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler2 = logging.FileHandler('Delivery.log')

file_handler2.setFormatter(formatter2)

Delivery_logger.addHandler(file_handler2)

#A test message for distance logger.
Delivery_logger.debug('___________________Delivery LOGGER PROCESS STARTING!____________________________')


# A logger used to see the final sorted lists prior to being stored in the hashmap.
finalLogger = logging.getLogger('final')

finalLogger.setLevel(logging.DEBUG)

formatter3 = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler3 = logging.FileHandler('Final.log')

file_handler3.setFormatter(formatter3)

finalLogger.addHandler(file_handler3)

#A test message for final logger.
finalLogger.debug('___________________FINAL LOGGER PROCESS STARTING!____________________________')







print("Delivery starting")


# A csv file for numerical distances is scanned in.
with open('DistanceData.csv') as distCSV:
    distanceCSV_Data = csv.reader(distCSV, delimiter=',')
    distanceCSV_Data = list(distanceCSV_Data)
    Distances_logger.debug('Distance LENGTH data csv opened')

# A csv file for location names and addresses is scanned in.
with open('LocationData.csv') as locCSV:
    LocationCSV_Data = csv.reader(locCSV, delimiter=',')
    LocationCSV_Data = list(LocationCSV_Data)
    Distances_logger.debug('Distance NAME data csv opened')


# Variable for truck speed. 18 miles per an hour is the stated truck speed in assumptions.
truckSpeed= 18

# Time that the first truck leaves the hub. 8 am is the earliest time allowed according to assumptions.
firstTimeList = ['8:00:00']
# Second truck leaves 9:05 so flight delayed packages are on board. Instantaneous loading occurs according to assumptions.
secondTimeList = ['9:05:00']
# Third truck leaves 11 as it needs to wait for the first truck driver to return.
thirdTimeList = ['11:00:00']

# The following function accepts a distance value as input, then divides it by 18 as that is the truck speed.
# Subsequently it utilizes divmod to show time and appends 00 to represent seconds.
# The timestamp string(digital record of a timed event) is split and converted to a datetime timedelta object.
# Later, the datetime timedelta object is added to sum(the total distance of a truck).
# O(N) is both the space and time complexity respectively for this function.
# This function also utilizes a match case sequence for simplicity and code reusability.
def truckTime(distance:float, truckNum:int)  -> 'timedelta':
    newTime = distance / truckSpeed
    distInMin = '{0:02.0f}:{1:02.0f}'.format(*divmod(newTime * 60, 60))
    finalTime = distInMin + ':00'

    match truckNum:
        case 1 :
            firstTimeList.append(finalTime)
            sum = datetime.timedelta()
            for i in firstTimeList:
                (hrs, min, sec) = i.split(':')
                d = datetime.timedelta(hours=int(hrs), minutes=int(min), seconds=int(sec))
                sum += d
            Distances_logger.debug('check FIRST truck time func called: %s ',sum)
            return sum

        case 2 :
            secondTimeList.append(finalTime)
            sum = datetime.timedelta()
            for i in secondTimeList:
                (hrs, min, sec) = i.split(':')
                d = datetime.timedelta(hours=int(hrs), minutes=int(min), seconds=int(sec))
                sum += d
            Distances_logger.debug('check SECOND truck time func called:%s',sum)
            return sum

        case 3 :
            thirdTimeList.append(finalTime)
            sum = datetime.timedelta()
            for i in thirdTimeList:
                (hrs, min, sec) = i.split(':')
                d = datetime.timedelta(hours=int(hrs), minutes=int(min), seconds=int(sec))
                sum += d
            Distances_logger.debug('check THIRD truck time func called:%s',sum)
            return sum


# this function returns address information for use.
# Space-time complexity is O(1)
def checkAddress() -> list:
    Distances_logger.debug('check ADDRESS time func called')
    return LocationCSV_Data

# These lists represent the sorted truck delivery route.
firstSortedTruck = []
secondSortedTruck = []
thirdSortedTruck = []

# These lists represent address indexes for sorted trucks.
# '0' is inside the following lists to make sure total distance calculations remain accurate.
# '0' is the index of the WGU Depot Address in LocationData.csv .
firstTruck_AddressList = ['0']
secondTruck_AddressList = ['0']
thirdTruck_AddressList = ['0']


# Simple function for returning the Address truck index list.
# O(1) is both the space and time complexity.
def truckAddressList(x:int) -> list:
    match x:
        case 1:
            Distances_logger.debug('return optimized FIRST truck INDEX func called : %s', firstTruck_AddressList)
            return firstTruck_AddressList

        case 2:
            Distances_logger.debug('return optimized SECOND truck INDEX func called:%s', secondTruck_AddressList)
            return secondTruck_AddressList

        case 3:
            Distances_logger.debug('return optimized THIRD truck INDEX func called: %s', thirdTruck_AddressList)
            return thirdTruck_AddressList


# Simple function for returning the sorted truck list, not the Address list.
# O(1) is both the space and time complexity.
def truckSortedList(x:int) -> list:
    match x:
        case 1:
            finalLogger.debug('return optimized FIRST truck LIST func called:%s', firstSortedTruck)
            return firstSortedTruck

        case 2:
            finalLogger.debug('return optimized SECOND truck LIST func called:%s', secondSortedTruck)
            return secondSortedTruck

        case 3:
            finalLogger.debug('return optimized THIRD truck LIST func called:%s', thirdSortedTruck)
            return thirdSortedTruck


# Lists to hold the  package order prior to the nearest neighbor algorithm taking effect.
firstDelivery = []
secondDelivery = []
thirdDelivery = []

# The times below represent the times that each truck leaves the hub.
# First truck and the first driver leave at 8 as assumptions states that is the earliest time possible.
firstTime = '8:00:00'
# Second truck and the second driver leave at 9:05. This due to some packages arriving at 9:05. No extra time is spent
# loading packages at the hub according to assumptions.
secondTime = '9:05:00'
#Third truck and the first driver leave at 11 am, this due to the first truck driver having to come back to swap trucks.
# Also leaves at 11 due to having to wait for Package 9, address to be corrected around 10:20 am.
thirdTime = '11:00:00'

# Total Distance tracking variables.
firstTruck_TotalDistance = 0
secondTruck_TotalDistance = 0
thirdTruck_TotalDistance = 0


# A delivery status update function.
def statusUpdate(initialTruckLoadList:list, truckLeaveTime:str, unsortedDeliveryList:list) -> None:
    # This for loop updates the status of delivery for all packages in a truck till the truck departs the station
    # O(1) is the space complexity. O(N) is the time complexity.
    j = 0 # The loop iterator variable
    for value in initialTruckLoadList:
        initialTruckLoadList[j][9] = truckLeaveTime
        unsortedDeliveryList.append(initialTruckLoadList[j])
        j += 1
    Delivery_logger.debug('status update called : %s',unsortedDeliveryList)

# Phase 1
# This is the delivery status updating phase. The first phase of the delivery algorithm.
statusUpdate(checkLoadedPkgsTruckList(1),firstTime,firstDelivery)
statusUpdate(checkLoadedPkgsTruckList(2),secondTime,secondDelivery)
statusUpdate(checkLoadedPkgsTruckList(3),thirdTime,thirdDelivery)

# An address comparison function.
def addressComparison(deliveryList:list) -> None:
    # This for loop compares as well as confirms the addresses on a truck list to the list of addresses in the location data CSV file
    # and then adds the address index to the truck list.
    # O(N^2) is the both thee Space and time complexity respectively.
    try:
        count = 0
        for i in deliveryList:
            for r in checkAddress():
                if i[2] == r[2]:
                    deliveryList[count][1] = r[0]
            count += 1
        Delivery_logger.debug('address comparison called: %s',deliveryList)
    except IndexError:
        pass

# Phase 2
# This is the address comparison phase. The second phase of the delivery algorithm.
addressComparison(firstDelivery)
addressComparison(secondDelivery)
addressComparison(thirdDelivery)



# Function finds and returns the current distance.
# O(1) is both the space and time complexity.
def currentDist(rowValue:int = 0, columnValue:int = 0) -> float:
    dist = distanceCSV_Data[rowValue][columnValue]
    if dist == '':
        dist = distanceCSV_Data[columnValue][rowValue]
    Distances_logger.debug('check CURRENT distance func called')
    return float(dist)


# Phase 3, nearest neighbor sorting algorithm!


# Function used to add elements to the sorted packages list and sorted address index list.
# O(1) is the space and also the time complexity.
def updateSortedList_andIndex(x:int,y:str,z:str) -> None:
    match x:
        case 1:
            truckSortedList(1).append(y)
            truckAddressList(1).append(z)
        case 2:
            truckSortedList(2).append(y)
            truckAddressList(2).append(z)
        case 3:
            truckSortedList(3).append(y)
            truckAddressList(3).append(z)

# Function used to remove an element off a list.
# O(1) is the space and also the time complexity.
def removeListElement(x:list,y:int) -> None:
    x.pop(x.index(y))


# This is a simple implementation of the nearest neighbor algorithm.
# O(N^2) is the space complexity due to lists and various look up operations.
# O(N^2) is the time complexity due to recursion and loops.
# There is a separate sort function for each truck but the conceptual structure is the same for all three functions.
def nearestNeighborSort() -> None:
    pkgLength1 = len(firstDelivery)
    # This while loop makes sure the sorting function ends when all packages are sorted. Prevents an infinite loop.
    while len(truckSortedList(1)) != pkgLength1:
        # Two Parameters, one for the final delivery list and the other for the location of a package delivery site.
        # Ideally no parameters would be needed but recursion is utilized here.
        def firstSort(truckDeliveryList:list = firstDelivery, location:int =0) -> None:
            try:
                # No 2 locations have more than 14.2 miles between each other( Wheeler Historic Farm at
                # 6351 South 900 East and Salt Lake City Streets and Sanitation at
                #  2010 W 500 S).
                # No 2 locations have less than 0.4 miles between each other(Valley Regional Softball Complex at
                #  5100 South 2700 West and Taylorsville City Hall at 2600 Taylorsville Blvd).
                shortestDist,newDist = 14.2,0.4
                # The lowest value is initialized then this loop seeks a possible smaller value till
                # there is nothing left to search.
                z = 0
                while z <len(truckDeliveryList) :
                    i = truckDeliveryList[z]
                    if currentDist(location, int(i[1])) <= shortestDist:
                        Distances_logger.debug('FIRST shortest dist func found new lowest value')
                        shortestDist = currentDist(location, int(i[1]))
                        newDist = int(i[1])
                    z += 1
                # This loop adds the sorted packages and their address indexes to their respective lists which are used
                # during the final phase for updating the hashmap in a later function.
                # Also has a recursive call to find the next nearest neighboring location.
                m = 0
                while m <len(truckDeliveryList) :
                    i = truckDeliveryList[m]
                    if currentDist(location, int(i[1])) == shortestDist:
                        Distances_logger.debug('shortest dist func added new optimized lowest value for truck 1 ONE')
                        updateSortedList_andIndex(1,i,i[1])
                        removeListElement(truckDeliveryList,i)
                        location = newDist
                        firstSort(truckDeliveryList, location)
                    m += 1
            # Used to pass along errors
            except IndexError:
                Distances_logger.debug('FIRST shortest dist func index error passed')
                pass
        firstSort()

    # Repeated version of previous function for the second truck.
    pkgLength2 = len(secondDelivery)
    while len(truckSortedList(2)) != pkgLength2:
        def secondSort(truckDeliveryList:list = secondDelivery, location:int = 0) -> None:
            try:
                shortestDist,newDist = 14.2,0.4
                z = 0
                while z <len(truckDeliveryList) :
                    i = truckDeliveryList[z]
                    if currentDist(location, int(i[1])) <= shortestDist:
                        Distances_logger.debug('SECOND shortest dist func found new lowest value')
                        shortestDist = currentDist(location, int(i[1]))
                        newDist = int(i[1])
                    z += 1
                m = 0
                while m <len(truckDeliveryList) :
                    i = truckDeliveryList[m]
                    if currentDist(location, int(i[1])) == shortestDist:
                        Distances_logger.debug('shortest dist func added new optimized lowest value for truck 2 TWO')
                        updateSortedList_andIndex(2,i,i[1])
                        removeListElement(truckDeliveryList,i)
                        location = newDist
                        secondSort(truckDeliveryList, location)
                    m += 1
            except IndexError:
                Distances_logger.debug('SECOND shortest dist func index error passed')
                pass
        secondSort()


    # Repeated version of previous function for the third truck.
    pkgLength3 = len(thirdDelivery)
    while len(truckSortedList(3)) != pkgLength3:
        def thirdSort(truckDeliveryList:list = thirdDelivery, location:int =0) -> None:
            try:
                shortestDist,newDist = 14.2,0.4
                z = 0
                while z <len(truckDeliveryList) :
                    i = truckDeliveryList[z]
                    if currentDist(location, int(i[1])) <= shortestDist:
                        Distances_logger.debug('Third shortest dist func found new lowest value')
                        shortestDist = currentDist(location, int(i[1]))
                        newDist = int(i[1])
                    z += 1
                m = 0
                while m <len(truckDeliveryList) :
                    i = truckDeliveryList[m]
                    if currentDist(location, int(i[1])) == shortestDist:
                        Distances_logger.debug('shortest dist func added new optimized lowest value for truck 3 THREE')
                        updateSortedList_andIndex(3,i,i[1])
                        removeListElement(truckDeliveryList,i)
                        location = newDist
                        thirdSort(truckDeliveryList, location)
                    m += 1
            except IndexError:
                Distances_logger.debug('Third shortest dist func index error passed')
                pass
        thirdSort()

nearestNeighborSort()


#  Function is used in the calculation of the total distance a truck.
# O(1) is both the space and time complexity.
def totalDistCalc(rowValue:int = 0, columnValue:int = 0, distanceSum:float = 0 ) -> float:
    dist = distanceCSV_Data[rowValue][columnValue]
    if dist == '':
        dist = distanceCSV_Data[columnValue][rowValue]
    distanceSum += float(dist)
    Distances_logger.debug('check TOTAL distance func called')
    return distanceSum



# Phase 4, total distance calculation phase!

# The function takes the values in a truck and runs them through various utility functions and is also used to calculate the total distance of a truck.
# It also transfers values into the hashmap for faster lookup speeds in other files.
# The space and time complexity are both O(N) respectively.
def distanceCalculation(truck:int) -> None :
    match truck:
        case 1:
            # For first truck.
            global firstTruck_TotalDistance
            firstTruck_pkgID = 0
            for i in range(len(truckAddressList(1))):
                try:
                    # Computes the total distance traversed by a truck.
                    firstTruck_TotalDistance = totalDistCalc(int(truckAddressList(1)[i]),
                                                             int(truckAddressList(1)[i + 1]),
                                                             firstTruck_TotalDistance)

                    # Computes the distance for each package delivery along the route.
                    deliveryPKG = truckTime(currentDist(int(truckAddressList(1)[i]),
                                                        int(truckAddressList(1)[
                                                                                      i + 1])), 1)

                    truckSortedList(1)[firstTruck_pkgID][10] = (str(deliveryPKG))
                    getter_HashMap().modify(int(truckSortedList(1)[firstTruck_pkgID][0]), firstDelivery)
                    firstTruck_pkgID += 1
                except IndexError:
                    pass
            finalLogger.debug('FIRST distCalc called,  list: %s', truckAddressList(1))


        case 2:
            # For second truck.
            global secondTruck_TotalDistance
            secondTruck_pkgID = 0
            for i in range(len(truckAddressList(2))):
                try:
                    secondTruck_TotalDistance = totalDistCalc(int(truckAddressList(2)[i]),
                                                              int(truckAddressList(2)[i + 1]),
                                                              secondTruck_TotalDistance)

                    deliveryPKG = truckTime(currentDist(int(truckAddressList(2)[i]),
                                                        int(truckAddressList(2)[
                                                                                      i + 1])), 2)

                    truckSortedList(2)[secondTruck_pkgID][10] = (str(deliveryPKG))
                    getter_HashMap().modify(int(truckSortedList(2)[secondTruck_pkgID][0]), secondDelivery)
                    secondTruck_pkgID += 1
                except IndexError:
                    pass
            finalLogger.debug('Second distCalc called,  list: %s', truckAddressList(2))



        case 3:
            # For third truck.
            global thirdTruck_TotalDistance
            thirdTruck_pkgID = 0
            for i in range(len(truckAddressList(3))):
                try:
                    thirdTruck_TotalDistance = totalDistCalc(int(truckAddressList(3)[i]),
                                                             int(truckAddressList(3)[i + 1]),
                                                             thirdTruck_TotalDistance)



                    deliveryPKG = truckTime(currentDist(int(truckAddressList(3)[i]),
                                                        int(truckAddressList(3)[
                                                                                      i + 1])), 3)

                    truckSortedList(3)[thirdTruck_pkgID][10] = (str(deliveryPKG))
                    getter_HashMap().modify(int(truckSortedList(3)[thirdTruck_pkgID][0]), thirdDelivery)
                    thirdTruck_pkgID += 1
                except IndexError:
                    pass
            finalLogger.debug('Third distCalc called,  list: %s', truckAddressList(3))




distanceCalculation(1)
distanceCalculation(2)
distanceCalculation(3)

# Following function returns the total distance traveled by each truck and  all trucks.
# The space and time complexity are both O(1) respectively.
def totalDistance(x):
    totalDistance = firstTruck_TotalDistance + secondTruck_TotalDistance + thirdTruck_TotalDistance

    match x:
        case 1:
            return firstTruck_TotalDistance
        case 2:
            return secondTruck_TotalDistance
        case 3:
            return thirdTruck_TotalDistance
        case 4:
            return totalDistance