#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Exome Validation: DRAGEN NovaSeq Validation 2026
# Batch benchmarking of exome samples against Platinum Genomes truth sets.
# ------------------------------------------------------------------

BASE_DIR="/mnt/ssd/data/benchmarking-dragen-hap"

# DRAGEN output directory
DRAGEN_DIR="/mnt/nas/peta-data/shared/dragen_output/3_Exome_Dragen_NovaSeq_Validation_2026/Exome_Validation_DRAGEN_1"

# Common paths
REFERENCE="${BASE_DIR}/hg38_reference/WholeGenomeFasta/genome.fa"
CONFIDENT_REGIONS="${BASE_DIR}/ConfidentRegions/ConfidentRegions.bed"
TARGET_REGIONS="${BASE_DIR}/ConfidentRegions/DRAGEN_Illumina_exome/hg38_Twist_Bioscience_for_Illumina_Exome_2_5_Mito.bed"
OUTPUT_DIR="${BASE_DIR}/exome_validation_dragen"

mkdir -p "${OUTPUT_DIR}"

# Sample ID -> Truth sample mapping
declare -A SAMPLES=(
    ["P22_000480"]="NA12878"
    ["P23_001471"]="NA12877"
)

for SAMPLE_ID in "${!SAMPLES[@]}"; do
    TRUTH="${SAMPLES[$SAMPLE_ID]}"

    TRUTH_VCF="${BASE_DIR}/PlatinumGenomesIllumina/vcf/${TRUTH}.vcf.gz"
    QUERY_VCF="${DRAGEN_DIR}/${SAMPLE_ID}/${SAMPLE_ID}.hard-filtered.vcf.gz"
    OUTPUT_PREFIX="${OUTPUT_DIR}/${SAMPLE_ID}_${TRUTH}"

    echo "=== ${SAMPLE_ID} [${TRUTH}] ==="

    happy \
        "${TRUTH_VCF}" \
        "${QUERY_VCF}" \
        -r "${REFERENCE}" \
        -f "${CONFIDENT_REGIONS}" \
        -T "${TARGET_REGIONS}" \
        -o "${OUTPUT_PREFIX}" \
        --engine vcfeval \
        --pass-only \
        --background

    echo ""
done

echo "All jobs submitted."