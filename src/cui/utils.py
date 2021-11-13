def ClearScreen():
    import os
    if 'nt' in os.name:
        os.system('cls')
    else:
        os.system('clear')

def Pause():
    input("Press enter to continue...")