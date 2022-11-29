# FERMO Dashboard

FERMO is a dashboard app for the processing and visualization of liquid chromatography - (tandem) mass spectrometry (LC-MS/MS) data, and its pairing to quantitative biological data and other metadata. In particular, FERMO is aimed toward the exploration and prioritization of compounds and/or samples for consecutive investigation, such as isolation and elucidation. Developed with natural products research in mind, FERMO can be also used in different areas of the life sciences, such as metabolomics or environmental sciences, to investigate metabolites, drugs, pollutants, or agrochemicals.

FERMO comes with an information-rich dashboard interface, which allows for visualization of all available data simultaneously. Users can provide metadata to group their samples, to get insight about sample- or group-specific compounds, or to annotate control/blank-associated features. Users can also provide data from biological activity screening, to identify compounds associated to quantitative biological data. Samples and compounds can be filtered for putative chemical novelty and diversity, and selected for further investigation based on reproducible and comprehensible criteria.
 

FERMO is written in Python and runs fully locally, with no data shared across the internet. We do note that it is possible to save a FERMO session in a comprehensive file format to share between collaborators or with the publication of a study. The use of FERNO does not require any registration, does not track user statistics, and is released under the permissive MIT open sources license, which allows it to be used in both an academic and commercial setting. To run FERMO, simply clone this repository or download the zipped folder, which can be found here (TBA). Installation instructions and a quickstart tutorial can be found below. A more thorough guide and references to specific functions of FERMO can be found in the [FERMO Wiki](https://github.com/mmzdouc/FERMO/wiki/) (TBA).

## License

FERMO is licensed under the [MIT License](LICENSE.md) - see the [LICENSE.md](LICENSE.md) file for details.

## Getting Started

### Prerequisites

FERMO requires following files for analysis

- a peaktable in the MZmine3 'quant_full.csv' format. 
- the accompanying MZmine3 .mgf-file, automatically created during peaktable generation. 
- (optional) a .csv file containing metadata information.
- (optional) a .csv file containing quantitative biological data information.
- (optional) a spectral library in the .mgf format.

Instructions for the generation of the files, as well as the required format, can be found in the [user guides on input data formats](https://github.com/mmzdouc/FERMO/wiki/Input-data-formats) in the FERMO Wiki.

Examples of the files can be found in the `example_data` folder in this repository. These example files can be used for a test-run of the software.


### Installation

#### WINDOWS:

1. Download the FERMO zipped package to an easily accessible location to which you have write access, such as the Downloads folder or the Desktop. Unpack the package. This can be done using (free) software such as 7-Zip (https://www.7-zip.org/). Alternatively, you can also clone this repository.

2. Download and install the latest Miniconda3 version from the [Conda website](https://docs.conda.io/en/latest/miniconda.html), following the instructions of the install program. Accept the default settings and the license conditions. Alternatively, Anaconda can also be used, but its installation requires substantially more disk space. More details on the installation procedure can be found in [this Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html).

3. Once Miniconda3 (or Anaconda) is installed, there are two options to run FERMO. The easiest option is by double-clicking the startup batch script `FERMO_START_WINDOWS.bat`, which can be found in the FERMO directory. This script will start FERMO, install all dependencies, and open a browser window where FERMO can be used (refresh after a few seconds if there is nothing to see). However, the script will only work if Miniconda3 (or Anaconda) was installed with default parameters, since the script will check for an installation in `C:\Users\your_username\miniconda3\` (or `C:\Users\your_username\anaconda3\`). 

4. If the script does not start correctly, it might be because Miniconda3/Anaconda3 were installed on another drive than `C:`. In this case, FERMO has to be started manually as indicated in step **5** (experienced users might also edit the `FERMO_START_WINDOWS.bat` file and change the path variables `MINICONDAPATH` and `MINIENVPATH` for Miniconda3 or `ANACONDAPATH` and `ANAENVPATH` for Anaconda3 and try to rerun the script). 

5. **Manual install and start of FERMO**: From the Windows start menu, open the **Anaconda Prompt**. A command line interface will appear, in which the following steps are performed.

6. In the command line interface, navigate to the previously downloaded and unpacked FERMO directory, using the `cd` command (i.e. "change directory").  To show the contents of the current directory, the `dir` command can be used. This has to be done every time FERMO is started.

7. Once in the FERMO directory, create a Conda virtual environment by entering the command `conda create --name FERMO python=3.8`. This has to be done only the first time you run FERMO.

8. Activate the newly created virtual environment by entering the command `conda activate FERMO`. The prefix of the command prompt should switch to `(FERMO)`, to indicate the change in environment. This has to be done every time FERMO is started.

9. Install the packages required by FERMO in the newly created virtual environment by entering the command `pip install numpy pandas matchms pyteomics plotly dash dash-cytoscape dash_bootstrap_components networkx "ms2query==0.4.3" dash[diskcache] dash[celery]`. This has to be done only the first time you run FERMO.

10. To start FERMO, enter the command `python app.py` and enter the local IP address `127.0.0.1:8050` in any browser window. The dashboard should appear after a couple of seconds. If not, simply reload the browser window. Example data for testing can be found in the folder `example_data`. 

11. After use, do not forget to close the command line window in which FERMO runs, or terminate execution of the program by hitting ctrl+c.


#### macOS:


1. Download the FERMO zipped package to an easily accessible location to which you have write access, such as the Downloads folder or the Desktop. Unpack the package. This can be done using (free) software such as 7-Zip (https://www.7-zip.org/). Alternatively, you can also clone this repository.

2. Download and install the latest Miniconda3 version from the [Conda website](https://docs.conda.io/en/latest/miniconda.html). Install Miniconda3 by opening a terminal window, navigating to the Miniconda3 binary, and executing the command `bash Miniconda3-latest-MacOSX-x86_64.sh`. Accept the default settings and the license conditions. Alternatively, Anaconda can also be used, but its installation requires substantially more disk space. More details on the installation procedure can be found in [this Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html).

3. Once Miniconda3 is installed, close and re-open the terminal window to make changes take effect. Now, your terminal prompt should have the prefix `(base)`.

4. In the terminal window, navigate to the previously downloaded and unpacked FERMO directory, using the `cd` ("change directory") command. To show the contents of the current directory, the `ls` command can be used. This has to be done every time FERMO is started.

5. Once in the FERMO directory, create a Conda virtual environment by entering the command `conda create --name FERMO python=3.8`. This has to be done only the first time you run FERMO.

6. Activate the newly created virtual environment by entering the command `conda activate FERMO`. The prefix of the command prompt should switch to `(FERMO)`, to indicate the change in environment .This has to be done whenever FERMO is started.

7. Install the packages required by FERMO in the newly created virtual environment by entering the command `pip install numpy pandas matchms pyteomics plotly dash dash-cytoscape dash_bootstrap_components networkx "ms2query==0.4.3" "dash[diskcache]" "dash[celery]"`. This has to be done only at the first start of FERMO.

8. To start FERMO, enter the command `python app.py` and enter the local IP address `127.0.0.1:8050` in any browser window. The dashboard should appear after a couple of seconds. If not, simply reload the browser window. Example data for testing can be found in the folder `example_data`. 

9. After use, do not forget to close the command line window in which FERMO runs, or terminate execution of the program by hitting ctrl+c.

For Apple Mac laptops with the new M1 chip, the error `zsh: illegal hardware instruction ...` has been observed. If such an error occurs, the following commands can help to fix the problem:
```
$_ pip install virtualenv
$_ virtualenv ENV
$_ source ENV/bin/activate
$_ wget "https://github.com/tensorflow/tensorflow/archive/refs/tags/v2.4.1.zip"
$_ unzip v2.4.1.zip
$_ mv v2.4.1 tensorflow_v2.4.1.whl
$_ pip install ./tensorflow_v2.4.1.whl
```
Afterwards, repeat the command in point 7.


#### (Ubuntu) Linux

1. Download the FERMO zipped package to an easily accessible location to which you have write access, such as the Downloads folder or the Desktop. Unpack the package. Alternatively, you can also clone this repository.

2. Download and install the latest Miniconda3 version from the [Conda website](https://docs.conda.io/en/latest/miniconda.html). Install Miniconda3 by opening a terminal window, navigating to the Miniconda3 binary, and executing the command `bash Miniconda3-latest-Linux-x86_64.sh`. Accept the default settings and the license conditions. Alternatively, Anaconda can also be used, but its installation requires substantially more disk space. More details on the installation procedure can be found in [this Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html).

3. Once Miniconda3 is installed, there are two options to run FERMO. The easiest option is by double-clicking the startup script `FERMO_START_LINUX.sh`, which can be found in the FERMO directory. This script will start FERMO, create a conda environment, activate it, install the all dependencies, and open a browser window where FERMO can be used (refresh after a few seconds if there is nothing to see). However, on some Linux distributions, shell-scripts cannot be opened in the file explorer for security reasons. In this case, open a new terminal window, and execute the commands `chmod +x ./FERMO_START_LINUX.sh` and `./FERMO_START_LINUX.sh`. If that does not work, FERMO can also be started manually, as indicated below:

4. **Manual install and start of FERMO:** Open a new terminal window, navigate to the previously downloaded and unpacked FERMO directory, using the `cd` ("change directory") command. To show the contents of the current directory, the `ls` command can be used. This has to be done whenever FERMO is started.

5. Once in the FERMO directory, create a Conda virtual environment by entering the command `conda create --name FERMO python=3.8`. This has to be done only at the first start of FERMO.

6. Activate the newly created virtual environment by entering the command `conda activate FERMO`. The prefix of the command prompt should switch to `(FERMO)`, to indicate the change in environment. This has to be done whenever FERMO is started.

7. Install the packages required by FERMO in the newly created virtual environment by entering the command `pip install numpy pandas matchms pyteomics plotly dash dash-cytoscape dash_bootstrap_components networkx "ms2query==0.4.3" dash[diskcache] dash[celery]`. This has to be done only at the first start of FERMO.

8. To start FERMO, enter the command `python app.py` and enter the local IP address `127.0.0.1:8050` in any browser window. The dashboard should appear after a couple of seconds. If not, simply reload the browser window. Example data for testing can be found in the folder `example_data`. 

9. After use, do not forget to close the command line window in which FERMO runs, or terminate execution of the program by hitting ctrl+c.


### Quickstart Guide

#### Overview and terminology:

FERMO is designed to work with **untargeted, data-dependend acquisition (DDA) LC_MS/MS data**. While not strictly necessary, FERMO works best with **high resolution data** (mass deviation 30 ppm and less). To describe data, FERMO uses the terminology commonly used in metabolomics experiments:

- **Sample**: a contiguous instrument run, containing a number of scans, that are either **MS1** (surveying) scans, or **MS2** (collision cell) scans. 
- **Feature**: a LC-MS extracted ion chromatogram (EIC) peak with specific attributes such as a mass-to-charge-ratio *m/z*, retention time *RT*, and a tandem mass fragmentation spectrum. Identical features detected across multiple samples can be collapsed and summarized in a non-redundant *peaktable*.

#### Step-by-step guide

This guide covers the essential steps to process and analyze data with FERMO. For first-time users, an example dataset is available in the folder `example_data`, which is a subset of 11 samples of the dataset [MSV000085376](https://doi.org/doi:10.25345/C5412V), described in the article [Planomonospora: A Metabolomics Perspective on an Underexplored Actinobacteria Genus](https://doi.org/10.1021/acs.jnatprod.0c00807). 

For more information on the input data format, see the [Input data formats overview](https://github.com/mmzdouc/FERMO/wiki/Input-data-formats) in the FERMO Wiki.

1. Start FERMO by following the instructions in the installation guide above. On the landing page, two different pages can be accessed: the **Peaktable processing page (standard mode)** and the **Restart session page (loading mode)**. The **Peaktable processing page** allows to process the peaktable in the MZmine3 **‘*_quant_full.csv’** format. The **Restart session page** allows reloading previously saved FERMO sessions. This step-by-step guide focuses on the standard mode. 

2. Access the **Peaktable processing page (standard mode)** by clicking the button on the bottom of the **Landing page**.

3. On the **Peaktable processing page**, data can be loaded into the app, and processing parameters can be set. Load the files by clicking on the respective buttons. The minimum requirement to run the Peaktable processing mode are a **peaktable** and its accompanying **.mgf-file**. Input files are tested for correct formatting, and a message indicates pass or fail of the assessment. With respect to parameter settings, the default settings should match most data types but can be adjusted as needed. Information about the individual parameters can be found in the tooltips, which are triggered by hovering over the blue dots, or by accessing the respective page in the wiki. By default, the MS2Query annotation module is switched off since its relatively long calculation time might not be desired during a first test run. Once the required files are loaded, the calculation can be started by clicking the **'Start FERMO'** button at the bottom of the **Peaktable processing page**.

4. Since all calculations are performed locally, the length of the calculation depends on the processing power of the computer that is used for the analysis. Once all calculations are finished, FERMO will automatically reload and redirect to the dashboard view.

5. To view a specific sample, click on one of the rows in the **sample table (1)**. 

6. A click on a row in the **sample table (1)** triggers the sample **chromatogram view (2)**, which displays the features detected in the sample, color-coded after their properties. Hovering over a feature presents general information, and clicking triggers the **feature information table (3)**, the **chromatogram overview (4)**, and the **spectral similarity/molecular networking view (5)**. 

7. In the **feature information table (3)**, all information about a feature is displayed. This includes its general attributes, its calculated scores, its annotations, and its spectrum similarity clique (a summary of feature relatedness based on MS2 spectrum similarity). If metadata on groups was provided, this data is displayed too. 

8. In the **chromatogram overview (4)**, the distribution of the feature across samples is displayed, which can be used to determine the sample most suitable for further exploration. 

9. The **spectral similarity/molecular networking view (5)** shows the relatedness of the feature with other features, based on similarity of their spectra. Clicking nodes or edges triggers the **node information table** or **edge information table**, respectively. These tables can be found below the network view. The nodes in the **Spectral similarity/molecular networking view** are color-coded if they are detected in the selected sample, and if they are specific to the group the selected sample belongs to (only if metadata on groups was provided). The same color-code is used in the smaller chromatogram beneath the **sample chromatogram overview (2)**, which indicates the spatial distribution of related features in the chromatogram. 

10. In the **filter and download panel (6)**, different filters can be set that filter the peaks in the **sample chromatogram view (2)** and display them in a different color, to indicate that they are below the selected threshold. Details on the different scores, the calculations, and suggested analysis strategies can be found in the wiki.

11. The analysis can be stored by clicking on **'Save FERMO session file (JSON)'**, which can be found in the **filter and download panel (6)**. This generates a text-based session file in the JSON format that can be used to load the dashboard view in the **Restart session page (loading mode)** mentioned in step **1.** of this quickstart guide. The session file can also be shared to other users, which allows to work collaboratively.

A more thorough guide, including information on scores and data processing, can be found in the Wiki (TBA).


## For Developers

### Contributing

For details on our code of conduct, and the process for submitting pull requests to us, please read [CONTRIBUTING.md](CONTRIBUTING.md).

### Versioning

We use [Semantic Versioning](http://semver.org/) for versioning.

## Authors

- **Mitja M. Zdouc** - *Lead developer* -
- **Hannah E. Augustijn** - *Design* -
- TBA - 

See also the list of [contributors](https://github.com/mmzdouc/FERMO/contributors) who participated in this project.

## Acknowledgments

TBA


