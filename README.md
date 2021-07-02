# [« Home](https://github.com/STI-Team/ontogen) / ontogen
OnotoGen: Software system for analyzing and transforming spreadsheets into ontologies and related data sets
This document describes the command-line interface for the <code>OntoGen(og)</code> system.

## Installation Instructions

Run the following commands in order in a cmd.exe
```
git clone https://github.com/STI-Team/ontogen
cd ontogen

python3 -m venv ont_env
ont_env\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```
If python3 is not installed, find out what version of python 3 is installed and use that instead
### A Simple Example
```
python main.py --name=f:\test

>>> Такой путь существует:  f:\test
>>> Такой путь существует:  f:\test/json
>>> Такой путь существует:  f:\test/json/jsondocs
```
