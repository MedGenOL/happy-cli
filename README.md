# happy-cli

A lightweight CLI wrapper for running
[hap.py](https://github.com/Illumina/hap.py) in Docker.
Built for lab teams that need to run benchmarking periodically when
sequencing technology or protocols change.

**hap.py** (Haplotype Comparison Tool) was created by
[Peter Krusche](https://github.com/pkrusche) at
[Illumina](https://www.illumina.com/).

## Prerequisites

- Python >= 3.9
- Docker installed and running
- The `pkrusche/hap.py` Docker image pulled (`docker pull pkrusche/hap.py`)

## Installation

```bash
git clone https://github.com/MedGenOL/happy-cli.git
cd happy-cli
pip install -e .
```

## Usage

```bash
happy \
  data/PlatinumGenomesIllumina/vcf/NA12877.vcf.gz \
  /path/to/your_pipeline_output.vcf.gz \
  -r /path/to/hg38/genome.fa \
  -f data/ConfidentRegions/ConfidentRegions.bed \
  -o /path/to/output/NA12877_vs_pipeline
```

All paths are **normal host paths** — the tool handles Docker volume
mounting automatically. Use `--dry-run` to preview the Docker command
without executing it.

Run `happy --help` for all options.

## Data

The `data/` directory includes curated Platinum Genomes truth sets and
high-confidence regions. Large files are gitignored and must be
downloaded — see [`data/README.md`](data/README.md) for instructions.

## Output

hap.py produces the following files (using the output prefix as base name):

| File                               | Contents                                |
| ---------------------------------- | --------------------------------------- |
| `.summary.csv`                     | Precision, recall, and F1 score         |
| `.extended.csv`                    | Extended statistics                     |
| `.metrics.json.gz`                 | Detailed metrics                        |
| `.runinfo.json`                    | Run metadata and parameters             |
| `.vcf.gz` / `.vcf.gz.tbi`         | Annotated comparison VCF with index     |
| `.roc.all.csv.gz`                  | ROC data for all variants               |
| `.roc.Locations.INDEL.csv.gz`      | ROC data for INDELs                     |
| `.roc.Locations.INDEL.PASS.csv.gz` | ROC data for INDELs (PASS only)         |
| `.roc.Locations.SNP.csv.gz`        | ROC data for SNPs                       |
| `.roc.Locations.SNP.PASS.csv.gz`   | ROC data for SNPs (PASS only)           |

## Documentation

See [`docs/Guide_to_run_benchmarking.md`](docs/Guide_to_run_benchmarking.md)
for a step-by-step walkthrough.
