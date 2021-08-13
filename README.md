# Moving files to specific directories utility
The TransferFiles utility is used to transfer files from one device to 
another device using the cloud as intermediary location. What makes 
TransferFiles unique is that the directory structures on both source and
target devices can be different. A local configuration file (transfiles.ini)
stores the information required for the transfer of each file to be done 
correctly.

The utility works on Android and on Windows. It is particularly useful if you 
code on your tablet or smartphone and in parallel use an IDE on your Windows 
pc.

More generally, it can be used to transfer any type of files between your 
devices without having each time to care for the destination dir.

## Using the utility
TransferFiles is a command line utility utility. When you launch the 
application with `python transferfiles.py` without specifying any command line
argument, the app displays a menu listing the projects defined in the local
configuration file (see below the config file format). A project is a section
of the config file in which several parameters are defined, like the local
project dir, the local project destination sub dirs associated to file name 
wildchard patterns. Also, excluded file patterns or excluded local project
sub directories can be specified.

After you selected a project, the utility checks if files of this project are
available in the cloud dir corresponding to this project. If it is the case,
the list of available files are displayed and the user can decide if those
files must be downloaded and transfered to their local destination. At this
stage, the user can choose not to download the files. If so, he will then be
asked if he wants instead to upload local files to the cloud, provided that
local files exist whose modification date is after the last synch date time
for this project as stored in the configuration file.

In both case if you download or you upload files, the last synch date time
for this project is updated in the local configuration file.

If no files are available on the cloud for the project you just selected, the
utility then display a list of local files whose modification date is after the 
project last synch date time. 

If neither cloud files nor local modified files exist, then the utility ends
up without performing anything.

Though, there's is an additional action the user can perform: he can choose
to modify the last synch date time for the selected project. Then, relaunching
the utility will potentially display a different list of modified files.

## Usage scenarios

## Project class diagram
<p align="center">
  <img src="images/class_diagram.jpg" width="600" title="Audio Download class diagram">
</p>

## Required libraries
- requests
- configobj
- dropbox

## Version history
- 2.2 Added possibility to keep files on cloud after downloading them so that they can 
  be downloaded on another device
- 2.1 Added utility loop execution
- 2.0 Added directory download: as a result, the directory structure on the 
synchronized devices is identical
- 1.3 Bug fix + user input minor improvements
- 1.2 Added update synch time option if no files should be uploaded
- 1.1 Added handling command line arguments
- 1.0 Working and unit tested version