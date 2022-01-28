#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from itertools import repeat
from multiprocessing import Pool, Manager, current_process

from mplogger import Logger


def worker_process(par):
    state, lq = par
    retl = []
    for n in range(100):
        lq.log('WARNING', f'{current_process().name} message{state} {n}')
    lq.log('WARNING', f'{current_process().name} finished')
    return retl


def test_entrypoint():
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


if __name__ == '__main__':
    test_entrypoint()
