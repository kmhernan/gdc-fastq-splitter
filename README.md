# gdc-fastq-splitter

CLI for splitting a fastq that has multiple readgroups. We currently only support non-interleaved
fastq files with the following seqid formats:

`@<machine>:<run>:<flowcell>:<lane>:<tile>:<x_coord>:<y_coord> <read_mate_number>:<vendor_filtered>:<bits>:<barcode>`

`@<machine>:<run>:<flowcell>:<lane>:<tile>:<x_coord>:<y_coord>/<read_mate_number>`

**Note: Your fastq must contain one of these formats but not a mixture of both**

## Docker

There is a publicly accessible repo on Quay [https://quay.io/repository/kmhernan/gdc-fastq-splitter](https://quay.io/repository/kmhernan/gdc-fastq-splitter):

```
# Can pull particular tags if needed
docker pull quay.io/kmhernan/gdc-fastq-splitter

# Run image
docker run --rm quay.io/kmhernan/gdc-fastq-splitter
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

## Install

The only dependencies are python>=3.5 as only standard python libraries are used. However, your build of python3 
does need to have been compiled with the zlib binding, which are including in standard python installations.

1. Clone: `git clone https://github.com/kmhernan/gdc-fastq-splitter.git`
2. Change directories: `cd gdc-fastq-splitter`
3. Create virtualenv (the path to your python3 executable may be different; your path to your virtual environment may be different): `virtualenv venv --python /usr/bin/python3.5`
4. Install (the path to your virtual environment may be different): `./venv/bin/pip install .`

## Usage

The CLI will be installed as `venv/bin/gdc-fastq-splitter`. The output of the help (`-h`) comand:

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

### Inputs

The input fastq can either be ASCII text or gzip (must end with `.gz`) compressed, no other compression formats are
accepted.

### Outputs

The output prefix will be used for the output files created which will be of the form 
`<prefix><flowcell>_<lane>_R<1/2>.fq.gz` so you probably will want to include either a
`.` or a `_` in your `--output-prefix` option. (The outputs will always be gzip compressed).

__For example, this single-end fastq command:__

```
gdc-fastq-splitter --output-prefix output_fastq_ input_fastq.fq.gz
```

will create output files for each detected readgroup with this structure in the current working directory:

```
output_fastq_<flowcell>_<lane>_R1.fq.gz
```

__While, this single-end fastq command:__

```
gdc-fastq-splitter --output-prefix output_fastq input_fastq.fq.gz
```

will create output files for each detected readgroup with this structure in the current working directory:

```
output_fastq<flowcell>_<lane>_R1.fq.gz
```

Thus, you should include whatever character (usually `.` or `_`) that you prefer to separate your prefix from the 
information added by the CLI.

**Note: R1 and R2 are inferred from the sequence ID rows and automatically added to the output files**

## Report JSON

A report JSON file will be created for each mate and readgroup detected by the software. For fastq files with sequence
identifiers that do not have the multiplex barcode index in them, the report JSON created will have the following
format:

```
{
  "metadata": {
    "fastq_filename": <output fastq filename referenced by this report>,
    "flowcell_barcode": <flowcell barcode for this readgroup>,
    "lane_number": <lane number for this readgroup>,
    "record_count": <number of records output into this readgroup fastq file>
  }
}
```

If there are multiplex barcodes, an additional section will contain the frequency of all barcodes seen for the
readgroup and an additional key in the `metadata` object will have the most frequent `multiplex_barcode`.

## Limitations

* This will only work as expected for fastqs that have sequence identifiers described above
* We do *not* support interleaved fastq files, and no checks are done to ensure this
* We do *not* support fastq files with a mixture of sequence identifier formats
