"""Main entrypoint for gdc-fastq-splitter CLI"""
import argparse
from signal import signal, SIGPIPE, SIG_DFL

from gdc_fastq_splitter import VERSION
from gdc_fastq_splitter.utils import get_logger
from gdc_fastq_splitter.handler import main_handler
signal(SIGPIPE, SIG_DFL)

def main(args=None):
    """The main method for gdc-fastq-splitter"""
    logger = get_logger('gdc-fastq-splitter')

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=VERSION)

    parser.add_argument('-o', '--output-prefix', required=True, type=str,
        help='The output prefix to use for output files.')

    parser.add_argument('fastq_a', help='Fastq file to process')
    parser.add_argument('fastq_b', nargs='?', help='If paired, the mate fastq file to process')
    options = parser.parse_args(args=args)
    main_handler(options)

if __name__ == '__main__':
    main()
