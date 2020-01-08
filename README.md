# albumart
#### Download high resolution albumart

### Depends
- Python 3.6
- argparse
- requests

### Install

1. Clone this repository
2. Run `install.sh` in a command terminal.  
This will make `albumart.py` executable and copy it to `/usr/local/bin/albumart`.


### Usage

```Bash
albumart mykki dog
```
This will find cover art for _Gay Dog Food_ by _Mykki Blanco_ and dowload it to the current directory as `Mykki Blanco - Gay Dog Food.png`

By default the first argument is freetext and will match on multiple attributes, like artist, album, composer, genre etc., but can be limited using the `--attr` argument. Other arguments are also available. See `albumart -h` for an overview.


<sub>_Tested on OS X 10.11.6 and Python 3.6.2_</sub>


