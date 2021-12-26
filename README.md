

## File-Update
---
Copy a file to a number of assigned destinations, and copies the latest version of the file whenever the program is invoked for an update for that file.

## Description
---
`file-update`, which can also be shortened to `fud` in the cli, is a program that copies a file to a number of preassigned directories. The main file to be copied is also called source file, abbreviated to **SRC**, or origin file. While directories where the SRC to be copied are called **DST** or **DIRS**.

## Requirements
---
1. Git
2. Python >= 3.6

## Installation
---
Currently, the program isn't uploaded to PyPI until it reaches certain maturity, however you can download it from github using `git` and use `pip` to install it directly. No elevated privileges required.

```
git clone www.github.com/falbloshi/file-update.git
cd file-update
python3.* -m pip install .
```
This will install it in the `~/.local/python3.*/site-packages` of your user level python folder.

## Usage
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
`/HOME/USER/.config/file-update/cache.json`  
And for windows in  
`C:\ProgramData\file-update\cache.json`

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
And if you want to update myfile.txt everywhere it was stored after editing it:  
`fud myfile.txt -u -v`

To confirm:  
`diff -s myfile.txt aunt/myfile.txt`
### --simulate or -s
Will simulate copy process, and doesn't perform real changes either to the specified folders or in cache.json file.
### --status
Displays file status of every copy. It will display a sha1 hash as well as time elapsed from last update. `-v` Will display the full hash value
### --swap \[SWP\]
This is will swap the source file with the swap file specified. They should share the same name.  
`fud myfile.txt --swap aunt/myfile.txt -v`
### --quiet or -q
Will display no output
### -r 