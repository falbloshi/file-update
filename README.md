File-Update
---
Copy a file to a number of assigned destinations, and copies the latest version of the file whenever the program is invoked for an update for that file.
Description
---
`file-update`, which can also be shortened to `fud` in the cli, is a program that copies a file to a number of assigned directories. The main file to be copied is also called source file, abbreviated as **SRC** or origin file. While directories where the SRC to be copied are called **DST** or **DIRS**.

The purpose behind this program is that we wanted to save backups of password banks accross our storage devices and update them whenever the main bank is updated.  
Requirements
---
1. Git
2. Python >= 3.6
Installation
---
Currently, the program isn't uploaded to PyPI until it reaches certain maturity, however you can download it from github using `git` and use `pip` to install it directly. No elevated privileges required. Change python3.6 based on your own installed version.  
```
git clone www.github.com/falbloshi/file-update.git
cd file-update
python3.6 -m pip install .
```  
This will install it in the `~/.local/python3.6/site-packages` of your user level python folder.
Uninstallation
---
`python3.6 -m pip uninstall file-update`  
Or delete it manually from  
`~/.local/python3.6/site-packages/file-update` for *Nix  
`C:\Users\User\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\file-update` for Windows 7 and up.  
Usage
---
### --add or -a
As an example, we have a file structure that looks like this:

```  
.
├── myfile.txt
├── aunt
├── parent
│   └── child
└── uncle
    └── cousin1
```  
To add _myfile.txt_ and copy it to any destination(s)(-v is the --verbose command, shows more information):  
`fud myfile.txt -a aunt/ parent/child parent/ uncle/cousin1 -v`   
If cache.json did not exist, it will be created at  
`/HOME/USER/.cache/file-update/cache.json`  
And for windows in  
`C:\ProgramData\File-Update\cache.json`  
Now, our current file structure will look like this:
```
.
├── myfile.txt
├── aunt
│   └── myfile.txt
├── parent
│   ├── myfile.txt
│   └── child
│       └── myfile.txt
└── uncle
    └── cousin1
        └── myfile.txt
```  
### --update or -u
Update myfile.txt everywhere it was stored after editing it:  
`fud myfile.txt -u -v`  
To confirm:  
`diff -s myfile.txt aunt/myfile.txt`
### --simulate or -s
Simulates copy process; doesn't perform real changes either to the specified folders or in cache.json file.
### --status
Displays file status of every copy. It will display a sha1 hash as well as time elapsed from last update. `-v` Will display the full hash value.
### --swap \[SWP\]
Swaps the source file with the swap file specified. They should share the same file name. The swap file becomes the new source file.  
`fud myfile.txt --swap aunt/myfile.txt -v`
To reverse the above command.
`fud aunt/myfile.txt --swap ./myfile.txt -v`
### --quiet or -q
Will display no output. `--status` overrides quiet. 
### --remove-dir or -r 
Removes directory listed in the cache file specific to the source file. Reverse of --add.
```
fud myfile.txt --remove-dir aunt/
Directory removed from future updates
```
### --delete or -d
Deletes a source file entry from cache.json. Doesn't delete actual file or its related copy folders.
```fud myfile.txt -d```
### --verbose or -v
Displays more messages and information to the user.
```fud myfile.txt --add aunt/ uncle/cousin1 -v```
### --version
Displays version number and exits.
LICENSE
---
MIT License. Found in LICENSE file. 