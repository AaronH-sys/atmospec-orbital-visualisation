# Standalone NTO Visualiser
Python Module Requirements:
-Aiida
-nglview 
-ipywidgets
-traitlets
-ase
-aiida_shell
-cubehandler
-numpy
-PIL

Installation:

0)  [Install ORCA.](https://www.faccts.de/docs#orca)

1) Pull/download files from repository and install all required Python Modules.

2) Make an Aiida profile on your system. ```verdi presto [--profile-name NAME]```

3) Setup the Aiida Codes for orca and orca_plot. ```verdi code create core.code.installed```
```
Computer: localhost
Filepath executable: PATH/TO/ORCA/orca
Label: orca
Description []: DESCRIPTION
Default CalcJob plugin: orca.orca
Escape using double quotes [y/N]: n
Prepend Text: export PATH=PATH/TO/ORCA/orca:$PATH; export LD_LIBRARY_PATH=PATH/TO/ORCA/orca:$LD_LIBRARY_PATH;

Computer: localhost
Filepath executable: PATH/TO/ORCA/orca_plot
Label: orca_plot
Description []: DESCRIPTION
Default CalcJob plugin: orca.orca_plot
Escape using double quotes [y/N]: n
Prepend Text: export PATH=PATH/TO/ORCA/orca_plot:$PATH; export LD_LIBRARY_PATH=PATH/TO/ORCA/orca_plot:$LD_LIBRARY_PATH;
```
4) Run "nglview.ipynb" to calculate NTOs and visualise them.
