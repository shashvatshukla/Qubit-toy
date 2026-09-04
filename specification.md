Build a pygame applet that runs as an executable. For now it should just have a switcher at the bottom that changes the color of the screen. There should be two buttons, one labelled "Bit" and one labelled "Qubit".

On the first screen there should be a little box indicating 0 or 1. There should be four buttons: Set 0, Set 1, Flip and Random. 

On the second screen there should be four lights arranges in a north south east west orientation. The lights are N: |0> , S: |1> , E: |+>, W: |->. The qubit will start in the |0> state but this will not be indicated in any way. There will be three buttons. One button is placed below the South light and says "Measure Z". When the Measure Z button is clicked it will measure the qubit and light up either |0> or |1> for the duration of 0.3 seconds. 

The "Measure X" button will be to the East of the |+> light, and will hehave analogously, lighting up either |+> or |->. 

To the south east position, aligned with the measure X and Z button, there should be a Hadamard gate button, that applies a H gate to the underlying qubit.

All buttons should light up to make it clear they were clicked

The four lights on the qubit screen should say 0, 1, + and - within them. remove the |> and the NSEW.

Without removing any of the functionality specified in `specification.md`, refactor the code to be shorter, not have much boilerplate, not have unnecessary features. 

The logic of the qubit should be implemented by storing an underlying `qubit_value` which is an enum of the four states. Define simple functions in the code that act on the enum how the gates should. 

Refactor the code into three files: qubit_toy.py that contains the main game loop and all logic except that which can be refactored into bit_logic.py and qubit_logic.py, which contain the functions and definitions specific to those two screens.


Add a level system that works like this. The levels are shown on the qubit screen. they involve shining lights in a specific sequence to complete the level. The levels are shown as a sequence of unlit small lights indicating which lights need to light up. As lights are lit up in the right sequence the small lights indicating the level also light up and stay solid. If one light is wrong it resets the lights back to all off. At the bottom of the sequence of lights are two arrows allowing you to go to the previous level or the next one. Make the code design such that each level is a list of the light enums, and all the levels are stored as a list of list. For now make the list of levels to be [[0,0,0,0,0],[1,1,1,1,1],[+,+,+,+,+],[-,-,-,-,-]]