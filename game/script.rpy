# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
define mc = Character('Message', color="#c8ffc8", show_two_window = True)
define nvln = Character(None, kind = nvl)

# The game starts here.
label start:
    $ setup()
    jump start2

label start2:
    $ show_folder("Packs")
    menu:
        "Please move your pack files into the opened folder before continuing."
        "Done.":
            jump start3
        "Show me the folder again":
            jump start2
            
label start3:
    $ list = getCards()
    $ getPacks = True
    $ packSet = []
    $ packLines = []
    $ wrongOnce = []
    while(getPacks):
        $ wantedPack = askPack(list)
        $ list.remove(wantedPack[1:])
        $ grabbedPack = listPack(wantedPack)
        $ packLines.extend(unifyList(grabbedPack))
        if (len(list) != 0):
            menu:
                "Add more packs to this session?"
                "Yes":
                    $ getPacks = True
                "No":
                    $ getPacks = False
        else:
            $ getPacks = False
    while(len(packLines) != 0):
        $ shufflePack(packLines)
        $ packLines =  quizMe(packLines)
        $ wrongOnce = arrayMerge(wrongOnce, packLines)
    $ wrongOnce = arraySplit(wrongOnce)
    if(len(wrongOnce) != 0):
        nvln "You need to review: [wrongOnce]"
    else:
        "You should be OK"
