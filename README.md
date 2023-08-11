# llm-batch-processing
An exploration of how a Large Language Model (LLM) can be used for batch data processing in a Canadian federal context.

Note: this code is intended as a starting point for developers wanting to explore the application space. The code is intended to be read as a learning experience.

Key considerations before deploying this to anything resembling real users:
* The memory and CPU requirements for this are not tiny: You need at least 16GB of memory and 4 relatively quick real CPU cores (not hyper-thread cores) to run this realistically.
* While this will technically run on processors without AVX2 extensions, it's really not recommended.

# Quickstart:
## Installation
```
wget https://huggingface.co/TheBloke/airoboros-l2-7B-gpt4-m2.0-GGML/resolve/main/airoboros-l2-7b-gpt4-m2.0.ggmlv3.q4_0.bin
pip install -r requirements.txt
```
## Execution
```
python app.py
```
...and then go get a coffee. This execution takes *quite* a while.

# Getting started with LLM learning
Open `app.py` in your favourite editor, and follow along if you want to learn about interacting with LLMs.

# Notes about data
The data in this repo is a tiny slice of the open part of the CSPS' course catalogue used for illustration purposes only. The real catalogue is much larger, and changes with time; this repository is not kept in sync with the live source.
