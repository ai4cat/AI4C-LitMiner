# **MatDataMiner**

**MatDataMiner** is a modular and extensible repository designed for **text mining and information extraction in materials science**.  
The repository hosts a collection of text-mining codes tailored to different materials-science topics, with the goal of systematically transforming unstructured scientific literature into structured, machine-readable data.

## **Overview**

Modern materials research generates an enormous volume of textual data in the form of scientific papers, reports, and supplementary information. However, much of this knowledge remains locked in unstructured formats, limiting its direct use in data-driven modeling and machine-learning workflows.

**MatDataMiner** aims to address this challenge by providing a unified framework for **materials-oriented literature mining**, enabling automated extraction of key information such as material compositions, synthesis conditions, structures, properties, and performance metrics from published papers.

## **Key Features**

- **Topic-oriented text-mining pipelines**  
  Each submodule is designed for a specific materials-science task (e.g., catalysis, energy materials, functional oxides), allowing flexible extension to new research domains.

- **PDF-based literature corpus**  
  The repository supports curated paper libraries in **PDF format**, serving as the primary data source for large-scale literature analysis.

- **Large Language Model (LLM)–assisted extraction**  
  Text mining is powered by existing large language models, with a current focus on **Google Gemini**, to enable semantic-level understanding beyond traditional rule-based or keyword-based methods.

- **Prompt-engineering-driven workflows**  
  Carefully designed **prompt-engineering strategies** are used to guide LLMs in performing structured information extraction, entity recognition, and relation parsing tailored to materials-science contexts.

## **Design Philosophy**

Rather than training domain-specific models from scratch, **MatDataMiner** emphasizes the effective utilization of **state-of-the-art general LLMs** through domain-aware prompts and task-specific pipelines. This approach enables rapid adaptation to emerging research topics while maintaining high interpretability and reproducibility.


## **Intended Applications**

- Construction of **materials databases** for data-driven discovery  
- Automated curation of literature for **machine-learning and AI models**  
- Large-scale meta-analysis of published experimental and computational results  
- Integration with downstream workflows such as catalyst screening and materials informatics


## **Repository Structure**

( to be modified... not comfirmed...)
```text
MatDataMiner/
├── ORR/               # PDF literature collections
├── prompts/           # Prompt templates for LLM-based extraction
├── pipelines/         # Task-specific text-mining workflows
├── utils/             # Common utilities (PDF parsing, cleaning, logging)
└── examples/          # Demonstration scripts and notebooks
```

## **License**

**MatDataMiner** is released under the **Apache License 2.0**.

This license permits use, modification, distribution, and commercial application of the code, while providing explicit patent protection for both contributors and users. It is particularly suitable for research-oriented software and AI-driven data-mining workflows.

For the full license text, please refer to the [Apache-2.0 license](https://github.com/yichun77/MatDataMiner/blob/main/LICENSE) file.
