# Prometheus Result

This repository contains the results of running **Prometheus Automatic Program Repair Agent** using multiple large language models (including GPT-4o and others) for automatic program repair.

## Features

* **Automatic bug repair** for multiple programming languages
* **Multi-model patch generation** for higher robustness
* **High-quality repair suggestions** leveraging state-of-the-art LLMs

## Usage

1. Clone this repository.
2. **Log format requirement**:
   When uploading, ensure that log files follow the naming format:

   ```
   instance_id.log
   ```

   For example:

   ```
   astropy__astropy-12907.log
   django__django-10914.log
   ```
3. If your logs are not in this format, you can use the provided `reformat.py` script to automatically rename them.

## Requirements

* Python 3.11+
* [Prometheus](https://github.com/Pantheon-temple/Prometheus)
* Access to supported large language models (e.g., OpenAI GPT-4o, Claude, DeepSeek, etc.)

## Acknowledgements

* [Prometheus](https://github.com/Pantheon-temple/Prometheus)
* OpenAI, Anthropic, DeepSeek, and other model providers
