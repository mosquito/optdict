OptDict
=======

Module for python, for easy to use command line options, validation options values and configuration from JSON file

== Example ==

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
                "validator": validators.Valid(lambda addr: ".".join([str(j) for j in [int(i) for i in addr.split(".")] if j >=0 and j<256]) == addr)

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
                "action": "store_const"
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
            }
        },
        # Meta section
        "__meta__": {
            # Help messages for sections
            "sections_help": {
                "debug": "Debugging options",
                "main": "Main options"
            },
            "sections_text": {
                "main": "This section contains main options for test this..."
            }
        }
    }

    if __name__ == "__main__":
        print (str(options, args = Parser(options_dict).parse_args())
```

And run it:

    $ test.py --help
    Usage: test.py [options]

    Options:
      -h, --help      show this help message and exit
      --config=FILE   Set options from JSON file (generate example by --gen-conf).
      --gen-conf      Print sample config file and exit.

      Debugging options:
        -d            Debuging output

      Main options:
        This section contains main options for test this...

        -l, --listen  Listen address

== Validations ==

The module provides this validators:
* RequireAll(func1[, func2, ... funcN]) {synonym: Require}
* RequireOnce(func1[, func2, ... funcN])
* ValidAll(name1[, name2 ... nameN]) {synonym: Valid}
* ValidOnce(name1[, name2 ... nameN])
* Conflict(name1[, name2 ... nameN])
* ValidationQueue(Validator0[, Validator1])

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

=== RequireAll ===
arguments: (*names)
synonym: Require



=== RequireOnce ===
arguments: (*names)

=== Conflict ===
arguments: (*names)


=== ValidAll ===
arguments: (*funcs, critical=True)
synonym: Valid

If at least one function returns false, an exception is thrown.

=== ValidOnce ===
arguments: (*funcs, critical=True)

If at least one function returns true, an exception is thrown.

=== ValidationQueue ===
