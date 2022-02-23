# Feature(s)

What this script does, is that you can enter Materials like "Reinforced Iron Plate", a multiplier, and it will give you the amount of Smelters/Constructors/etc you need to build in order to fully run one full batch of your Materia.

Alternate Recipes are also incorporated in this script. If you want the calculator to use one or more alt recipes, f. e. Steel Screws, the calculator will replace all Screws during the calculations with Steel Screws. 

If this explanation doesn't make sense, look at the example section

# How to use:

Simply run frontend.py on a python interpreter and follow the instructions

## Example:

Recipe: "Reinforced Iron Plate"

Amount: 1

Output: [('Iron Plate', 3.0), ('Screw', 3.0), ('Iron Rod', 2.0), ('Iron Ingot', 4.0)]

Which means to produce one batch (in the case of RIP, that would be 5/min), we need: 
- 4 Smelters Producing Iron
- 2 Constructors Producing Iron Rods
- 3 Constructors Producing Screws
- 3 Constructors Producing Iron Plates

Recipe: "Reinforced Iron Plate"

Amount: 1

Alt Recipe: "Steel Screw" 

Output: [('Iron Plate', 1.5), ('alt Steel Screw', 0.23076923076923078), ('Iron Ingot', 1.5), ('Steel Beam', 0.07692307692307693), ('Steel Ingot', 0.10256410256410256)]