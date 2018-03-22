"""Module containing base reader class"""
import gzip
import io

from gdc_fastq_splitter.fastq.base import FastqRecord

class FastqReader:
    """Base fastq reader"""
    def __init__(self, fname, record_cls=FastqRecord):
        self.fname = fname
        self.record_cls = record_cls
        self._next = None
        self.fobj = gzip.open(fname, 'rb') if fname.endswith('.gz') else open(fname, 'rb')
        self.f = io.BufferedReader(self.fobj)

    def __iter__(self):
        return self

    def next(self):
        seqid = self.f.readline().decode("utf-8").rstrip('\r\n')
        sequence = self.f.readline().decode("utf-8").rstrip('\r\n')
        qid = self.f.readline().decode("utf-8").rstrip('\r\n')
        qual = self.f.readline().decode("utf-8").rstrip('\r\n')

        if qual:
            record = self.record_cls(seqid, sequence, qid, qual)
            self._next = record
            return record
        else:
            self._next = None
            raise StopIteration

    def __next__(self):
        return self.next()

    def close(self):
        """ Close the reader """
        self.fobj.close()
