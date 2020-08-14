# slippi-replay-renamer
Renames slippi replays according to a template defined by the user.

## Installation

I'll work on getting an executable together, but for now you need to use this with a python3 installation on your machine, as well as having py-slippi installed.

Place the executable in a directory with .slp files, or a directory with subdirectories containing .slp files. Slippi stores your replays to C:\Users\Current_User\Documents\Slippi by default.

Run the executable and select the template you want to use.

## Templates

slippi-replay-renamer comes prepackaged with a few premade templates, but you can also make your own.

A template looks like this:
```
{year}-{month}-{day} {p1_char} vs {p2_char} on {stage}
```

That template results in a filename like this:
```
2020-8-1 Falco vs Sheik on Yoshi's Story.slp
```

The words inside {} are replaced with the info from each respective game. Below is a list of supported terms.

### Supported terms

Currently the supported terms to look for in the replays are the following:
```
|Term                         |Value from replay                  |
|-----------------------------|-----------------------------------|
|{year}, {month}, {day},      |The respective values from the date|
|{hour}, {minute}, {second}   |the game was originally played.    |
|_____________________________|___________________________________|
|{p1_char}, {p2_char}         |The character played by player 1   |
|                             |and player 2 respectively.         |
|_____________________________|___________________________________|
|{stage}                      |The stage played in the match.     |
|_____________________________|___________________________________|
|{duration}                   |The duration of the game in number |
|                             |of frames.                         |
|_____________________________|___________________________________|
|{p1_name}, {p2_name}         |Netplay name of player 1 and       |
|                             |player 2 respectively.             |
|_____________________________|___________________________________|
```

The program will give you an error if you attempt to use a term that is not mentioned in this list.

### Invalid characters

Some characters are not valid to be used in filenames. For that reason you will not be able to use them in your template. The invalid characters are the following:
```
< > : " / \ | ? *
```

## Built With

* [py-slippi](https://github.com/hohav/py-slippi) - The API used to access the .slp-files

## Authors

* [**Blink**](https://twitter.com/BlinkSSBM) - *Initial work*

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE.md](LICENSE.md) file for details

## Brult?

Brult.
