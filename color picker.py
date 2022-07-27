import random

while True: #loop to continously print random colors, so the user doesn't have to open the file each time.
    colors = ['black','grey','red','yellow','green','purple','orange'] #create colors list variable with some colors
    print(random.choice(colors)) #print random color from colors variable, using random module
    d = input('\nPress E to exit, or any other to continue').upper() #ask for input and convert to uppercase
    if d == 'E': #if user pressed the e key, exit
        break #break the while loop and end execution
    continue #continue back to the while loop