import os
import sys, getopt

showProgress = False

def getDirsAndFiles(path) :
    lastDir = os.getcwd()

    os.chdir(path)

    dirList = os.listdir(path);

    dirs = []
    files = []

    for item in dirList:
        if os.path.isdir(os.path.abspath(item)):
            dirs.append(os.path.abspath(item))
        else:
            files.append(item)
        #END-IF
    #END-FOR

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

def getDupes(path):

    print("Getting dupes in " + path)

    dupes = []
    firstInstances = []
    dirStack = [path]

    counter = 0

    while len(dirStack) > 0 :
        counter = counter + 1

        if showProgress and counter % 50 == 0 :
            print("working... \r\n\t%d directories checked" % counter)

        currDir = dirStack.pop()

        dirList, fileList = getDirsAndFiles(currDir)

        if(len(dirList) > 0) :
            for item in dirList :
                dirStack.append(item)
            #END-FOR
        #END-IF

        for item in fileList :
            found = False

            for d in dupes :
                if item == d[0] :
                    d.append(currDir)
                    found = True
                #END-IF
            #END-FOR

            if found == False:
                for f in firstInstances :
                    if item == f[0] :
                        found = True
                        #append first instance
                        dupes.append(f)
                        #add current directory holding current instance
                        dupes[len(dupes)-1].append(currDir)
                    #END-IF
                #END-FOR
            #END-IF

            if found == False :
                firstInstances.append([item, currDir])

        #END-FOR

    #END-WHILE

    dupes.sort()

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
dupes = getDupes(os.path.abspath(directory))

if directoryMode == True :
    mess = printByDirectory(dupes)
else :
    mess = printByFile(dupes)
#END-IF
if output == "" :
    print(mess)
else :
    filePath = os.getcwd() +"\\"+ output
    print(filePath)
    f = open(filePath, "w")
    f.write(mess)
    f.close()
#END-IF

raw_input("Press Enter when finished")

print("\r\nProgram Ended Succesfully")
#END-PROGRAM
