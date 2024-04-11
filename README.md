# Commands

```
Usage: example-cli [OPTIONS] COMMAND [ARGS]...

  Simple CLI example

Options:
  --global-example TEXT  A global option
  --option-one TEXT      First option
  --option-two TEXT      Second option
  -V, --version          Show the version and exit.
  -h, --help             Show this message and exit.

Commands:
  abort                      Generates an exception
  expanded-path              Expand option path
  help                       Print help
  readme (doc)               Generates a README.rst
  subgroup (subgroup-alias)  A sub group
  version                    Print version
```

## example-cli abort

```
Usage: example-cli abort [OPTIONS]

  Generates an exception on purpose (test)

Options:
  -h, --help  Show this message and exit.
```

## example-cli expanded-path

```
Usage: example-cli expanded-path [OPTIONS]

  Command with expanded path option

Options:
  --file PATH  File path which expands
  -h, --help   Show this message and exit.
```

## example-cli help

```
Usage: example-cli help [OPTIONS]

  Print help

Options:
  -h, --help  Show this message and exit.
```

## example-cli readme

```
Usage: example-cli readme [OPTIONS]

  Uses gen_doc click-skeleton helper to generates a complete readme

Options:
  --output [rst|markdown]  README output format  [default: rst]
  -h, --help               Show this message and exit.
```

## example-cli subgroup

```
Usage: example-cli subgroup [OPTIONS] COMMAND [ARGS]...

  I am a subgroup!

Options:
  -h, --help  Show this message and exit.

Commands:
  help        Print help
  subcommand  A sub command
```

### example-cli subgroup subcommand

```
Usage: example-cli subgroup subcommand [OPTIONS]

  I am a subcommand!

Options:
  --myoptions TEXT  A splitted option
  -h, --help        Show this message and exit.
```

## example-cli version

```
Usage: example-cli version [OPTIONS]

  Print version, equivalent to -V and --version

Options:
  -h, --help  Show this message and exit.
```
