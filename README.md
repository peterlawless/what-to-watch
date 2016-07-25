## Synopsis

The purpose of this repository is to create an suggestion engine
based on data from the University of Minnesota's GroupLens Research Project.

It is one of my first attempts at object-oriented programming and test-driven
development.

Data is read from character separated values files into lists using the csv module
and then converted into special user, movie, and rating objects.

My approach was to make a larger database object that is initialized with lists
of users, movies, and ratings, and then make a series of methods that operated on
that database object.  However, the level of complexity inherent in my approach
leads me to believe that there must be a more efficient design out there that
also is not a PEP8 nightmare.
