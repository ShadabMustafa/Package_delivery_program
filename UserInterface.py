# The User Interface Module, holds the user interaction functionality.

import os
from Delivery import *
import datetime

# Simple class to hold colors.
class style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# Basic print program short cut, should save time for debugging.
# The space and time complexities are both O(1) respectively.
def p (x : str) -> None:
    print(x)

# Shortcut for returning a variable.
# The space and time complexities are both O(1) respectively.
def r(x) -> None:
    return x

# Confirms File has been imported by Main.py.
p(style.YELLOW + '\n UserInterface Start')

# Simple function for printing the opening sequence of UserInterface.py.
# The space and time complexities are both O(1) respectively.
def OpeningSequence() -> None:
    p(style.BLUE + 'WGUPS Delivery Status Program Start! \n')
    print(style.RESET + 'Truck 1 has a total distance of', "{0:.2f}".format(totalDistance(1), 2), 'miles. \n')
    print(style.RESET + 'Truck 2 has a total distance of', "{0:.2f}".format(totalDistance(2), 2), 'miles. \n')
    print(style.RESET + 'Truck 3 has a total distance of', "{0:.2f}".format(totalDistance(3), 2), 'miles. \n')
    print(style.RESET + 'The total distance for all three trucks is', "{0:.2f}".format(totalDistance(4), 2), 'miles. \n')

OpeningSequence()

userInput = input(style.RED + """
Please choose an option, do so by typing and entering the number or word matching your desired option :
1 : Look up a single package's delivery status information at a certain time.
2 : Find the delivery status information of all packages at a certain time.
3 : Exit Program, except when typing in package id for option 1.
Quit : Exits Program under any circumstances!
""")

