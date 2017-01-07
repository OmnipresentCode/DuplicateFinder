import os
import sys, getopt
import time

showProgress = False
NOT_FOUND = -1

BEFORE = -1
SAME = 0
AFTER = 1

def getDirsAndFiles(path) :
    lastDir = os.getcwd()

    dirs = []
    files = []

    try :
        os.chdir(path)
        dirList = os.listdir(path);

        for item in dirList:
            if os.path.isdir(os.path.abspath(item)):
                dirs.append(os.path.abspath(item))
            else:
                files.append(item)
            #END-IF
        #END-FOR
    except WindowsError:
        print("Cannot access %s" % path)
    #END-TRY

    os.chdir(lastDir)
    return (dirs,files)
#END-DEF

def printByFile(dupes):
    mess = ""
    for dupe in dupes :
        count = 0
        for item in dupe :
            if count == 0 :
                mess += "\r\nFilename: %s \r\nLocations: \r\n" % item
            else :
                mess += "\t%s\r\n" % item
            #END-IF
            count += 1

        #END-FOR
    #END-FOR
    return mess
#END-DEF

def printByDirectory(dupes):

    dirList = []
    mess = ""

    for dupe in dupes :
        counter = 0
        filename = ""
        for item in dupe :
            found = False
            if counter == 0 :
                filename = item
            else :
                for i in dirList :
                    if item == i[0] :
                        i.append(filename)
                        found =True
                    #END-IF
                #END-FOR

                if found == False :
                    dirList.append([item, filename])
                #END-IF
            #END-IF
            counter += 1
        #END-FOR
    #END-FOR
    dirList.sort()


    for item in dirList :
        counter = 0
        for i in item :
            if counter == 0 :
                mess += "\r\nDirectory: %s\r\nFiles:\r\n" % i
            else :
                mess += "\t%s\t\r\n" % i
            #END-IF
            counter += 1
        #END-FOR

    #END-FOR
    return mess
#END-DEF

def addItem(listList, itemList) :

    if len(listList) == 0 :
        listList.insert(0,itemList)
        return 0
    elif len(listList) == 1 :
        if compareKeys(itemList, listList[0]) == BEFORE :
            listList.insert(0,itemList)
            return 0
        else:
            listList.insert(1,itemList)
            return 1
        #END-IF
    #END-IF

    left = 0
    right = len(listList) - 1
    middle = 0

    notFound = True
    counter = 0
    while True :
        counter += 1
        if(counter > 100) :
            print("left = %d, right = %d, middle = %d" % (left,right,middle))
        middle = (left + right) / 2

        if middle == len(listList) - 1 :
            listList.append(itemList)
            return middle + 1
        elif middle == 0 :
            listList.insert(0, itemList)
            return 0
        elif compareKeys(itemList, listList[middle]) == AFTER and compareKeys(itemList, listList[middle + 1]) == BEFORE :
            listList.insert(middle + 1, itemList)
            return middle + 1
        elif compareKeys(itemList, listList[middle]) == BEFORE :
            right = middle
        else :
            left = middle + 1
        #END-IF
    #END-WHILE
    return middle
#END-DEF

#Returns BEFORE, SAME, or AFTER in reference to the alphabetical heirachy
#of item 1 to item 2
def compareKeys(itemList1, itemList2) :
    if itemList1[0] == itemList2[0] :
        return SAME
    elif sorted([itemList1[0], itemList2[0]])[0] == itemList1[0] :
        return BEFORE
    else:
        return AFTER
    #END-IF
#END-DEF

def binarySearch(listList, key) :
    if len(listList) == 0 :
        return NOT_FOUND

    left = 0
    right = len(listList) - 1
    middle = 0

    notFound = True

    while notFound and left < right :
        middle = (right + left) / 2

        if compareKeys([key], listList[middle]) == SAME:
            notFound = False
        else :
            if compareKeys([key], listList[middle]) == BEFORE :
                right = middle
            else :
                left = middle + 1
            #END-IF
        #END-IF
    #END-WHILE

    if compareKeys([key], listList[middle]) != SAME :
        middle = NOT_FOUND
    #END-IF
    return middle
#END-DEF

def getDupes(path):

    print("Getting dupes in %s\r\nTo abort press 'ctrl+c'" % path)

    dupes = []
    firstInstances = []
    dirStack = [path]

    counter = 0
    root = os.getcwd()

    while len(dirStack) > 0 :
        counter = counter + 1

        if showProgress and counter % 50 == 0 :
            print("working... \r\n\t%d directories checked" % counter)

        currDir = dirStack.pop()
        os.chdir(currDir)

        dirList, fileList = getDirsAndFiles(currDir)

        if(len(dirList) > 0) :
            for item in dirList :
                dirStack.append(item)
            #END-FOR
        #END-IF
        for item in fileList :
            found = False
            index = binarySearch(dupes, item)
            if index != NOT_FOUND :
                dupes[index].append(currDir)
                found = True
            #END-IF
            if found != True :
                index =  binarySearch(firstInstances, item)
                if index != NOT_FOUND :
                    addItem(dupes, [item, firstInstances[index][1], currDir])
                    found = True
                else :
                    addItem(firstInstances, [item, currDir])
                #END-IF
            #END-IF
        #END-FOR
    #END-WHILE

    os.chdir(root)
    return dupes
#END-DEF


#Start program
helpStr = "python DuplicateFinder.py -d <root directory>\r\n \
            \t-f or --fileView            change the output to be file focused\
        \r\n\t-d <root> or --dir <root>   set the direcory to start from\
        \r\n\t-h or --help                print manual (this paragraph)"


directoryMode = False
output = ""
directory = raw_input("Root Directory : ")
if "y" in raw_input("Directory View Mode? (y/n) ") :
    directoryMode = True
#END-IF
if "y" in raw_input("Output to File?(y/n) ") :
    output = raw_input("Filename: ")
#END-IF

startTime = time.time()

dupes = getDupes(os.path.abspath(directory))

endTime = time.time()

if directoryMode == True :
    mess = printByDirectory(dupes)
else :
    mess = printByFile(dupes)
#END-IF
if output == "" :
    print(mess)
else :
    filePath = os.getcwd() +"\\"+ output
    print("\r\nOutputing to %s" % filePath)
    print(mess)
    f = open(filePath, "w")
    f.write(mess)
    f.close()
#END-IF

print("\r\nProgram Ended Succesfully")
print("\r\nRuntime = %d seconds\r\n" % (endTime - startTime))

raw_input("Press Enter when finished")
#END-PROGRAM
