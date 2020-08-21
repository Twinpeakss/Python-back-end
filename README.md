# General info

It's small python project which is written to create and import some data into database based on Json file.
Implementing line interface for some database quieries.

## Technologies
Project is created with:
* Python 3.8.3
* Peeweee ORM
* SQLite database
* Click command line

## How To Use
Start with clone this repository:
```sh
$ git clone https://github.com/Twinpeakss/Python-back-end
```
To run this project, install some packages if not already exist:

* Click
```sh
pip install click
```
* Peewee
```sh
pip install peewee
```


## Using

Just run "script.py." then you will get the list of all available commands.

## Launch
For running projects files, just use command below:

```sh
$python script.py

```

## Available commands

![GIF](http://g.recordit.co/jHn4h5rWcy.gif)

Or for example just write this to get all the peoples in given dates as parameters:

```sh
python script.py get-dates-between -f '1971-05-20' -t '1992-05-06'

```
