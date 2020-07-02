import unittest
import os
import logging

from gdc_fastq_splitter.fastq.illumina import (
    IlluminaFastqRecord,
    IlluminaSequenceIdentifierNoBarcode,
    IlluminaSequenceIdentifier,
    IlluminaNoBarcodeFastqRecord,
    infer_fastq_type,
)


class TestIlluminaSequenceIdentifier(unittest.TestCase):
    """Test modern illumina sequence identifiers"""

    def test_parse_record(self):
        """Parse modern illumina identifier"""
        seqid = "@NS500106:131:HTM2GBGXX:1:11101:18568:1043 2:N:0:TAAGGCGA+ATAGAGAG"
        sobj = IlluminaSequenceIdentifier.from_string(seqid)
        self.assertTrue(sobj.seqid == seqid)
        self.assertTrue(sobj.instrument_name == "NS500106")
        self.assertTrue(sobj.run == "131")
        self.assertTrue(sobj.flowcell == "HTM2GBGXX")
        self.assertTrue(sobj.lane == 1)
        self.assertTrue(sobj.read_pair == "2")
        self.assertTrue(sobj.index == "TAAGGCGA+ATAGAGAG")

    def test_validate_record(self):
        """Test the is_valid staticmethod"""
        seqid = "@NS500106:131:HTM2GBGXX:1:11101:18568:1043 2:N:0:TAAGGCGA+ATAGAGAG"
        self.assertTrue(IlluminaSequenceIdentifier.is_valid(seqid))
        self.assertFalse(IlluminaSequenceIdentifierNoBarcode.is_valid(seqid))


class TestIlluminaSequenceIdentifierNoBarcode(unittest.TestCase):
    """Test sequence identifiers for illumina reads with no barcode section"""

    def test_parse_record(self):
        """Parse no barcode illumina identifier"""
        seqid = "@D00761:79:C9E9CANXX:7:1208:2524:17753/1"
        sobj = IlluminaSequenceIdentifierNoBarcode.from_string(seqid)
        self.assertTrue(sobj.seqid == seqid)
        self.assertTrue(sobj.instrument_name == "D00761")
        self.assertTrue(sobj.run == "79")
        self.assertTrue(sobj.flowcell == "C9E9CANXX")
        self.assertTrue(sobj.lane == 7)
        self.assertTrue(sobj.read_pair == "1")

    def test_validate_record(self):
        """Test the is_valid staticmethod"""
        seqid = "@D00761:79:C9E9CANXX:7:1208:2524:17753/1"
        self.assertFalse(IlluminaSequenceIdentifier.is_valid(seqid))
        self.assertTrue(IlluminaSequenceIdentifierNoBarcode.is_valid(seqid))


class TestIlluminaFastqRecord(unittest.TestCase):
    """Test the creation of fastq records"""

    def test_valid_record(self):
        lines = [
            "@NS500106:131:HTM2GBGXX:1:11101:18568:1043 2:N:0:TAAGGCGA+ATAGAGAG",
            "CCAATT",
            "+",
            "##<<AA",
        ]

        sobj = IlluminaFastqRecord(*lines)
        self.assertTrue(sobj.seqid.instrument_name == "NS500106")


class TestInferFastqType(unittest.TestCase):
    """Test the infer_fastq_type functionality"""

    def test_modern(self):
        """Testing IlluminaFastqRecord"""
        fil = os.path.join(
            os.path.dirname(__file__), "etc/fake_IlluminaSequenceIdentifier.fastq"
        )
        m = infer_fastq_type(fil)
        expected = ("IlluminaFastqRecord", IlluminaFastqRecord)
        self.assertEqual(expected, m)

    def test_nobarcode(self):
        """Testing IlluminaNoBarcodeFastqRecord"""
        fil = os.path.join(
            os.path.dirname(__file__),
            "etc/fake_IlluminaSequenceIdentifierNoBarcode.fastq",
        )
        m = infer_fastq_type(fil)
        expected = ("IlluminaNoBarcodeFastqRecord", IlluminaNoBarcodeFastqRecord)
        self.assertEqual(expected, m)

    def test_unknown(self):
        """Testing raise exception"""
        fil = os.path.join(os.path.dirname(__file__), "etc/fake_Unknown.fastq")

        with self.assertRaises(Exception):
            m = infer_fastq_type(fil)


if __name__ == "__main__":
    unittest.main()
