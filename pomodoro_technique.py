from time import sleep, time
from pygame import mixer
import os
import pyautogui
import screen_brightness_control as sbc

# Incase Files are absent in the app_data directory it will create default files instead of giving error
i = 0
for subdir, dirs, files in os.walk('./ringtones/'):
    for file in files:
        if(i == 0):
            randfile = file
            i = 1

if(not(os.path.exists("app_data/ringtone_file.txt"))):
    with open("app_data/ringtone_file.txt", "w") as f:
        f.write(f"ringtones/{randfile}")

if(not(os.path.exists("app_data/session_length.txt"))):
    with open("app_data/session_length.txt", "w") as f:
        f.write("25")

# A fail safe function if in case user enters other than int value
def input_int(intput_string):
    int_check_value = True
    
    while(int_check_value):
        try:
            temp = int(input(intput_string))
            int_check_value = False
        except ValueError:
            print("-"*30)
            print("Invalid Input")
            print("Try Again")
            print("-"*30)
            int_check_value = True
    
    return temp

# A fail safe fuction to accept desired string from user as input
def input_particular_string(input_string, favoured_string_list):
    temp = input(input_string)
    
    while(temp not in favoured_string_list):
        print("-"*86)
        print("Invalid Input")
        print("Try Again")
        print("-"*86)
        temp = input(input_string)
    
    return temp

# Playing Music(playing time in sec)
def playing_music(music_location, playing_time):
    mixer.init()
    mixer.music.load(music_location)
    mixer.music.play()
    sleep(playing_time)
    mixer.music.stop()

# Time Countdown Fuction
def countdown(hrs, min, sec):
    # Starting Don't Sleep Timer from 1 sec
    dontsleeptimer = 1

    print("-"*86)
    print("Remaining Time")

    # Converting sec(under 60 sec), min(under 60 min) for eg. 3600 sec will be converted to 60 min then 60 min will be converted to 1 hr for proper arrangement of clock
    while sec>=60:
        sec -= 60
        min += 1

    while min>=60:
        min -= 60
        hrs += 1

    def fn(x):
        if (x<=9) and (x>=0):
            return '0' + str(x)
        else:
            return str(x)
    
    # Total Sec Keep track of time
    total_sec = sec + (min*60) + (hrs*3600)
    while total_sec != 0:
        print(f'    -> {fn(hrs)}:{fn(min)}:{fn(sec)}', end = '\r') # Printing countdown

        # Countdown 
        if sec == 0:
            if min != 0:
                sec = 59
                min -= 1
            else:
                if hrs != 0:
                    sec = 59
                    min = 59
                    hrs -= 1
                else:
                    break 
        else:
            sec -= 1
        total_sec -= 1

        # Don't sleep function will press volume up and down button to avoid sleep mode after every 100 sec
        dontsleeptimer += 1
        if(dontsleeptimer%100 == 0):
            pyautogui.press('down')
        
        # Function will repeat after 1 sec until hrs, min, sec are all 0
        sleep(1)

    print('    -> 00:00:00\nTime Up')

    # Opening Ringtone File(Collecting Ringtone Location), and then Playing Ringtone for 10 sec
    with open("app_data/ringtone_file.txt", "r") as f:
        ringtone = f.read()
    
    playing_music(ringtone, 10)

    print("-"*86)


# Main Program
print("-"*86)
print("Pomodoro Session")
print("-"*86)

