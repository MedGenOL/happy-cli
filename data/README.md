# Genomic Reference Data

This directory contains curated datasets for benchmarking variant calls. Large files (VCFs, BED) are gitignored and must be downloaded separately.

## Platinum Genomes Truth Set VCFs

High-confidence variant calls for NA12877 and NA12878 (hg38/GRCh38).

**Download from AWS S3:**

```bash
aws s3 cp --no-sign-request \
  s3://platinum-genomes/2017-1.0/hg38/small_variants/NA12877/ \
  data/PlatinumGenomesIllumina/vcf/ --recursive
```

**Download from Illumina FTP:**

```bash
wget -P data/PlatinumGenomesIllumina/vcf/ \
  ftp://platgene_ro@ussd-ftp.illumina.com/2017-1.0/hg38/small_variants/NA12877/NA12877.vcf.gz \
  ftp://platgene_ro@ussd-ftp.illumina.com/2017-1.0/hg38/small_variants/NA12877/NA12877.vcf.gz.tbi \
  ftp://platgene_ro@ussd-ftp.illumina.com/2017-1.0/hg38/small_variants/NA12878/NA12878.vcf.gz \
  ftp://platgene_ro@ussd-ftp.illumina.com/2017-1.0/hg38/small_variants/NA12878/NA12878.vcf.gz.tbi
```

See [`PlatinumGenomesIllumina/README.md`](PlatinumGenomesIllumina/README.md) for full details.

## Confident Regions BED

High-confidence genomic intervals for restricting benchmarking comparisons (Platinum Genomes 2017-1.0, hg38).

**Download from AWS S3:**

```bash
aws s3 cp --no-sign-request \
  s3://platinum-genomes/2017-1.0/hg38/small_variants/ConfidentRegions.bed.gz \
  data/ConfidentRegions/
gunzip data/ConfidentRegions/ConfidentRegions.bed.gz
```

See [`ConfidentRegions/README.md`](ConfidentRegions/README.md) for full details.

## Reference Genome

You also need an hg38 reference FASTA with `.fai` and `.dict` index files. This is not included in this repository. Common sources:

- [UCSC hg38](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/)
