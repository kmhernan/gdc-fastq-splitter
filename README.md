# gdc-fastq-splitter

CLI for splitting a fastq that has multiple readgroups. We currently only support non-interleaved
fastq files with the following seqid formats:

`@<machine>:<run>:<flowcell>:<lane>:<tile><x_coord>:<y_coord> <read_mate_number>:<vendor_filtered>:<bits>:<barcode>`

`@<machine>:<run>:<flowcell>:<lane>:<tile>:<x_coord>:<y_coord>/<read_mate_number>`

## Install

The only dependencies are python>=3.5 as only standard python libraries are used. However, your build of python3 
does need to have been compiled with the zlib binding, which are including in standard python installations.

1. Clone: `git clone git@github.com:kmhernan/gdc-fastq-splitter.git`
2. Change directories: `cd gdc-fastq-splitter`
3. Checkout develop branch: `git checkout develop`
4. Create virtualenv (the path to your python3 executable may be different; your path to your virtual environment may be different): `virtualenv venv --python /usr/bin/python3.5`
5. Install (the path to your virtual environment may be differen): `./venv/bin/pip install .`

If you want to run unittest tests before your install: `./venv/bin/python -m unittest -v`

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

The output prefix will be used for the output files created which will be of the form 
`<prefix><flowcell>_<lane>_R<1/2>.fq.gz` so you probably will want to include either a
`.` or a `_` in your `--output-prefix` option.

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
for e
