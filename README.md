# gdc-fastq-splitter

CLI for splitting a fastq that has multiple readgroups. We currently only support non-interleaved
fastq files with the following seqid formats:

`@<machine>:<run>:<flowcell>:<lane>:<tile><x_coord>:<y_coord> <read_mate_number>:<vendor_filtered>:<bits>:<barcode>`

`@<machine>:<run>:<flowcell>:<lane>:<tile>:<x_coord>:<y_coord>/<read_mate_number>`

## Install

You must use python 3.5 or greater

`pip install .`

## Usage

```
gdc-fastq-splitter -h
usage: gdc-fastq-splitter [-h] [--version] -o OUTPUT_PREFIX fastq_a [fastq_b]

positional arguments:
  fastq_a               Fastq file to process
  fastq_b               If paired, the mate fastq file to process

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -o OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX
                        The output prefix to use for output files.
```

The output prefix will be used for the output files created which will be of the form 
`<prefix><flowcell>_<lane>_R<1/2>.fq.gz`

