import pickle, sys


#function to make a new object in pickle
def saveObj(name, option, objDict):
    #test for type is probably redunant, but can't hurt
    if type(name) == str:
        if type(option) == str:
            # only three type of strings will be accepted
            ### SELL or TRADE or BUY
            # any other entry won't be saved
            if option == "SELL" or option == "TRADE" or option == "BUY":
                if option == "BUY":
                    # make an empty dict
                    buyingthingdic = {}
                    # param: option is either SELL or TRADE or BUY
                    #        buyingthingdic is the empty dictionary
                    #        FALSE: is a flag that is False per default and decides whether entry gets an additional TRADE entry
                    objDict.update({name: (option, buyingthingdic, False)})
                    # save pickle
                    pickle.dump(objDict, open("hzdObjList.p", "wb"))
                elif option == "TRADE":
                    buyingthinglist = []
                    objDict.update({name: (option, buyingthinglist)})
                    pickle.dump(objDict, open("hzdObjList.p", "wb"))
                else:
                    objDict.update({name: (option)})
            else:
                print("Option can only be following commands: \n"
                      "BUY -> buy a rare item with object\n"
                      "TRADE -> trade for a box with object\n"
                      "SELL -> sell object")
        else:
            print("Option name must be String")
    else:
        print("Object name must be String")

# adds a buying thing to an existing object
def addBuyingThing(name, thing, count, objDict):
    #checks whether type is TRADE or BUY (operation cannot be done for SELL)
    optionType = objDict.get(name)[0]
    if optionType == "TRADE" or optionType == "BUY":
        # extracts the already existing dict for entry name
        thingList = objDict.get(name)[1]
        if thing in thingList:
            print("Thing already in Dict")
        else:
            # special case for entry "REST_TRADE":
            #         flag in third position will be set to TRUE
            if thing == "REST_TRADE":
                # loop changes entry for key == name
                for key in objDict.keys():
                    if key == name:
                        option = objDict[key][0]
                        buyingThingdic = objDict[key][1]
                        objDict[key] = (option, buyingThingdic, True)

            objDict.get(name)[1].update({thing : int(count)})
            # save pickle changes
        pickle.dump(objDict, open("hzdObjList.p", "wb"))
    else:
        print("Selected object is a SELL-type and cannot hold buying thing dicts")

def addTrade(name, thing, objDict):
    if objDict[name][0] == "TRADE":
        objDict[name][1].append(thing)
    elif objDict[name][2]:
        # creates a second entry for 'name', with a #, appending 'thing*
        if name+"#" in objDict:
            objDict[name+"#"].append(thing)
        else:
            thinglist = []
            thinglist.append(thing)
            objDict.update({str(name) + "#" : thinglist})

        # save pickle
        pickle.dump(objDict, open("hzdObjList.p", "wb"))
    else:
        print("Trade flag not set")

#delete object in pickle
def deleteObj(name, objDict):
    if name in objDict:
        del objDict[name]
    else:
        print("No object of that name to delete")

#delete an element in an object buying thing dict
def deleteThing(name, thing, objDict):
    optionType = objDict.get(name)[0]
    if optionType == "TRADE" or optionType == "BUY":
        del objDict.get(name)[1][thing]
    else:
        print("Object is of type SELL and there is no buying thing list item to remove")

# makes list from command line arguments
args = []
for i in sys.argv[1:]:
    args.append(i)
if len(args) == 0:
    exit()

    # loades from file 'hzdObjList.p' and creates new if no file of that name is found
else:
    try:
        objDict = pickle.load(open("hzdObjList.p", "rb"))
    except (OSError, IOError):
        objDict = {}
        pickle.dump(objDict, open("hzdObjList.p", "wb"))
