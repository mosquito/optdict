OptDict
=======

Python module for easy to use command line options. With validation options values and configuration from JSON file.

## Example

Example usage for command line params
```python
from optdict import Parser, validators

options_dict = {
    # Params section "main"
    "main": {
        "listen": {
            # Command line keys (require)
            "keys": ["-l", "--listen"],

            # Validator call for value (optional)
            "validator": validators.Valid(lambda addr: ".".join([str(j) for j in [int(i) for i in addr.split(".")] if j >=0 and j<256]) == addr),

            # Help text (optional)
            "help": "Listen address",

            # Default value (optional default None)
            "default": "127.0.0.1",

            # Action (optional)
            # support all OptParse options
            # * store_true - stores true (default False)
            # * store_false - stores false (default True)
            # * store_const - stores constans
            # * count - stores the number of repetitions of the key (if only key is single symbol)
            # * callback - run function defined to "callback" option (see OptParse docs)
            "action": "store_const"
        },
        "test": {
            "keys": ["-t"],
            "help": "Test someone",
            "action": "callback",
            "callback": lambda x: exit(0),
        }
    },
    # Another section
    "debug": {
        "debug": {
            "keys": ['-d'],
            "action": "count",
            "default": 0,
            "type": "int",
            "help": "Debuging output"
        },
        "__meta__": {
            "help": "Main section",
            "text": "Alternative syntax"
        }
    },
    # Meta section
    "__meta__": {
        # Help messages for sections
        "sections_help": {
            "debug": "Debugging options",
        },
        "sections_text": {
            "Debug": "This section contains debug options for test this..."
        }
    }
}

if __name__ == "__main__":
    options, args = Parser(options_dict).parse_args()

    print "Listen:", options.main_listen
    print "Debug:", options.debug_debug
```

And run it:

    $ python test.py --help
    Usage: test.py [options]

    Options:
      -h, --help            show this help message and exit
      --config=FILE         Set options from JSON file (generate example by --gen-conf).
      --gen-conf            Print sample config file and exit.

      Debugging options:
        -d                  Debuging output

      Main options:
        This section contains main options for test this...

        -t                  Test someone
        -l MAIN_LISTEN, --listen=MAIN_LISTEN
                            Listen address

## Validations

The module provides this validators:
* RequireAll(func1[, func2, ... funcN]) {synonym: Require}
* RequireOnce(func1[, func2, ... funcN])
* ValidAll(name1[, name2 ... nameN]) {synonym: Valid}
* ValidOnce(name1[, name2 ... nameN])
* Conflict(name1[, name2 ... nameN])
* ValidationQueue(Validator0[, Validator1])
* Modifier(func1[, func2 ... funcN)

Call example:

```python
options_dict = {
    # Params section "main"
    "main": {
        "listen_address": {
            "keys": ["-l", "--listen"],
            "validator": validators.ValidOnce(
                lambda addr: ".".join([str(j) for j in [int(i) for i in addr.split(".")] if j >=0 and j<256]) == addr,
                lambda path: os.path.exists(os.path.basedir(path),
            )
            "help": "Listen address",
        },
        "port": {
            "keys": ["-p", "--port"],
            # if "unix_socket" option defined, call exception
            # key critical - if true then exit(128)
            "validator": Conflict("unix_socket", critical=True)
        },
        "unix_socket": {
            "keys": ["--socket"],
            "help": "Force listen unix socket"
        }
    }
}
```

### RequireAll
arguments: (*names)
synonym: Require

Test if all options from args is set

example:

    RequireAll("main_listen", "main_port")

### RequireOnce
arguments: (*names)

Test if once option from args is set

example (for optopn test from main section (main_test)):

    RequireOnce("main_listen", "main_port", "main_socket")

### Conflict
arguments: (*names)

Test if other options not set (and bool(default) == False)

example (for option name "main_listen"):

    Conflict("main_test") # Exception if option test from main section is set

### ValidAll
arguments: (*funcs, critical=True)
synonym: Valid

If at least one function returns false, an exception is thrown.

example:

    Valid(
        lambda x: x >= 0,
        lambda x: x < 256
    )

### ValidOnce
arguments: (*funcs, critical=True)

If at least one function returns true, an exception is thrown.

example:

    ValidOnce(
        lambda x: x >= 0 and x < 256,
        lambda x: x == -1
    )

### ValidationQueue
Validate Multiple validators

example:

    ValidateQueue(
        ValidAll(
            lambda x: x >= 0,
            lambda x: x != -1,
        ),
        ValidOnce(
            lambda x: x < 0,
            lambda x: x > 10,
        )
    )

### Modifier
Modify value

example:

    Modifier(
        lambda f: open(f).read()
    )

## Configuration from JSON file
OptDict added options "--config" and "--gen-conf" in root section.

### Generate example configuration
To create a configuration example, a call option "generate". Configuration will be printed.

### Read configuration from file
Create a sample configuration as follows:

    # python test.py --gen-conf | tee /tmp/sample.json
    {
     "debug": {
      "debug": 0
     },
     "main": {
      "test": null,
      "listen": "127.0.0.1"
     }
    }

Edit /tmp/sample.json:

    {
     "debug": {
      "debug": 999
     },
     "main": {
      "test": null,
      "listen": "0.0.0.0"
     }
    }

Run test with config file:

    $ python test.py --config /tmp/sample.json
    Listen: 0.0.0.0
    Debug: 999

Start options override the config file:

    $ python readme.py --config /tmp/sample.json -l 10.0.0.1
    Listen: 10.0.0.1
    Debug: 999

## Options usage
Example usage for optdict after parse options

```python
if __name__ == "__main__":
    options, args = Parser(options_dict).parse_args()

    print "Listen:", options.main_listen
    print "Debug:", options.debug_debug
```

### Attribute naming
The naming attribute is the next rule:

    section_optionname

thus, the option "listen" in the section "main" is an attribute of "main_listen"

### Current config (dictionary)
Method options.to_dict() returns dictionary of dictionaries of values
