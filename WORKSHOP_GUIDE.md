# Maritime Insurance Processing Workshop Guide

## Workshop Overview

This hands-on workshop will guide you through building a multi-step workflow using LangChain and LangGraph to process maritime insurance documents, extract key information, look up vessel and company history, and generate risk assessments.

## Workshop Duration: 2 hours

## Prerequisites

- Python 3.13+
- Basic understanding of Python
- OpenAI API key

## Setup (Before Workshop)

1. Clone the repository:
   ```bash
   git clone https://github.com/oysmal/langchain-workshop-2.git
   cd langchain-workshop-2
   ```

2. Install Devbox (either):
   - See [official instructions](https://www.jetify.com/docs/devbox/installing_devbox)
   - Or, on Mac/Linux run:
     ```bash
     curl -fsSL https://get.jetify.com/devbox | bash
     ```

3. Set up your environment:
   ```bash
   cp .env.template .env.local
   # Edit .env.local to add your OpenAI API key
   ```

4. Start the Devbox shell:
   ```bash
   devbox shell
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Introduction (20 minutes)

We will present:
- Overview of LangChain and LangGraph
- Key concepts and techniques
- Maritime insurance processing workflow
- Project structure and components

## Step 1: Hello World LangChain (20 minutes)

**Branch: `step-1`**

In this step, you'll create a simple LangChain application to understand the basics.

1. Open `src/main.py` and implement a basic LangChain chain:
   ```python
   # TODO: Use langchain to create an llm chain that:
   # 1. Uses a prompt template to format the input
   # 2. Uses OpenAI's LLM to generate a response
   # 3. Prints the response
   ```

   Suggestion: Use `ChatPromptTemplate` to create a prompt template that formats the input for the LLM.
   Idea: Add a prompt that takes a word as input and generates a dad joke based on that word.

2. Test your implementation:
   ```bash
   python -m src.main
   ```
## Step 2: Document Processing (20 minutes)

**Branch: `step-2`**

In this step, you'll set up your LangGraph workflow, and implement document processing to handle different file types.

1. Open `src/workflow_state.py` and add a new entry for the documents to the state class. These should be a list of Documents.

2. Open `src/main.py` and complete the `create_workflow` and `process_documents` methods. You must instantiate your StateGraph using your WorkflowState class. Then, add a node for document processing to the workflow, and edges between START, your new node, and END.

3. Open `src/document_processor.py` and implement the missing methods:
   ```python
   # TODO: Implement the load_pdf method
   # TODO: Implement the load_excel method
   # TODO: Update the process_documents method
   ```

   Hint: You need `PyPDFLoader` and `UnstructuredExcelLoader`

4. Print the loaded documents when the workflow has run

5. Test your implementation:
   ```bash
   python -m src.main
   ```

**Key Concepts:**
- LangGraph for workflow management
- Document loaders from langchain_community
- Handling different file types (PDF, text, Excel)
- Combining documents from multiple sources

**Expected Output:**
A list of Document objects containing the content from the PDF, text, and Excel files.

## Step 3: Information Extraction (20 minutes)

**Branch: `step-3`**

In this step, you'll implement structured information extraction from documents.

1. Open `src/information_extractor.py` and implement the extraction methods:
   ```python
   # TODO: Implement the extract_entity_data method
   # TODO: Implement the extract_financial_data method
   # TODO: Implement the extract_insurance_risk_data method
   ```
You will have to use `ChatPromptTemplate` to create a prompt template, and combine this with appropriate structured output entities for parsing.

2. Update `src/main.py` and `src/workflow_state.py` to add a node for information extraction:
   ```python
   # TODO: Use the InformationExtractor to extract structured data from the documents and store in the state
   ```

3. Print the extracted data when the workflow has run.

4. Test your implementation:
   ```bash
   python -m src.main
   ```

**Key Concepts:**
- Structured extraction with LLMs
- Pydantic models for validation
- Extraction chains
- Prompt engineering for extraction

**Expected Output:**
Structured data objects containing entity information (company, vessels), financial data (premium, loss ratio), and insurance risk data.

## Step 4: Lookup Vessel and Company History (20 minutes)

**Branch: `step-4`**

In this step, you'll implement a node for looking up vessel and company history.

1. Update `src/main.py` to add a node for history lookup:
   ```python
   # TODO: Use the clients src/history_lookup.py to look up vessel and company history
   ```

2. Add a new entry to the state class in `src/workflow_state.py` for the history data.

3. Test your implementation:
   ```bash
   python -m src.main
   ```

**Expected Output:**
History data for vessels and companies, including incidents and claims.

## Step 5: Risk Assessment (20 minutes)

**Branch: `step-5`**

In this step, you'll implement risk assessment using LLMs.

1. Open `src/models.py` and add pydantic fields to the `Assessment` model.

2. Open `src/risk_assessor.py` and implement the assessment methods:

3. Update `src/main.py` to add a node for risk assessment:

4. Test your implementation:
   ```bash
   python -m src.main
   ```

**Key Concepts:**
- LLM chains with structured output
- Prompt engineering for assessment
- Using Pydantic models for structured outputs
- Combining multiple data sources for assessment

**Expected Output:**
A structured assessment object containing a summary, recommendation, risk score, and points of attention.

## Project Structure

The project is organized as follows:

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

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [LangChain Structured Output Guide](https://python.langchain.com/docs/how_to/output_parser_structured/)

## Troubleshooting

### Common Issues

1. **OpenAI API Key**
   If you encounter authentication errors, check that your OpenAI API key is correctly set in `.env.local`.

2. **Import Errors**
   Ensure you've installed all dependencies from requirements.txt.

3. **File Path Issues**
   The project uses relative paths from the project root. Always run scripts from the project root directory.

5. **Model Errors**
   If you encounter errors related to the OpenAI model, check that you're using a supported model name in your code.