#   GET HELP
    if args[0] == "-help" or args[0] == "-Help" or args[0] == "-HELP":
        print("The following commands are available:\n"
            "SAVE : save a new object || hzd.py -save [name] [option]\n"
            "ADD : add a new buying thing to existing Object || hzd.py -add [name] [thing] [count] \n"
            "DELOBJ : delete an object in the list || hzd.py -delobj [name]\n"
            "DELTHI : delete a buying thing in an object || hzd.py -delthi [name] [thing]\n"
            "PRINT : prints entry for object || hzd.py -print [name]\n"
            "TRADE : add trade entry if flag is set || hzd.py -trade [name] [thing]"
            "OBJLIST : prints out list of objects || hzd.py -objlist"
            "RENAME_OBJ: renames object || hzd.py -rename_obj [old_name] [new_name]")

    #   SAVE OBJECT
    elif args[0] == "-save" or args[0] == "-Save" or args[0] == "-SAVE":
        if len(args) == 3:
            if args[1] in objDict:
                print("Object exists already")
            else:
                saveObj(args[1], args[2], objDict)
                pickle.dump(objDict, open("hzdObjList.p", "wb"))
        else:
            print("Wrong parameter length")
    #   ADD NEW BUYING THING
    elif args[0] == "-add" or args[0] == "-Add" or args[0] == "-ADD":
        if len(args) == 4:
            if args[1] in objDict:
                addBuyingThing(args[1], args[2], args[3], objDict)
                pickle.dump(objDict, open("hzdObjList.p", "wb"))
            else:
                print("Key not in Dict")
        else:
            print("Wrong parameter length")
    #   DELETE OBJECT
    elif args[0] == "-delobj" or args[0] == "-Delobj" or args[0] == "-DELOBJ" or args[0] == "-delObj":
        if len(args) == 2:
            deleteObj(args[1], objDict)
            pickle.dump(objDict, open("hzdObjList.p", "wb"))
        else:
            print("Wrong parameter length")
    #   DELETE THING
    elif args[0] == "-delthi" or args[0] == "-Delthi" or args[0] == "-DELTHI" or args[0] == "-delThi":
        if len(args) == 3:
            deleteThing(args[1], args[2], objDict)
            pickle.dump(objDict, open("hzdObjList.p", "wb"))
        else:
            print("Wrong parameter length")
    #   ADD TRADE
    elif args[0] == "-trade" or args[0] == "-Trade" or args[0] == "-TRADE":
        if len(args) == 3:
            #TODO
            addTrade(args[1], args[2], objDict)
            pickle.dump(objDict, open("hzdObjList.p", "wb"))
        else:
            print("Wrong parameter length")

    #   PRINT
    elif args[0] == "-print" or args[0] == "-Print" or args[0] == "-PRINT":
        if args[1] in objDict:
            optionType = objDict.get(args[1])[0]
            if optionType == "BUY":
                thingList = objDict.get(args[1])[1].items()
                count = 0
                for j, k in thingList:
                    count = count + int(k)
                buyingList = objDict.get(args[1])[1]

                print (str("=========") + str("BUY") + str("========="))
                for m in buyingList:
                    if(m == "REST_TRADE"):
                        print("==> " + m)
                    else:
                        print(m + ": x" + str(buyingList[m]))
                print(str(" || x") +  str(count) + "\n")
                if objDict.get(args[1])[2]:
                    print(str("=========") + "TRADE" + str("========="))
                    buyingList2 = objDict.get(str(args[1] + "#"))
                    print(buyingList2)
            elif optionType == "TRADE":
                print(str("=========") + str("TRADE") + str("========="))
                buyingList2 = objDict.get(args[1])
                print(buyingList2[1])
            else:
                print(str("=========") + str("SELL") + str("========="))

        else:
            print("No item of that name")


    elif args[0] == "-rename_obj" or args[0] == "-RENAME_OBJ":
        if args[1] in objDict:
            objDict[args[2]] = objDict.pop(args[1])
            pickle.dump(objDict, open("hzdObjList.p", "wb"))
        else:
            print("no object of that name")

    #   PRINT OUT A LIST OF KEYS
    elif args[0] == "-objlist" or "-Objlist" or "-OBJLIST" or "-objList":
        keys = objDict.keys()
        for k in keys:
            if "#" in k:
                keys.remove(k)
        print (sorted(keys))
    #   RENAME AN OBJECT KEY


