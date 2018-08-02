# Arithmetical Calculator

An application to solve arithmetical operations using a computation server and a client to send operations to it.

## Getting started

These instructions will help you set up the project

### Prerequisites

You can use virtualenv or conda to install dependencies. Just take care of python version, which is 3.7.
The requirements to install are included in requirements.txt, so you can run:

```bash
pip install -r requirements.txt
```

### Running the code

The server part has to be started first to let the client connect to it.

#### Server

To run the server with default options.

```bash
python server.py
```

The port on which the server runs can be changed with the option *--port.*

```bash
python server.py --port 1234
```

The server uses multiprocessing to speed up calculations. To change the number of processes you can use the option *-p* or *--processes*.

```bash
python server.py -p 4
python server.py --processes 4
```

#### Client

The client has two positional arguments that are mandatory for the execution.
Both *input_file* and *output_file* must be provided in order to know from where to read the operations and where to store the results.

```bash
python client.py path/to/input_file.txt path/to/output_file.txt
```

Additionally, *--port* and *--host* can be provided in case that the server doesn't use the default settings.

```bash
python client.py --host remote-host --port 80 path/to/input_file.txt path/to/output_file.txt
```

#### Both

For both server and client, *--version* and *--help* (or *-h*) arguments will show respectively the version of the program and the help utility.

```bash
python server.py --version
python server.py -h
python client.py --version
python client.py -h
```

Likewise, both have three levels of logging, default is set to info while *-q* provides quiet mode, just showing warnings and errors, and *-v* offers verbose mode which shows debug logs on top of info, warnings and errors.

```bash
python server.py -q
python server.py -v
python client.py -q path/to/input_file.txt path/to/output_file.txt
python client.py -v path/to/input_file.txt path/to/output_file.txt
```

A log file will be created in a logs folder inside the project. Log file is always set to show warnings and errors only.

## License

This project is licensed under the UnLicense - see the [LICENSE](LICENSE) file for details