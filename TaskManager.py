# Five steps to run below python code 
# 1. Save all this content into a file called TaskManager.py
# 2. Make sure python 3.12.x is installed on the computer
# 3. Open powershell or command-line window or terminal window
# 4. Go to the folder where the file “TaskManager.py” is stored.
# 5. Type below command and follow instructions shown by the program
# python TaskManager.py


import json
import time
import util
import json
import getpass
import hashlib


# The TaskManager App code
# below boolean var is used to decide run or close the App based on user input
wrapApp = False
# if user input is equal to EXIT or exit, application terminates
userInput = "" 

userCredsFile = "./tmUsers.dat"
loginState = {"userID":"LOGIN_PENDING","loggedIn": False}

# initialize empty dictionary of users
userList = {}
# name of the Task File for a user is held in this variable
userTaskFile = "" 
#initialize empty dictionary of tasks
taskList = {}

def startTaskManager():
    global userInput 
    global wrapApp
    global loginState

    while (not wrapApp):
        userInput = input(f"TaskManager/{loginState['userID']}>")
        if userInput.upper() == "LOGIN" or userInput == "1" :
            loginState["userID"] = login()
        elif userInput.upper() == "CREATEUSER" or userInput == "2" :
            createUser()    
        elif userInput.upper() == "RESETPASSWORD" or userInput == "3" :
            resetPassword() 
        elif userInput.upper() == "VIEWUSERS" or userInput == "4" :
            viewUsers() 
        elif userInput.upper() == "ADDTASK" or userInput == "5" :
            createTask(loginState["userID"])
        elif userInput.upper() == "COMPLETETASK" or userInput == "7" :
            completeTask(loginState["userID"])    
        elif userInput.upper() == "DELETETASK" or userInput == "8" :
            deleteTask(loginState["userID"])   
        elif userInput.upper() == "VIEWTASKS" or userInput == "6" :
            viewTasks(loginState["userID"])                                     
        elif userInput.upper() == "HELP" or userInput == "9" :
            printHelp()        
        elif userInput.upper() == "LOGOUT" or userInput == "0":
            logout(loginState["userID"])
        elif userInput.upper() == "EXIT" or userInput.upper() == "X":
            wrapApp = True
        else:
             printHelp()

    
def printHelp():
    print('This App supports below commands.\n')
    print('Command / Keyword ...... Action')
    print('-------------------------------')
    print('1 or login ............. Login')
    print('2 or createUser ........ Create a User')
    print('3 or resetPassword ..... Reset Your password')
    print('4 or viewUsers ........ View existing UserIDs')
    #print('Manage Tasks after Login using below commands ...')
    print('5 or addTask ........... Add a Task')
    print('6 or viewTasks ......... View Tasks')  
    print('7 or completeTask ...... Mark a Task as Completed')    
    print('8 or deleteTask ........ Delete a Task')    
    print('9 or help .............. View Application Help')
    print('0 or logout ............ Logout')
    print('X or exit .............. Exit Task Manager App')
    print('Enter one of the Numeric code or Full text command from above list')


def createTask(userID):
    print('MenuItem: Add a Task')
    global userTaskFile
    global taskList
    global loginState
    if loginState["loggedIn"] == False:
        print('please login before adding a task')
        return
    userTaskFile = f"./{userID}Tasks.dat" 
    taskDesc = input("Task description>")
    #get current counter and add 1 before adding a new task
    tcounter = taskList.get("tcounter",0)
    tcounter += 1
    tid = f"T{tcounter}"
    taskJSON = f'"TaskID":"{tid}","Description":"{taskDesc}","Status":"PENDING"'
    taskList[tid] = "{" + taskJSON + "}"
    taskList["tcounter"] = tcounter
    storeTasks()
    print("New Task is successfully stored")

def deleteTask(userID):
    print('MenuItem: Delete A Task')
    global taskList
    global loginState

    if loginState["loggedIn"] == False:
        print("Please login before acting on a Task")
        return
    
    showTaskList()
    
    tID = input("Enter task ID>")
    # if taskID is present in tasks, then delete it
    if taskList.get(tID) != None:
        taskDetails = taskList.get(tID,"NOTFOUND")
        tDict = json.loads(taskDetails)
        print("Below task is deleted")
        print(f'TaskID: {tDict["TaskID"]}, Description: {tDict["Description"]}, Status: {tDict["Status"]}')
       
        taskList.pop(tID,None)
        storeTasks()
    else:
        print("Invalid TaskID, Select Menu option 8, to try again")

def completeTask(userID):
    print('MenuItem: Mark a Task as Completed')
    global taskList
    global loginState

    if loginState["loggedIn"] == False:
        print("Please login before acting on a Task")
        return
    showTaskList()
    
    tID = input("Enter task ID>")
    if taskList.get(tID) != None:
        taskList[tID]
        tempStr = taskList[tID]
        tempStr = tempStr.replace('"Status":"PENDING"', '"Status":"COMPLETED"')
        taskList[tID] = tempStr
        storeTasks()
        print("Task Status set to Completed and updated task list is below")
        showTaskList()
    else:
        print("Invalid TaskID, Select Menu option 7, to try again")
    

def viewTasks(userID):
    global loginState

    print('MenuItem: View Tasks')
    if loginState["loggedIn"] == False:
        print("please login before viewing tasks")
        return
    print(f'Task List for userID: {userID}')
    if userID != "LOGIN_PENDING":
        showTaskList()
    else:
        print("Please login before managing tasks")