# Overall worst case space and time complexity of the entire loop is O(N^2).
# Best case is O(1) for both space and time.
while userInput != '3' or userInput != 'Quit':

    # The Case for Option 1.
    # Gets the information for a single package at a particular time.
    # The space and time complexities are both O(N) respectively.
    if userInput == '1':
        try:
            pkgID = input('Please enter a package ID from 1 to 40: ')
            firstTime = getter_HashMap().read(str(pkgID))[9]
            secondTime = getter_HashMap().read(str(pkgID))[10]
            inputTime = input('Please enter a time (HH:MM:SS): ')
            (hrs, mins, secs) = inputTime.split(':')
            userTimeConversion = datetime.timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))
            (hrs, mins, secs) = firstTime.split(':')
            firstTimeConversion = datetime.timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))
            (hrs, mins, secs) = secondTime.split(':')
            secondTimeConversion = datetime.timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))


            # Finds out if the package has yet to depart the hub.
            if firstTimeConversion >= userTimeConversion:

                getter_HashMap().read(str(pkgID))[10] = 'At Hub'
                getter_HashMap().read(str(pkgID))[9] = 'Departs at ' + firstTime

                # Print the package's current information.
                p(
                    f'Package ID: {getter_HashMap().read(str(pkgID))[0]}\n'
                    f'Street address: {getter_HashMap().read(str(pkgID))[2]}\n'
                    f'Mandatory Delivery Time: {getter_HashMap().read(str(pkgID))[6]}\n'
                    f'Package weight: {getter_HashMap().read(str(pkgID))[7]}\n'
                    f'Status of Truck: {getter_HashMap().read(str(pkgID))[9]}\n'
                    f'Status of Delivery: {getter_HashMap().read(str(pkgID))[10]}\n'
                )

            # Finds  out if the package has yet to be delivered but has left the hub.
            elif firstTimeConversion <= userTimeConversion:
                if userTimeConversion < secondTimeConversion:
                    getter_HashMap().read(str(pkgID))[10] = 'In transit'
                    getter_HashMap().read(str(pkgID))[9] = 'Departed at ' + firstTime

                    # Print the package's current information.
                    p(
                        f'Package ID: {getter_HashMap().read(str(pkgID))[0]}\n'
                        f'Street address: {getter_HashMap().read(str(pkgID))[2]}\n'
                        f'Mandatory Delivery Time: {getter_HashMap().read(str(pkgID))[6]}\n'
                        f'Package weight: {getter_HashMap().read(str(pkgID))[7]}\n'
                        f'Status of Truck: {getter_HashMap().read(str(pkgID))[9]}\n'
                        f'Status of Delivery: {getter_HashMap().read(str(pkgID))[10]}\n'
                    )

                # Print the package's current information.
                else:
                    getter_HashMap().read(str(pkgID))[10] = 'Delivered at ' + secondTime
                    getter_HashMap().read(str(pkgID))[9] = 'Departed at ' + firstTime

                    # Print the package's current information.
                    p(
                        f'Package ID: {getter_HashMap().read(str(pkgID))[0]}\n'
                        f'Street address: {getter_HashMap().read(str(pkgID))[2]}\n'
                        f'Mandatory Delivery Time: {getter_HashMap().read(str(pkgID))[6]}\n'
                        f'Package weight: {getter_HashMap().read(str(pkgID))[7]}\n'
                        f'Status of Truck: {getter_HashMap().read(str(pkgID))[9]}\n'
                        f'Status of Delivery: {getter_HashMap().read(str(pkgID))[10]}\n'
                    )
        except ValueError:
            p(style.UNDERLINE + 'Invalid Input!, will exit program!')
            exit()

    # The Case for Option 2.
    # Gets the information for all packages at a particular time .
    # The space and time complexities are both O(N) respectively.
    elif userInput == '2':
        try:
            inputTime = input('Please enter a time (HH:MM:SS): ')
            (hrs, mins, secs) = inputTime.split(':')
            userTimeConversion = datetime.timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))

            p(style.BLUE + ' \n Truck 1 leaves at or has left at  08:00:00')
            p(style.GREEN + ' Truck 2 leaves at or has left at 09:05:00')
            p(style.RED + ' Truck 3 leaves at or has left at 11:00:00 \n')

            # Both Space and Time Complexities are O(N^2).
            for pkgID in range(1, 41):
                try:
                    firstTime = getter_HashMap().read(str(pkgID))[9]
                    secondTime = getter_HashMap().read(str(pkgID))[10]
                    (hrs, mins, secs) = firstTime.split(':')
                    firstTimeConversion = datetime.timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))
                    (hrs, mins, secs) = secondTime.split(':')
                    secondTimeConversion = datetime.timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))
                except ValueError:
                    pass

                # Determine which packages have exited the hub.
                if firstTimeConversion >= userTimeConversion:
                    getter_HashMap().read(str(pkgID))[10] = 'At Hub'
                    getter_HashMap().read(str(pkgID))[9] = 'Departs at ' + firstTime

                    # Print the package's current information.
                    p(
                        f'Package ID: {getter_HashMap().read(str(pkgID))[0]} |  '
                        f'Status of Delivery: {getter_HashMap().read(str(pkgID))[10]} |    '
                        f'Street address: {getter_HashMap().read(str(pkgID))[2]} |  '
                        f'Mandatory Delivery Time: {getter_HashMap().read(str(pkgID))[6]} |  '
                        f'Package weight: {getter_HashMap().read(str(pkgID))[7]} |  '
                        f'Status of Truck: {getter_HashMap().read(str(pkgID))[9]} |    '
                    )

                # Determines which packages have exited the hub but have not been delivered.
                elif firstTimeConversion <= userTimeConversion:
                    if userTimeConversion < secondTimeConversion:
                        getter_HashMap().read(str(pkgID))[10] = 'In transit'
                        getter_HashMap().read(str(pkgID))[9] = 'Departed at ' + firstTime

                        # Print the package's current information.
                        p(
                            f'Package ID: {getter_HashMap().read(str(pkgID))[0]} |  '
                            f'Status of Delivery: {getter_HashMap().read(str(pkgID))[10]} |    '
                            f'Street address: {getter_HashMap().read(str(pkgID))[2]} |  '
                            f'Mandatory Delivery Time: {getter_HashMap().read(str(pkgID))[6]} |  '
                            f'Package weight: {getter_HashMap().read(str(pkgID))[7]} |  '
                            f'Status of Truck: {getter_HashMap().read(str(pkgID))[9]} |    '
                        )

                    # Determines which packages have been delivered successfully.
                    else:
                        getter_HashMap().read(str(pkgID))[10] = 'Delivered at ' + secondTime
                        getter_HashMap().read(str(pkgID))[9] = 'Departed at ' + firstTime

                        # Print the package's current information.
                        p(
                            f'Package ID: {getter_HashMap().read(str(pkgID))[0]} |  '
                            f'Status of Delivery: {getter_HashMap().read(str(pkgID))[10]} |    '
                            f'Street address: {getter_HashMap().read(str(pkgID))[2]} |  '
                            f'Mandatory Delivery Time: {getter_HashMap().read(str(pkgID))[6]} |  '
                            f'Package weight: {getter_HashMap().read(str(pkgID))[7]} |  '
                            f'Status of Truck: {getter_HashMap().read(str(pkgID))[9]} |    '
                        )
        except IndexError:
            print(IndexError)
            exit()
        except ValueError:
            p(style.UNDERLINE + 'Invalid Input!, will exit program!')
            exit()


    # The Case for Option 3.
    # This ends the program.
    elif userInput == '3':
        p(style.UNDERLINE + 'Exiting program as you have inputted 3')
        exit()

    # The Case for Quit Option.
    # This ends the program.
    elif userInput == 'Quit':
        p(style.UNDERLINE + 'Exiting program as you have inputted Quit')
        exit()

    # The Error case.
    # Tells the user that they have inputted incorrect an invalid entry.
    else:
        p(style.UNDERLINE + 'Invalid Input!, will exit program!')
        exit()