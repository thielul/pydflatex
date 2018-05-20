This is a fork of the pdflatex python wrapper [pydflatex](https://github.com/olivierverdier/pydflatex) by Olivier Verdier. I modified a couple of things to finally **silence** LaTeX (no visible auxiliary files and useless output messages). Here's what I did:
* I use the -output-directory=.tmp to move all the annoying auxiliary files to the hidden directory .tmp. The final PDF output file is then moved back from here to the base directory.
* I added the -synctex=1 option.
* I removed the -recorder option.

*Installation:* [Download](https://github.com/thielul/pydflatex/archive/master.zip) this repository and run ```python setup.py install --record files.txt```

*Uninstallation:* Do ```cat files.txt | xargs rm -rf```

(You have to add a ```sudo``` depending on your permissions.)