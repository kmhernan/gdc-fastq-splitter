"""Module containing classes for parsing fastq files that adhere to illumina formats"""
import gzip
import inspect
import sys

import gdc_fastq_splitter.fastq.base as base


class IlluminaSequenceIdentifier(base.SequenceIdentifier):
    """Standard Illumina sequence identifier format for modern Casava versions.
    These are of the format:

    @NS500106:131:HTM2GBGXX:1:11101:18568:1043 2:N:0:TAAGGCGA+ATAGAGAG
    """

    @classmethod
    def from_string(cls, seqid):
        _keys = [
            "instrument_name",
            "run",
            "flowcell",
            "lane",
            "tile",
            "x_coord",
            "y_coord",
            "read_pair",
            "pf",
            "bits",
            "index",
        ]

        parts = seqid[1:].split(" ")
        assert len(parts) == 2, "{0}".format(parts)

        parts_a = parts[0].split(":")
        assert len(parts_a) == 7

        parts_b = parts[1].split(":")
        assert len(parts_b) == 4

        data = {k: (v if v else None) for k, v in zip(_keys, parts_a + parts_b)}
        data["seqid"] = seqid
        data["lane"] = int(data["lane"])
        assert data["lane"] < 9
        return cls(**data)

    @staticmethod
    def is_valid(seqid):
        if seqid.count(":") != 9:
            return False
        elif seqid.count(" ") != 1:
            return False
        return True


class IlluminaSequenceIdentifierNoBarcode(base.SequenceIdentifier):
    """Illumina fastq file with the following format:

    @D00761:79:C9E9CANXX:7:1208:2524:17753/1
    """

    @classmethod
    def from_string(cls, seqid):
        _keys = [
            "instrument_name",
            "run",
            "flowcell",
            "lane",
            "tile",
            "x_coord",
            "y_coord",
            "read_pair",
        ]

        parts = seqid[1:].split("/")
        assert len(parts) == 2, "{0}".format(parts)

        parts_a = parts[0].split(":")
        assert len(parts_a) == 7

        parts_b = parts[1]
        assert parts_b in ("1", "2")

        data = {k: (v if v else None) for k, v in zip(_keys, parts_a + [parts_b])}
        data["seqid"] = seqid
        data["lane"] = int(data["lane"])
        assert data["lane"] < 9
        return cls(**data)

    @staticmethod
    def is_valid(seqid):
        if seqid.count(":") != 6:
            return False
        elif seqid.count(" ") != 0:
            return False
        elif seqid.count("/") != 1:
            return False
        return True


class IlluminaFastqRecord(base.FastqRecord):
    seqid_cls = IlluminaSequenceIdentifier

    def __init__(self, seqid, sequence, qid, qual):
        super().__init__(seqid, sequence, qid, qual)

    @property
    def read_key(self):
        return "{0.seqid.flowcell}_{0.seqid.lane}".format(self)

    @property
    def index(self):
        return self.seqid.index

    @property
    def read_pair(self):
        return self.seqid.read_pair

    @property
    def flowcell(self):
        return self.seqid.flowcell

    @property
    def lane(self):
        return self.seqid.lane

    @classmethod
    def is_valid_seqid(cls, seqid):
        return cls.seqid_cls.is_valid(seqid)


class IlluminaNoBarcodeFastqRecord(base.FastqRecord):
    seqid_cls = IlluminaSequenceIdentifierNoBarcode

    def __init__(self, seqid, sequence, qid, qual):
        super().__init__(seqid, sequence, qid, qual)

    @property
    def read_key(self):
        return "{0.seqid.flowcell}_{0.seqid.lane}".format(self)

    @property
    def read_pair(self):
        return self.seqid.read_pair

    @property
    def flowcell(self):
        return self.seqid.flowcell

    @property
    def lane(self):
        return self.seqid.lane

    @classmethod
    def is_valid_seqid(cls, seqid):
        return cls.seqid_cls.is_valid(seqid)


def infer_fastq_type(fil):
    """
    Infer the type of fastq based on the first line.
    """

    def predicate(obj):
        """A predicate to get all classes that are subclasses of
        base.FastqRecord"""
        return (
            inspect.isclass(obj)
            and issubclass(obj, base.FastqRecord)
            and hasattr(obj, "is_valid_seqid")
        )

    fh = gzip.open(fil, "rt") if fil.endswith(".gz") else open(fil, "rt")

    cls_mod = None

    try:
        line = fh.readline().rstrip("\r\n")
        # mod = sys.modules["gdc_fastq_splitter.fastq.illumina"]
        mod = sys.modules["gdc_fastq_splitter.fastq.illumina"]
        # Get all available seqidentifier types
        for m in inspect.getmembers(mod, predicate):
            if m[1].is_valid_seqid(line):
                cls_mod = m
                break
    finally:
        fh.close()
    if not cls_mod:
        raise Exception("Unable to determine the type of fastq")
    return cls_mod
