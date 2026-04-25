# Standalone NTO Visualiser
Python Module Requirements (pip install):
- aiida-core
- aiida-shell
- nglview 
- ipywidgets
- cubehandler
- ase

### Installation:

0)  [Install ORCA.](https://www.faccts.de/docs#orca)

1) Pull/download files from repository and install all required Python Modules.

2) Make an AiiDA profile on your system using 
```
verdi presto [--profile-name NAME]
```

3) Setup the AiiDA Codes for orca and orca_plot using 
```
verdi code create core.code.installed
``` 
and the settings below.


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
### Usage
Run "orbital_visualiser.ipynb", which will calculate NTOs and visualise them inside the notebook.

### Atmospec Integration
Integration with AtmoSpec can be found at https://github.com/AaronH-sys/aiidalab-ispg.

Follow all installation instructions found in the README.
Once on the AiiDAlab home page, open the terminal and enter 

```aiidalab install ispg@git+https://github.com/AaronH-sys/aiidalab-ispg```.

Setup the ORCA codes as you have done for the standalone and our updated fork of Atmospec should be ready to run.
