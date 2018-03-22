"""Module containing writer classes for writing Fastq files"""
import gzip
import io
from gdc_fastq_splitter.fastq.report import BaseReport

class FastqWriter:
    """Base Fastq writer class"""
    def __init__(self, fname, **kwargs):
        self.fname = fname
        self.fobj = gzip.open(self.fname, mode='wb', compresslevel=6) if self.fname.endswith('.gz') else open(self.fname, 'wb')
        self.f = io.BufferedWriter(self.fobj)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __iadd__(self, record):
        self.f.write(bytes(record))
        return self

    def close(self):
        self.f.flush()
        self.fobj.close()

class FastqWriterWithReport(FastqWriter):
    """Writer class with a report"""
    def __init__(self, fname, reporter, **kwargs):
        super().__init__(fname, **kwargs)
        self.reporter = reporter

    @classmethod
    def from_record_and_prefix(cls, prefix, record, report_cls=BaseReport):
        fbase = '{0}_{1}_R{2}'.format(prefix, record.read_key, record.read_pair)
        fname = '{0}.fq.gz'.format(fbase)
        rname = '{0}.report.json'.format(fbase)
        return cls(fname, report_cls(rname, flowcell_barcode=record.flowcell, lane_number=record.lane))

    def __iadd__(self, record):
        self.reporter += record
        self.f.write(bytes(record))
        return self

    def close(self):
        super().close()
        self.reporter.write_to_json()

