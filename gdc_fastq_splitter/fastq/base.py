"""A module containing the base classes for Fastq records"""
from abc import ABCMeta, abstractmethod


class SequenceIdentifier(metaclass=ABCMeta):
    """Class for parsing the sequence identifier line from a fastq record"""

    def __init__(self, **kwargs):
        """
        Constructor.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    @abstractmethod
    def from_string(cls, seqid):
        return cls(seqid=seqid)

    def __str__(self):
        return self.seqid


class FastqRecord:
    """The base class for a Fastq record"""

    seqid_cls = SequenceIdentifier

    def __init__(self, seqid, sequence, qid, qual):
        self.seqid = self.seqid_cls.from_string(seqid)
        self.sequence = sequence
        self.qid = qid
        self.qual = qual

    def __str__(self):
        return "{0.seqid}\n{0.sequence}\n{0.qid}\n{0.qual}\n".format(self)

    def __bytes__(self):
        return bytes(self.__str__().encode("utf-8"))
