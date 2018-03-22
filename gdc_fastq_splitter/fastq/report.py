"""Module containing classes for generating reports from Fastq files"""
import os
import json
from collections import Counter


class BaseReport:
    """Base report for a fastq file"""
    def __init__(self, filename, flowcell_barcode=None, lane_number=None):
        self._filename = filename
        self.filename = os.path.basename(filename)
        self.flowcell_barcode = flowcell_barcode
        self.lane_number = lane_number
        self.record_counts = 0

    def __iadd__(self, record):
        self.record_counts += 1
        return self

    def __str__(self):
        return '<flowcell>({0.flowcell_barcode}),<lane>({0.lane_number})'.format(self)

    def to_dict(self):
        return {
            'metadata': {
                'filename': self.filename,
                'flowcell_barcode': self.flowcell_barcode,
                'lane_number': self.lane_number,
                'record_count': self.record_counts
            }
        }

    def write_to_json(self):
        with open(self._filename, 'wt') as o:
            json.dump(self.to_dict(), o, indent=2, sort_keys=True)


class BarcodeFastqReport(BaseReport):
    """Report that contains barcode frequencies."""
    def __init__(self, filename, flowcell_barcode=None, lane_number=None):
        super().__init__(filename, flowcell_barcode=flowcell_barcode, lane_number=lane_number)
        self.barcode_frequency = Counter()

    @property
    def most_common_barcode(self):
        try:
            bc = self.barcode_frequency.most_common(1)[0][0]
            return bc.replace('-', '+')
        except IndexError:
            return None

    def _add_barcode(self, barcode):
        self.barcode_frequency[barcode] += 1

    def __iadd__(self, record):
        self.record_counts += 1
        self._add_barcode(record.index)
        return self

    def __str__(self):
        return '<flowcell>({0.flowcell_barcode}),<barcode>({0.multiplex_barcode}),<lane>({0.lane_number})'.format(self)

    def to_dict(self):
        return {
            'metadata': {
                'filename': self.filename,
                'flowcell_barcode': self.flowcell_barcode,
                'multiplex_barcode': self.most_common_barcode,
                'lane_number': self.lane_number,
                'record_count': self.record_counts
            },
            'barcode_frequency': dict(self.barcode_frequency)
        }
