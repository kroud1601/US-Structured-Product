from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path

import pandas as pd
import yaml

from src.analysis import analyze_offerings
from src.common import PROJECT_ROOT, email_is_placeholder, ensure_directories, load_config
from src.pipeline import (
    build_filing_universe,
    build_offerings,
    build_research_sample,
    collect_and_classify,
    enrich_primary_documents,
)
from src.validation import create_validation_sample, summarize_validation


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Beginner-friendly SEC structured-products research pipeline"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="Check Python, configuration, and folders")
    metadata = subparsers.add_parser("metadata", help="Build the 424B2 filing universe")
    metadata.add_argument("--force", action="store_true", help="Redownload SEC index files")
    sample_plan = subparsers.add_parser(
        "sample-plan", help="Create the stratified probability sample used for the study"
    )
    sample_plan.add_argument("--force", action="store_true", help="Rebuild the saved sample")
    primary_map = subparsers.add_parser(
        "primary-map", help="Map sampled accessions to direct SEC primary documents"
    )
    primary_map.add_argument("--force", action="store_true", help="Redownload SEC submission JSON")

    collect = subparsers.add_parser("collect", help="Download, classify, and extract filings")
    _add_run_size_arguments(collect)

    subparsers.add_parser("build", help="Deduplicate filings into unique offerings")
    subparsers.add_parser("analyze", help="Create tables, charts, and a preliminary report")
    subparsers.add_parser("demo", help="Run the offline synthetic demonstration")
    validation = subparsers.add_parser(
        "validation-sample", help="Create a spreadsheet-ready manual review sample"
    )
    validation.add_argument("--size", type=int, default=100, help="Number of filings to review")
    subparsers.add_parser(
        "validation-report", help="Score the completed manual validation sheet"
    )

    all_parser = subparsers.add_parser("all", help="Run metadata, collect, build, and analyze")
    _add_run_size_arguments(all_parser)
    all_parser.add_argument("--force-metadata", action="store_true")

    arguments = parser.parse_args()
    ensure_directories()
    config = load_config()

    if arguments.command == "doctor":
        return doctor(config)
    if arguments.command == "demo":
        analyze_offerings(config, demo=True)
        print(f"Demo complete: {PROJECT_ROOT / 'demo_output' / 'DEMO_RESULTS.md'}")
        return 0

    if arguments.command == "validation-sample":
        sample = create_validation_sample(config, sample_size=arguments.size)
        print(
            f"Validation sample created ({len(sample):,} rows): "
            f"{PROJECT_ROOT / 'data' / 'validation' / 'validation_sample.csv'}"
        )
        return 0

    if arguments.command == "validation-report":
        metrics = summarize_validation()
        print(metrics.to_string(index=False))
        return 0

    if email_is_placeholder(config["sec"].get("email", "")):
        print("ERROR: Edit config/config.yaml and replace YOUR_EMAIL@example.com.")
        print("The SEC requires automated users to provide an identifying user agent.")
        return 2

    if arguments.command == "metadata":
        frame = build_filing_universe(config, force=arguments.force)
        print(f"Metadata complete: {len(frame):,} Form 424B2 filings")
    elif arguments.command == "sample-plan":
        frame = build_research_sample(config, force=arguments.force)
        print(f"Research sample complete: {len(frame):,} filings")
    elif arguments.command == "primary-map":
        frame = enrich_primary_documents(config, force=arguments.force)
        coverage = frame["primary_document_url"].notna().mean()
        print(f"Primary-document map complete: {coverage:.1%} coverage")
    elif arguments.command == "collect":
        frame = collect_and_classify(
            config,
            limit=arguments.limit,
            full=arguments.full,
            research_sample=arguments.research_sample,
        )
        print(f"Classification file contains {len(frame):,} processed filings")
    elif arguments.command == "build":
        frame = build_offerings(config)
        print(f"Offering master contains {len(frame):,} unique offerings")
    elif arguments.command == "analyze":
        analyze_offerings(config)
        print(f"Analysis complete: {PROJECT_ROOT / 'report' / 'FULL_REPORT.md'}")
    elif arguments.command == "all":
        build_filing_universe(config, force=arguments.force_metadata)
        if arguments.research_sample:
            enrich_primary_documents(config)
        collect_and_classify(
            config,
            limit=arguments.limit,
            full=arguments.full,
            research_sample=arguments.research_sample,
        )
        build_offerings(config)
        analyze_offerings(config)
        print(f"Pipeline complete: {PROJECT_ROOT / 'report' / 'FULL_REPORT.md'}")
    return 0


def _add_run_size_arguments(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--limit", type=int, help="Number of filings to select for this run")
    group.add_argument("--full", action="store_true", help="Process the full remaining universe")
    group.add_argument(
        "--research-sample",
        action="store_true",
        help="Process the saved issuer-year probability sample",
    )


def doctor(config: dict) -> int:
    print("Structured Products Project — Setup Check")
    print(f"Python: {platform.python_version()}")
    print(f"Pandas: {pd.__version__}")
    print(f"PyYAML: {yaml.__version__}")
    print(f"Project folder: {PROJECT_ROOT}")
    print(
        "Study period: "
        f"{config['project']['start_date']} through {config['project']['end_date']}"
    )
    email = config["sec"].get("email", "")
    if email_is_placeholder(email):
        print("SEC identity: NOT READY — replace the placeholder email in config/config.yaml")
        return 2
    print(f"SEC identity: READY ({email})")
    print("Setup check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
