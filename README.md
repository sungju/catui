# catui
crash analysis tool user interface

### Setup environment

- Run 'make' to install required packages

```
$ cd catui/
$ ls
LICENSE           README.md         docs/             setup.py
Makefile          catui/            requirements.txt  tests/

$ make
pip3 install -r requirements.txt
Requirement already satisfied: pexpect in /usr/local/lib/python3.7/site-packages (from -r requirements.txt (line 1)) (4.8.0)
Requirement already satisfied: ansi2html in /usr/local/lib/python3.7/site-packages (from -r requirements.txt (line 2)) (1.5.2)
Requirement already satisfied: ptyprocess>=0.5 in /usr/local/lib/python3.7/site-packages (from pexpect->-r requirements.txt (line 1)) (0.6.0)
Requirement already satisfied: six in /usr/local/lib/python3.7/site-packages (from ansi2html->-r requirements.txt (line 2)) (1.14.0)
$
```

- Should have server list as ${HOME}/.catuirc
  - Sample is located as catui/catui/_catuirc
  - Copy this and modify to fit your requirement

```
$ cp catui/_catuirc ${HOME}/.catuirc
$ vi ~/.catuirc
```

### Start the tool

- Run the below in local system as it uses GUI

```
$ python catui/cagui.py
```
