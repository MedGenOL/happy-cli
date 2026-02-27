# ConfidentRegions for Benchmarking (Platinum Genomes, hg38)

This folder contains the **ConfidentRegions.bed** file used for benchmarking variant calls against the Platinum Genomes truth set on the **hg38/GRCh38** reference genome.

## 📄 File Details

- **Filename**: `ConfidentRegions.bed` (originally `ConfidentRegions.bed.gz`)
- **Source**: Platinum Genomes Project (Illumina)
- **Version**: 2017-1.0 release
- **Reference genome**: GRCh38 (hg38)
- **Download origin**:  
  - **AWS S3**: `s3://platinum-genomes/2017-1.0/hg38/small_variants/ConfidentRegions.bed.gz`  
  - **Illumina FTP**: `ftp://platgene_ro@ussd-ftp.illumina.com/2017-1.0/hg38/small_variants/ConfidentRegions.bed.gz`

## 🧬 Purpose

This BED file defines the **high-confidence genomic intervals** used when benchmarking variant callsets. It ensures:

- Comparisons are limited to regions with validated, high-quality sequence and variant data.
- Exclusion of problematic regions (e.g., low-complexity, segmental duplications, unresolved genome areas).
- Accurate metrics (precision, recall, F1) from tools like `hap.py`.

## ✅ Usage Example (hap.py)

```bash
bash hap-docker.sh \
  truth.vcf.gz \
  query.vcf.gz \
  -r genome.fa \
  -f ConfidentRegions/ConfidentRegions.bed \
  -o output_prefix
