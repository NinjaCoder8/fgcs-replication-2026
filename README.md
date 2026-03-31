# FGCS Replication Package

This repository contains the materials required to reproduce the results presented in the paper:

**"A Reference Architecture for an Orchestrated Collaborative MLOps: A Ground-Up Design from the Literature Combining Human and LLM Expertise"**

## Overview
The package includes:
- LLM analysis scripts and configurations
- Prompts and outputs for all runs
- Evaluation and comparison results
- Supporting artifacts for reproducibility

## Structure
```
/scripts         # LLM execution and processing scripts
/prompts         # Prompts used for all configurations
/results         # Raw and processed outputs
/evaluation      # Metrics and comparison tables
```

## Requirements
- Python 3.10+
- Required libraries listed in `requirements.txt`
- Access to LLM APIs (OpenAI, Anthropic, Google, etc.)

## Notes
- Each configuration is executed multiple times to assess stability.
- Outputs are stored per model and per run.
- Evaluation metrics include coverage, invalid items, duplicates, and structural consistency.

## Reproducibility
All prompts, configurations, and outputs are provided to ensure full traceability and reproducibility of the study.

## Contact
For questions or issues, please contact the authors.
