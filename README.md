# Swampyer
Doubling down on Allen Downey's amazing Swampy Package, Swampyer retains the same themes and overarching organization, while adding additional features that make it easier to implement diverse behaviors and a rich environment.

The key changes spawn from an augmentation of TurmiteWorld, which I have called BehaviorWorld.

A new class, 'Behavior' (Behavior.py) allows the user to define arbitrary behaviors, which are then incorporated as methods of animals. Animals call upon their behavior to interact with their environment at each timestep.

To implement Behavior, I created a Motions.py module that can be used to specify arbitrary instantaneous repositionings of an animal. So far, Motions.py been very lightly used, but I believe it offers great expressive potential.

Downey's CellWorld.py module is split in two: CellWorld.py and Cells.py. CellWorld.py retains the CellWorld class, while Cells.py contains a bunch of cell classes, each following a simple format established by an abstract Cell class. For reference, Downey's Cell class is reformulated as BoolCell. Different cell classes can be used to represent the landscape of the world that our animals roam.

As of 1/2/2018, there are only two animals: Turmites and Dustmites. Turmites interact with BoolCells and follow the Langton Ant behavior. They are as implemented by Downey. Dustmites interact with GrayCells and 'eat dust' (check out the code to see what that means!).

Finally, Swampyer lets the user set the topological properties of the world! For now only very simple, 2-dimensional worlds are supported: (infinite-plane, infinite-ribbon, rectangle, infinite-cylinder, finite-cylinder, torus). More to come; in particular, a spherical world is a short-term target.

As stated above, credit is due to Allen Downey, and I highly recommend reading his original Swampy (and other!) package(s), which can be found at http://www.greenteapress.com/thinkpython/swampy/

To contact me directly: lreardon@berkeley.edu
