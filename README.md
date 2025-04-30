# Maritime Insurance Processing Tutorial

This tutorial demonstrates how to use LangChain and LangGraph to build a multi-step workflow for processing maritime insurance documents, extracting key information, looking up vessel and company history, and generating risk assessments.

Project structure

```
langchain-workshop/
├── README.md
├── requirements.txt
├── WORKSHOP_GUIDE.md          # This guide
├── src/
│   ├── __init__.py
│   ├── main.py                # Entry point and workflow
│   ├── document_processor.py  # Document loading and processing
│   ├── information_extractor.py # Extract structured info
│   ├── history_lookup.py      # Custom tools for lookups
│   ├── risk_assessor.py       # Generate risk assessments
│   ├── models.py              # Pydantic models
│   ├── utils.py               # Utility functions
│   └── data/                  # Sample data files
│       ├── mock_data.py       # Mock data for lookups
│       └── [sample files]     # PDF, text, and Excel files
```

## Setup

This workshop uses Devbox, which is an open source tool that gives you a shell with all the necessary requirements, such
as the correct version of Python and a corresponding `venv`. (It does this declaratively by being built on the Nix package
manager, which is very cool!)

For windows users:
- You must use Ubuntu Shell, not WSL. This can be installed via the Microsoft Store.
- When you run pip install, you must use `DISPLAY= pip install -r requirements.txt`.

1. Install Devbox (either):

   - (a). see [this official link](https://www.jetify.com/docs/devbox/installing_devbox)
   - (b). or, if you're on Mac or Linux just run this command:

     ```bash
     curl -fsSL https://get.jetify.com/devbox | bash
     ```

2. Clone this repository

3. Prepare the API key for OpenAI:

   1. run the following command in this repository:

   ```bash
   cp .env.template .env.local
   ```

   2. edit the new `.env.local` file and put your API key in the `OPENAI_API_KEY` variable

4. Start the devbox shell by running the following command (this might take a minute to install everything):

   ```bash
   devbox shell
   ```

5. Now inside the devbox shell, install python dependencies with the following command:

   ```bash
   pip install -r requirements.txt
   ```

6. Test it out by running the following command:

   ```python
   python -m src.main
   ```

## Running the Application

this will:

1. Process the PDF and text documents
2. Extract key information (company details, vessel IMO numbers, insurance offer)
3. Look up vessel and company history
4. Generate a risk assessment
5. Create a structured database entry

## Components

### Document Processor

Uses LangChain document loaders to process PDF and text files.

### Information Extractor

Uses LangChain extraction chains to extract structured information from unstructured text.

### History Lookup

Implements custom LangChain tools for looking up vessel and company history.

### Risk Assessor

Uses LLM chains to generate risk assessments and summaries based on the extracted information and history lookups.

### Main Workflow

Uses LangGraph to create a multi-step workflow that ties all the components together.

## Key Learning Points

1. How to use LangChain document loaders to process different file types
2. How to extract structured information from unstructured text
3. How to incorporate data lookups
4. How to use LLMs for assessment and summarization
5. How to build a multi-step workflow using LangGraph
6. How to use Pydantic for data modeling and validation
