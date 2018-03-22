import os

import multiprocessing

from gdc_fastq_splitter.utils import get_logger
from gdc_fastq_splitter.fastq.reader import FastqReader
from gdc_fastq_splitter.fastq.writer import FastqWriterWithReport
from gdc_fastq_splitter.fastq.illumina import infer_fastq_type 

def process_fastq(input_file, output_prefix, logger_name='fastq_processing', log_itvl=1000000):
    logger = get_logger(logger_name)
    ibase = os.path.basename(input_file)
    logger.info("Processing fastq: {0}".format(ibase))

    fq_cls = infer_fastq_type(input_file) 
    logger.info("Inferred fastq class {0} in fastq {1}".format(fq_cls[0], ibase))

    reader = FastqReader(input_file, record_cls=fq_cls[1])
    count = 0
    writers = {}
    try:
        for record in reader:
            count += 1
            if count % log_itvl == 0:
                logger.info("Processed {0} records from {1}".format(count, ibase))

            key = record.read_key
            if key not in writers:
                logger.info("Found read key {0} in fastq {1}".format(key, ibase))
                writer = FastqWriterWithReport.from_record_and_prefix(record, output_prefix)
                logger.info("Output file for read key {0} in fastq {1} is {2}".format(key, ibase, writer.fname)) 
                writers[key] = writer
            writers[key] += record

    finally:
        reader.close()
        for key in writers:
            writers[key].close()
    logger.info("Processed a total of {0} records from {1} and found {2} read keys".format(count, ibase, len(writers)))
    return ({key : writers[key].reporter.to_dict() for key in writers}, count)

def do_process(args):
    return process_fastq(*args)

def main_paired(args):
    pool = multiprocessing.Pool(2)
    tasks = [(i, args.output_prefix) for i in [args.fastq_a, args.fastq_b]]
    results = pool.map(do_process, tasks) 
 
    result_a, result_b = results
    result_a_input_total = result_a[1]
    result_b_input_total = result_b[1]

    if result_a_input_total != result_b_input_total:
        msg = "The input files had different number of records! ({0}, {1})".format(result_a_input_total, result_b_input_total)
        logger.error(msg)
        raise ValueError(msg)

    result_a_data = result_a[0]
    result_b_data = result_b[0]
    if len(result_a_data) != len(result_b_data):
        msg = "The input files had different number of read keys! ({0}, {1})".format(len(result_a_data), len(result_b_data))
        logger.error(msg)
        raise ValueError(msg)

    a_keys = list(result_a_data.keys())
    b_keys = list(result_b_data.keys())
    sdiff = set(a_keys).symmetric_difference(set(b_keys))
    if sdiff:
        msg = "These read keys were not found in both files: {0}".format(",".join(list(sdiff)))
        logger.error(msg)
        raise ValueError(msg)

    written_a = 0
    written_b = 0
    for key in a_keys:
        a_fil = result_a_data[key]['metadata']['fastq_filename']
        a_ct = result_a_data[key]['metadata']['record_count']
        b_fil = result_b_data[key]['metadata']['fastq_filename']
        b_ct = result_b_data[key]['metadata']['record_count']

        if a_ct != b_ct:
            msg = "The output files ({0}, {1}) have different totals! ({2}, {3})".format(a_fil, b_fil, a_ct, b_ct)
            logger.error(msg)
            raise ValueError(msg)
        written_a += a_ct
        written_b += b_ct

    if written_a != result_a_input_total:
        msg = "The number of records input and output doesn't match! ({0}, {1})".format(result_a_input_total, written_a)
        logger.error(msg)
        raise ValueError(msg)

    if written_b != result_b_input_total:
        msg = "The number of records input and output doesn't match! ({0}, {1})".format(result_b_input_total, written_b)
        logger.error(msg)
        raise ValueError(msg)

def main_handler(args):
    logger = get_logger('handler')
    
    if args.fastq_b:
        assert args.fastq_a != args.fastq_b
        logger.info('Running in paired mode')
        main_paired(args)