# Keeping Programming in Loop until user close it.
restart = True
while restart:
    main_menu_choice = input_particular_string(f'''Main Menu
{"-"*86}
-> About Pomodoro ........(a)
-> Pomodoro Session ......(p)
-> Level Up Session ......(u)
-> Level Down Session ....(d)
-> Break .................(b)
-> Change Ringtone .......(r)
-> Exit ..................(e)
{"-"*86}
 # Enter Your Choice: ''', ["a", "p", "u", "d", "b", "r", "e"])
    print("-"*86)
    
    # About Pomodoro
    if(main_menu_choice == "a"):
        print('''What Is the Pomodoro Technique?

    The  Pomodoro Technique  is  a  time  management  system  that  encourages  people
to  work  with  the  time  they  have—rather  than  against it. Using this method, you 
break  your  workday  into  25-minute chunks  separated  by  five-minute breaks. These 
intervals  are referred to as pomodoros. After about four pomodoros, you take a longer 
break of about 15 to 20 minutes.

    The  idea  behind  the  technique is that the timer  instills  a sense of urgency. 
Rather  than  feeling  like you have  endless time  in the workday  to get things done 
and  then  ultimately  squandering  those  precious work  hours on  distractions,  you 
know you only have 25 minutes to make as much progress on a task as possible.
    
    Additionally, the forced breaks help to cure that frazzled, burnt-out feeling most 
of us experience toward the end of the day. It's impossible to spend hours in front of 
your  computer without even realizing it,  as that ticking timer reminds you to get up 
and take a breather''')
    
    # Pomodoro Session
    elif(main_menu_choice == "p"):
        # Importing User Define or Default(25 min) Session Length
        with open("app_data/session_length.txt", "r") as f:
            session = int(f.read())
        
        # Coverting Total Minutes into hours and minutes
        hrs = 0
        min = session
        while(min>=60):
            min -= 60
            hrs += 1
        
        # Running Countdown or Going Back to Main Menu Choice
        print("Current Session Length:", hrs, "hr and", min, "min")
        sub_menu_choice = input_particular_string("Want to Start Session(y/n): ", ["y", "Y", "n", "N"])
        
        print("-"*86)
        
        
        if sub_menu_choice == 'n' or sub_menu_choice == "N":
            continue
        else:
            brightness_control = input_particular_string("Will You be using PC During Session(y/n): ", ["y", "Y", "n", "N"])
            print("-"*86)

            if(brightness_control == 'n' or brightness_control == 'N'):
                print("Lowering Screen Brightness")
                sbc.set_brightness(10, display=0)
                sbc.set_brightness(10, display=1)

            countdown(hrs, min, 0)

            if(brightness_control == 'n' or brightness_control == 'N'):
                print("Lowering Screen Brightness")
                sbc.set_brightness(100, display=0)
                sbc.set_brightness(90, display=1)

    # Level Up
    elif(main_menu_choice == "u"):
        # Importing User Define or Default(25 min) Session Length
        with open("app_data/session_length.txt", "r") as f:
            session = int(f.read())
        
        # Coverting Total Minutes into hours and minutes
        hrs = 0
        min = session

        while(min>=60):
            min -= 60
            hrs += 1

        print(f"Current Session Time: {hrs} hr and {min} min")

        # Level Up Choices
        sub_menu_choice = input_particular_string(f'''Level Up Menu:
-> Standard Level Up(5 min) ...(s)
-> Custom Level Up ............(c)
-> Go Back to Main Menu .......(m)
{"-"*86}
 # Enter Your Choice: ''', ["s", "c", "m"])

        # Adding 5 min to Previously User Define Session or Default Session(25 min)
        if(sub_menu_choice == "s"):
            session = session + 5

            with open("app_data/session_length.txt", "w") as f:
                f.write(str(session))
            
            print("Session Time Increased by 5 min")
        
        # Adding custom min & hrs to Previously User Define Session or Default Session(25 min)
        elif(sub_menu_choice == "c"):
            hr = input_int("\nEnter Increase Hrs: ")
            mn = input_int("Enter Increase Min: ")

            session = session + (hr*60) + mn

            with open("app_data/session_length.txt", "w") as f:
                f.write(str(session))
            
            print(f"Session Time Increased by {hr} hr and {mn} min")
        
        # Going Back to Main Menu
        else:
            print("-"*86)
            continue
    
    # Level Down
    elif(main_menu_choice == "d"):
        # Importing User Define or Default(25 min) Session Length
        with open("app_data/session_length.txt", "r") as f:
            session = int(f.read())
        
        # Coverting Total Minutes into hours and minutes
        hrs = 0
        total_min = session

        while(total_min>=60):
            total_min -= 60
            hrs += 1

        print(f"Current Session Time: {hrs} hr and {total_min} min")

        # Level Down Choices
        sub_menu_choice = input_particular_string(f'''Level Down Menu:
-> Standard Level Down(5 min) ...(s)
-> Custom Level Down ............(c)
-> Going Back to Main Menu ......(m)
{"-"*86}
 # Enter Your Choice: ''', ["s", "c", "m"])

        # Subtracting 5 min from Previously User Define Session or Default Session(25 min)
        if(sub_menu_choice == "s"):
            session = session - 5

            with open("app_data/session_length.txt", "w") as f:
                f.write(str(session))
            
            print("Session Time Decreased by 5 min")

        # Subtracting custom min & hrs from Previously User Define Session or Default Session(25 min)
        elif(sub_menu_choice == "c"):
            hr = input_int("\nEnter Decrease Hrs: ")
            mn = input_int("Enter Decrease Min: ")

            session = session - (hr*60) - mn

            with open("app_data/session_length.txt", "w") as f:
                f.write(str(session))
            
            print(f"Session Time Decreased by {hr} hr and {mn} min")
        
        # Going Back to Main Menu
        else:
            print("-"*86)
            continue
    
    # Break
    elif(main_menu_choice == "b"):
        char_collect = []

        # max break allow: 600 min or 10 hrs(which is lot and if you need this much break then you should probably see a doctor)
        for i in range(600):
            char_collect.append(str(i+1))

        char_collect.append("c")

        br_len = input_particular_string(f'''Break Time:
-> 5 min ..................(1)
-> 15 min .................(2)
-> Custom .................(3)
-> Go Back to Main Menu ...(4)
{"-"*86}
 # Enter Your Choice: ''', char_collect)
        
        if(br_len == "1" or br_len == "5"):
            min = 5

        elif(br_len == "2" or br_len == "15"):
            min = 15

        elif(br_len == "3" or br_len == "c"):
            print("-"*86)
            min = input_int("Enter Minutes: ")

        elif(br_len == "4"):
            print("-"*86)
            continue

        else:
            min = int(br_len)
            continue_input = input_particular_string(f"\n-> {min} min break session\n # Want to Continue(y/n): ", ["y", "n"])
            if(continue_input == "y"):
                pass
            else:
                print("-"*86)
                continue
        
        brightness_control = input_particular_string("Will You be using PC During Session(y/n): ", ["y", "Y", "n", "N"])
        print("-"*86)

        if(brightness_control == 'n' or brightness_control == 'N'):
            print("Lowering Screen Brightness")
            sbc.set_brightness(10, display=0)
            sbc.set_brightness(10, display=1)

        countdown(0, min, 0)

        if(brightness_control == 'n' or brightness_control == 'N'):
            print("Lowering Screen Brightness")
            sbc.set_brightness(100, display=0)
            sbc.set_brightness(100, display=1)
    
    # Change Ringtone
    elif(main_menu_choice == "r"):
        # Importing Current Ringtone in a list at 0th position
        with open("app_data/ringtone_file.txt", "r") as f:
            current = f.read()
            file_lst = [current[10:]]

        # Importing All Ringtone in List except Current Ringtone as it already exists
        for subdir, dirs, files in os.walk('./ringtones/'):
            for file in files:
              if(file == file_lst[0]):
                  pass
              else:
                  file_lst.append(file)
        
        # Assigning No. to Ringtones for user to interact
        for i in range(len(file_lst)):
            if(i == 0):
                print(f"{i+1}. {file_lst[i]}(current ringtone)")
            else:
                print(f"{i+1}. {file_lst[i]}")
        print("-"*86)

        # Option To Listen available ringtones before choosing
        print("Listen Ringtones")
        cho = ''
        while(cho != "n"):
            sub_menu_choice = input_particular_string("Enter Ringtone No. you want to listen: ", [str(i+1) for i in range(len(file_lst))])
            sub_menu_choice = int(sub_menu_choice) - 1
            playing_music(f"ringtones/{file_lst[sub_menu_choice]}", 10)

            cho = input_particular_string("\nWant to Listen More(y/n): ", ["y", "Y", "n", "N"])
            cho.lower()
            print("-"*86)
        
        # Assigning No. to Ringtones for user to interact
        for i in range(len(file_lst)):
            if(i == 0):
                print(f"{i+1}. {file_lst[i]}(current ringtone)")
            else:
                print(f"{i+1}. {file_lst[i]}")
        print("-"*86)

        # Choosing Ringtone & Updating Ringtone Record
        sub_menu_choice = input_particular_string("Enter Your Ringtone Choice: ", [str(i+1) for i in range(len(file_lst))])
        sub_menu_choice = int(sub_menu_choice) - 1

        with open("app_data/ringtone_file.txt", "w") as f:
            f.write(f"ringtones/{file_lst[sub_menu_choice]}")
    
    # Exit
    else:
        restart = False
        continue


    print("-"*86)
    restartfn = input_particular_string('Want to Continue(y/n): ', ["y", "Y", "n", "N"])
    print("-"*86)
    if restartfn == 'n' or restartfn == "N":
        restart = False

print("Closing Program")
sleep(0.5)