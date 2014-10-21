Flashcarder
===========

Renpy implementation of a type-out flash card app.

This app was written in Python (and the Ren'Py Visual Novel Engine). Here's, in a nutshell, what it does:

    * Make the Packs folder if I have to
    * Open the folder
    * Step through the folder, checking only for .rsv ("return separated values haha") files
    * Make a menu, using .rsv files as an option
    * Check if you want to use multiple packs (important for midterms/cramming!)
    * Create a list of questions/answers from each .rsv file; the expected format of each .rsv file is a line of text containing a question, followed by a line of text containing an answer.
    * Shuffles this list.
    * Presents each question if it does not have a mode. If it does have a mode, we do something special.
    * Answers are not case or punctuation sensitive; if you type out the answer wrong, we re-add it to the deck. Otherwise, we chuck it out.

## Using modes - (Examples are copyright DigiPen Institute of Technology 2014)
[combo] - Requires all answers, but in any order.

    What are the three primary elements of the game analysis model used for this class?
    [combo]/Modes/Goals/Dynamics

[at_least][n] - Requires at lesat "n" answers, but in any order.

    Name at least three modes of design.
    [at_least]/[3]/Narrative/Visual/Audio/Haptic/Mechanics/Components/Spaces

[image][file] - Displays the image "file", and requires the third segment as the answer.

    Identify this game which is the pinnacle of the evolution of this game type from Nard.
    [image]/[/GAT110/backgammon.png]/Backgammon

[any_of] - Any of the answers are acceptable.

    What is the name of the draw pile of dominoes?
    [any_of]/Boneyard/woodpile
    
    
[any_of+formula] - 

    What is a general rule for quickly determining the average roll of an N-sided die where N is an even number?
    [any_of+formula]BREAK(N/2)+(1/2)BREAK(N+1)/2

## Making an .rsv file.
1. Make a new text file.
2. Every two lines constitutes a flash card. The first line is the question, and the second line is the answer.
3. Add modes, if need be.
4. Remove the last character of the file if it is a newline. (The last line should contain the last answer.)

## Installing an .rsv file.
1. Launch the program.
2. Start a "game".
3. Watch the folder open - you may need to tab to other Finder/Explorer windows on UNIX (OS X/Linux) systems.
4. Move your .rsv files in there.
