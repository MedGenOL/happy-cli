"""CLI entry point for happy-cli, a Docker wrapper around hap.py."""

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import click

PETA_SHARED_DEFAULT = "/mnt/nas/peta-shared"


def _resolve_and_validate(path_str, label):
    """Resolve a path to absolute and validate it exists."""
    p = Path(path_str).resolve()
    if not p.exists():
        click.echo(f"Error: {label} not found: {p}", err=True)
        sys.exit(1)
    return p


def _is_subpath(path, parent):
    """Check if path is equal to or under parent."""
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _build_docker_volumes(file_paths, output_path, shared_mount):
    """Compute Docker volume mounts and translate host paths to container paths.

    Returns (volume_args, path_map) where volume_args is a flat list of
    ["-v", "host:container", ...] and path_map maps each Path to its
    container path string.
    """
    mounts = []  # list of (host_dir: Path, container_dir: str)

    # Always include the shared mount if available on the host
    shared = Path(shared_mount)
    if shared.is_dir():
        mounts.append((shared, "/peta-shared"))

    # Collect all directories that need mounting
    all_paths = list(file_paths)
    if output_path:
        all_paths.append(output_path)

    extra_dirs = set()
    for p in all_paths:
        parent = p.parent
        if not any(_is_subpath(parent, host_dir) for host_dir, _ in mounts):
            extra_dirs.add(parent)

    # Deduplicate: remove dirs that are subdirs of another dir in the set
    sorted_dirs = sorted(extra_dirs, key=lambda d: len(d.parts))
    deduped = []
    for d in sorted_dirs:
        if not any(_is_subpath(d, existing) for existing in deduped):
            deduped.append(d)

    for i, d in enumerate(deduped):
        mounts.append((d, f"/mnt/happy_{i}"))

    # Build -v arguments
    volume_args = []
    for host_dir, container_dir in mounts:
        volume_args.extend(["-v", f"{host_dir}:{container_dir}"])

    # Translate each path to its container equivalent
    path_map = {}
    for p in all_paths:
        for host_dir, container_dir in mounts:
            if _is_subpath(p, host_dir):
                rel = p.relative_to(host_dir)
                path_map[p] = f"{container_dir}/{rel}"
                break

    return volume_args, path_map


@click.command(
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
)
@click.argument("truth_vcf")
@click.argument("query_vcf")
@click.option(
    "-r", "--reference",
    required=True,
    help="Reference FASTA file.",
)
@click.option(
    "-f", "--regions",
    default=None,
    help="High-confidence regions BED file.",
)
@click.option(
    "-o", "--output-prefix",
    default=None,
    help="Output prefix for result files.",
)
@click.option(
    "--shared-mount",
    default=PETA_SHARED_DEFAULT,
    show_default=True,
    help="Host directory to mount as /peta-shared.",
)
@click.option(
    "--docker-image",
    default="pkrusche/hap.py",
    show_default=True,
    help="Docker image to use.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Print the Docker command without running it.",
)
@click.option(
    "-bg", "--background",
    is_flag=True,
    help="Run in background and log output to happy_YYYYMMDD_HHMMSS.log.",
)
@click.pass_context
def main(ctx, truth_vcf, query_vcf, reference, regions, output_prefix,
         shared_mount, docker_image, dry_run, background):
    """Compare variant calls against a truth set using hap.py in Docker.

    TRUTH_VCF is the truth variant call file.
    QUERY_VCF is the variant call file to evaluate.

    All file paths should be normal host paths. The tool automatically sets up
    Docker volume mounts and translates paths for the container.

    Any extra arguments are passed through to hap.py.
    """
    if not shutil.which("docker"):
        click.echo("Error: Docker is not installed or not in PATH.", err=True)
        sys.exit(1)

    # Resolve and validate input files
    truth = _resolve_and_validate(truth_vcf, "Truth VCF")
    query = _resolve_and_validate(query_vcf, "Query VCF")
    ref = _resolve_and_validate(reference, "Reference FASTA")

    file_paths = [truth, query, ref]

    regions_path = None
    if regions:
        regions_path = _resolve_and_validate(regions, "Regions BED")
        file_paths.append(regions_path)

    output_path = None
    if output_prefix:
        output_path = Path(output_prefix).resolve()
        if not output_path.parent.is_dir():
            click.echo(
                f"Error: Output directory does not exist: {output_path.parent}",
                err=True,
            )
            sys.exit(1)

    # Build Docker volume mounts and translate paths
    volume_args, path_map = _build_docker_volumes(
        file_paths, output_path, shared_mount,
    )

    cmd = [
        "docker", "run", "--rm",
        *volume_args,
        docker_image,
        "/opt/hap.py/bin/hap.py",
        path_map[truth],
        path_map[query],
        "-r", path_map[ref],
    ]

    if regions_path:
        cmd.extend(["-f", path_map[regions_path]])

    if output_path:
        cmd.extend(["-o", path_map[output_path]])

    # Pass through any extra arguments to hap.py
    cmd.extend(ctx.args)

    click.echo(" ".join(cmd))

    if dry_run:
        return

    if background:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = Path.cwd() / f"happy_{timestamp}.log"
        with open(log_file, "w") as log:
            subprocess.Popen(
                cmd, stdout=log, stderr=log,
                start_new_session=True,
            )
        click.echo(f"Running in background. Log: {log_file}")
        return

    result = subprocess.run(cmd)
    sys.exit(result.returncode)
