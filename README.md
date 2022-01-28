# MPLogger
Multi-processing capable print-like logger for Python

## Requirements and Installation

Python 3.8+ is required

### Pip

`pip install mplogger`

### Manual

[_Poetry_](https://python-poetry.org/) and (optionally) [_GNU Make_](https://www.gnu.org/software/make/) are required.

1. `git clone https://github.com/ELTE-DH/webarticlecurator.git`
2. Run `make`

On Windows or without Make (after cloning the repository):

1. `poetry install --no-root`
2. `poetry build`
3. `poetry run pip install --upgrade dist/*.whl` (the correct filename must be specified on Windows)

## Usage

### Single-process

```python
from MLPlogger import Logger

# Initialize logger (default: STDERR only with INFO level)
logger = Logger(log_filename, logfile_mode, logfile_encoding, logfile_level, console_stream, console_level, console_format, file_format)

logger.log('INFO', 'First argument log level as string')
logger.log('WARNING', 'THIS IS A WARNING!', 'In multiple lines', 'just like print()', sep='\n')
logger.log('CRITICAL', 'Can also set line endings!', end='\r\n')
```

### Multi-process

```python
from itertools import repeat
from multiprocessing import Pool, Manager, current_process

from MLPlogger import Logger

def worker_process(par):
    state, lq = par
    retl = []
    for n in range(100):
        lq.log('WARNING', f'{current_process().name} message{state} {n}')
    lq.log('WARNING', f'{current_process().name} finished')
    return retl

log_obj = Logger('test.log', 'w')  # Apply all parameters for logger here!
log_obj.log('INFO', 'NORMAL LOG BEGIN')  # Normal logging
with Manager() as man:
    log_queue = man.Queue()
    with log_obj.init_mp_logging_context(log_queue) as mplogger, Pool() as p:
        # Here one can log parallel from all processes!
        return_queue = p.imap(worker_process, zip(range(10), repeat(mplogger)), chunksize=3)
        for _ in return_queue:
            pass
log_obj.log('INFO', 'NORMAL LOG END')  # Normal logging
```

# Licence

This project is licensed under the terms of the GNU LGPL 3.0 license.
