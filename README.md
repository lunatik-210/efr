Escape from Russia
===============

Entry in PyWeek #15  <http://www.pyweek.org/15/>
URL: https://github.com/lunatik-210/efr
Team: PyGeeks
Members: Andrew Lapin (lunatik) - andrew.d.lapin@gmail.com, Alexander Gudulin (sagod), Michael Turusov (Sneaky4oe)
License: see LICENSE.txt


Running the Game
----------------

On Windows or Mac OS X, locate the "start.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python start.py


How to Play the Game
--------------------

yourgamedescription

Move the cursor around the screen with the mouse.

Press the left mouse button to fire the ducks.


Development notes 
-----------------

Creating a source distribution with::

   python setup.py sdist

You may also generate Windows executables and OS X applications::

   python setup.py py2exe
   python setup.py py2app

Upload files to PyWeek with::

   python pyweek_upload.py

Upload to the Python Package Index with::

   python setup.py register
   python setup.py sdist upload
