## Summary
A library application to use alongside audacious

## Usage
If you decide to start using this application, you will need to have Python installed with the following packages:

python-mutagen (for their ID3-tag reading)
python-tkinter (for the interface)
audacious

In debian-based linux systems they can be installed using apt-get <package name>. In other systems, look for the home page of the packages and download it from there.

Take caution using this program: It is still under construction!

There is a simple script in the root directory that can open the program from anywhere.

Known bugs:
- Albums are shown regardless of artist (if you'd first select an artist, and then album "Unknown" all "Unknown" album entries will be shown in the third column)
- The file browser disregards selections, you should enter the folder you want to scan before clicking OK
- The first line in `library.maf' is disregarded
