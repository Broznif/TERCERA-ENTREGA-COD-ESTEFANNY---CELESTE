# DATA CLUSTER PROJECT

## Autors
- Maria Celeste Zuluaga Giraldo.
- Estefanny Alejandra Jaimes León.

## Suggested structure
- Src carpet: In this folder we have the menu source code and program logic.
- Test: In this folder we have the error, exception and normal unit tests.

## Functionality and use
In this program we implement an algorithm to calculate the distance between each data point and the centroids of the current clusters, and then assign each data point to the cluster whose centroid is closest.

## Program execution for GUI
To execute the program we first need to have a database, in this case one called "adult.csv" was used where we have data on people's age, number of education hours per week, capital loss and capital gained, with this database we proceed to perform the clusterin tests for the user and to not enter floating, negative numbers, so that the file does load correctly, to finally be able to show the user the clusters of the data as output.

pip install kivy["base"]

pip install pandas

pip install matplotlib

* Clone the repository.

`git clone https://github.com/Broznif/TERCERA-ENTREGA-COD-ESTEFANNY---CELESTE.git`

* Open a terminal in the folder where the program files are located.

`cd TERCERA-ENTREGA-COD-ESTEFANNY---CELESTE`

* Run the following command to start the program:

`python src\console\main.py`

The menu will be displayed where you can access to choose which file (.csv only) to use to know the number of clusters.

## Program execution for console

pip install pandas

pip install matplotlib

* Clone the repository.

`git clone https://github.com/Broznif/TERCERA-ENTREGA-COD-ESTEFANNY---CELESTE.git`

* Open a terminal in the folder where the program files are located.

`cd TERCERA-ENTREGA-COD-ESTEFANNY---CELESTE`

* Run the following command to start the program:

`python src\console\menu.py`

## Running unit tests
Before creating a program, a series of unit tests are carried out to verify its correct operation. With this starting point we execute them, making sure to correctly install the libraries, files and commands.

`pip install pytest`

`pytest 1 error CM.py`