def showTaskList():
    global taskList

    print("TaskID   Status        Description")
    for t in taskList.keys():
        #skip printing task counter but rest of the tasks
        if t != "tcounter":
            taskDetails = taskList.get(t)
            tDict = json.loads(taskDetails)
            print(f'{tDict["TaskID"]}       {tDict["Status"]}      {tDict["Description"]} ')

def storeTasks():
    """ This function stores user tasks into file"""
    global userTaskFile
    global taskList
    with open(userTaskFile,"w") as utFile:
        json.dump(taskList,utFile)
        

def loadTasks(userID):
    
    global taskList
    global userTaskFile
    #set tasks file name here based on userid loggedin
    userTaskFile = f"./{userID}Tasks.dat"
   #  print(f'loading tasks from {userTaskFile}')
    try:
        with open(userTaskFile,"r") as utFile:
            taskList = json.load(utFile)
    except FileNotFoundError:
        with open(userTaskFile, "w+") as utFile:
            contents = utFile.read()
    except json.JSONDecodeError:
        print(f"Note:  No Tasks on file yet")


def createUser():
    print('MenuItem: Registration or Creating new user')
    global userList
    global userTaskFile

    currentUsers = list(userList.keys())
    if len(currentUsers) == 0:
        print("Create atleast one UserID before using the App")
    
    userName = input('UserName(no more than 8 characters)=')
    passWord = getpass.getpass('Password(keep it simple)=')
    passWordRe = getpass.getpass('Re-enter password=')

    if passWord != passWordRe:
        print('Password re-entered did not match, try again')
    else:
        passWord = hashlib.sha256(passWord.encode()).hexdigest()
        uData = f"{userName}:{passWord}"
        # add to local list before storing in file
        userList[userName] = uData
        # print(userList)
        with open(userCredsFile, "w+") as uFile:
            json.dump(userList,uFile)
        # create a user task file for newly created user    
        userTaskFile = f"./{userName}Tasks.dat"    
        try: 
            with open(userTaskFile,"x") as utFile:
                print(f"Ready to manage tasks for user '{userName}'")
        except FileExistsError:
                print("seems userID exists")

def login() -> str:
    global loginState

    print('Menu Item: login')
    if loginState["loggedIn"] == True:
        print("Logout using '0' option and then login as different user")
        return loginState["userID"]

    userID = input('Userid=')
    passWord = getpass.getpass('Password=')
    passWord = hashlib.sha256(passWord.encode()).hexdigest()
    if verifyLogin(userID,passWord):
        loadTasks(userID)
        return userID
    else:
        return "LOGIN_PENDING"

def verifyLogin(uid,pwd) -> bool:
    global userList
    global loginState
    uResult = userList.get(uid,"NOTFOUND")
    if uResult == "NOTFOUND":
        print("userID was not created yet, please create a user before proceeding further")
        return False
    else:
        uSecret = uResult.split(":")[1]

        if uSecret == pwd:
            loginState["userID"] = uid
            loginState["loggedIn"] = True
            print("login is successful")
            return True
        else:
            print("incorrect login and password, try again")    
            return False
        
def resetPassword():
    print('MenuItem: Reset password')
    global userList
    userNames = list(userList.keys())
    userName = userNames[0]
    print(f"reset password for {userName}")
    passWord = getpass.getpass('New Password(keep it simple)=')
    passWordRe = getpass.getpass('Re-enter New password=')

    if passWord != passWordRe:
        print('Password re-entered did not match, try again')
    else:
        #note : do not use default hash function since it returns inconsistent hashcodes for same input
        passWord = hashlib.sha256(passWord.encode()).hexdigest()
        uData = f"{userName}:{passWord}"
        # add to local list before storing in file
        userList[userName] = uData
        # print(userList)
        with open(userCredsFile, "w+") as uFile:
            json.dump(userList,uFile)

def logout(userID):
    
    global taskList
    global userTaskFile
    global loginState
    print('MenuItem: Logout')
    if loginState["loggedIn"] == False:
        print("Nice try, no one logged in yet. Try X to exit")
        return
    print(f'{userID} successfully loggedout')
    loginState["loggedIn"] = False
    loginState["userID"] = "LOGIN_PENDING"
    taskList = {}
    userTaskFile = ""

def viewUsers():
    print('MenuItem: View existing UserIDs')
    currentUsers = list(userList.keys())
    for userID in currentUsers:
        print(userID)

def loadUsers():
    global userCredsFile
    global userList
    # create file if its first time using the App
   # with open(userCredsFile, "w+") as uFile:
    #    contents = uFile.read()
    # Read dictionary from a JSON file
    try:
        with open(userCredsFile, 'r') as uFile:
            userList = json.load(uFile)
    except FileNotFoundError:
        with open(userCredsFile, "w+") as uFile:
            contents = uFile.read()
    except json.JSONDecodeError:
        print(f"Warning:  No users created yet")

def setupUsers():
    global userCredsFile

    print('Preparing App', end="")
    msgStr = '......' 
    util.fancyPrint(msgStr)
    loadUsers()
    print('App is ready.\n')
    time.sleep(0.3)

# Start of the App code execution
print('\n***** Welcome to TASK MANAGER App *****')
setupUsers()
printHelp()
startTaskManager()
