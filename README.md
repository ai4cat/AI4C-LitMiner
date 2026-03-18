# **LLM-Based Literature Mining for Atomically Dispersed Catalysts**

This repository provides an automated workflow for extracting structured scientific data from unstructured literature using large language models (LLMs). The primary focus is on catalyst systems, especially atomically dispersed catalysts (ADCs), including single-atom and dual-atom configurations.

The framework is designed to convert scientific publications (PDF/DOCX) into machine-readable datasets, enabling downstream data-driven catalyst discovery, descriptor analysis, and machine learning model development.

For further details, you are encouraged to consult our [paper](https://) and visit our [website](https://) for additional resources and also our [dataset](https://) information.

## **Installation**

### Development Environment
- Python 3.12
- Validated on Windows OS
- Use `conda env create -f litminer.yml` to create the enviornment.

### Setup
To set up the codes, run the following commands:

```bash
git clone https://github.com/ai4cat/AI4C-LitMiner.git
cd AI4C-LitMiner
```

## Data Availability & Copyright Notice

The dataset used in this project is NOT publicly distributed due to copyright and licensing restrictions. The input data consist of published scientific articles, which are typically:

Protected by publisher copyright

Accessible only through institutional subscriptions or paid access

As a result:

❌ We do not provide raw PDF/DOCX files

❌ We do not redistribute full-text literature

Users are required to:

Obtain the relevant publications through legal and authorized channels (e.g., institutional access, publisher purchase)

This repository only provides:

✅ Code for data extraction

✅ Prompt design and schema definitions

✅ Example structured outputs (non-copyrighted)

## **Repository Structure**

```text
AI4C-LitMiner/
├── code/
├──── sys_method_extract.py     # Extract the sysnthesis methods
├──── info_extract/             
├─────── config.py              # Configurations
├─────── main.py                # Task-specific text-mining workflows
├─────── processor.py           # Perform the task            
├─────── prompt.py              # Prompt templates for LLM-based extraction
├─────── utils.py               # Common utilities (PDF parsing, cleaning, logging)
└──── result/                 
```

## Contributing
Contributions are welcome! Please follow the standard fork-and-pull request workflow on GitHub.

If you use our code in your research, please cite our paper:
```bash
@article{,
  title={s},
  author={},
  journal={},
  year={},
  volume = {},
  pages = {}
}
```

## **License**

**MatDataMiner** is released under the **MIT License**.

For the full license text, please refer to the [MIT License](https://github.com/ai4cat/AI4C-LitMiner/blob/main/LICENSE) file.
