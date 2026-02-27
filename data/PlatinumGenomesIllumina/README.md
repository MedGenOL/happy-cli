# Original link: https://emea.illumina.com/platinumgenomes.html

# Platinum Genomes Truth Set – High-Confidence VCF Files

This folder contains high-confidence variant call sets (VCFs) from the **Platinum Genomes Project**, based on whole-genome sequencing of the **CEPH pedigree 1463**, generated using **Illumina HiSeq® 2000 systems**.

## 📚 Project Overview

Whole-genome sequencing of this 17-member family was performed at high depth to enable accurate characterization of human genomic variation. Data from this project has supported the creation of widely used benchmark VCFs.

## 👥 Samples Included

- **17 individuals** from CEPH pedigree 1463 were sequenced at ~50× depth:
  - `NA12877`, `NA12878`, `NA12879`, `NA12880`, `NA12881`, `NA12882`, `NA12883`, `NA12884`, `NA12885`, `NA12886`, `NA12887`, `NA12888`, `NA12889`, `NA12890`, `NA12891`, `NA12892`, `NA12893`
  - dbGaP accession: [`phs001224`](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs001224)

- Additional high-depth sequencing:
  - `NA12877` and `NA12878` sequenced to **200× depth** (ENA: [PRJEB3246](https://www.ebi.ac.uk/ena/browser/view/PRJEB3246))

## 🧬 Truth Set Details

This folder includes high-confidence **variant call files (VCFs)** for individuals `NA12877` and `NA12878`. These truth sets were generated using:

- Inheritance-aware filtering across the 17-member pedigree
- Concordance across multiple variant calling methods

These files are suitable for **benchmarking variant calling pipelines**.

## 📥 Download Sources

If you are looking for additional files or reference data, the truth set VCFs are also available from:

- [Platinum Genomes GitHub](https://github.com/Illumina/PlatinumGenomes)
- Illumina's FTP: `ftp://ussd-ftp.illumina.com`  
  - Username: `platgene_ro`  
  - Password: *(leave empty)*
- [BaseSpace Sequence Hub](https://basespace.illumina.com/)

## 📝 Citation

If you use these truth sets in your work, please cite:

> Eberle MA, et al. (2017).  
> *A reference data set of 5.4 million phased human variants validated by genetic inheritance from sequencing a three-generation 17-member pedigree.*  
> Genome Research 27:157–164.  
> DOI: [10.1101/gr.210500.116](https://doi.org/10.1101/gr.210500.116)

## 💬 Contact

Questions or feedback?

- Email: [platinumgenomes@illumina.com](mailto:platinumgenomes@illumina.com)
- GitHub: [Open an issue](https://github.com/Illumina/PlatinumGenomes/issues)

> ⚠️ **Note:** Platinum Genomes data is freely available, but **technical support is not provided by Illumina**.

---
