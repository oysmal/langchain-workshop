# Maritime Insurance Processing Workshop Guide

This guide will walk you through building a multi-step workflow using LangChain and LangGraph to process maritime insurance documents, extract key information, look up vessel and company history, and generate risk assessments.

## Workshop Duration: 1.5 hours

## Prerequisites

- Python 3.13
- Basic understanding of Python
- Basic understanding of LangChain and LLMs
- Familiarity with Python Pydantic models
- OpenAI API key (set as environment variable `OPENAI_API_KEY`)

## Setup (10 minutes)

1. Clone the repository:
   ```bash
   git clone https://github.com/oysmal/langchain-workshop.git
   cd langchain-workshop-2
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

4. Create the sample PDF files:
   ```bash
   python utils/create_sample_pdfs.py
   ```
   
   Note: Sample data files will be created in the src/data/ directory

## Project Structure

The project is organized as follows:

```bash
langchain-workshop/
├── README.md
├── requirements.txt
├── test_workflow.py           # Main test script
├── WORKSHOP_GUIDE.md          # This guide
├── src/
│   ├── __init__.py
│   ├── document_processor.py  # Document loading and processing
│   ├── information_extractor.py # Extract structured info from documents
│   ├── history_lookup.py      # Custom tools for lookups
│   ├── risk_assessor.py       # Generate risk assessments
│   ├── models.py              # Pydantic models for data
│   └── data/                  # Sample data files
│       ├── mock_data.py       # Mock data for lookups
│       └── [sample files]     # PDF and text files
└── utils/
    ├── create_sample_pdfs.py  # Script to create sample PDFs
    └── graph_visualizer.py    # Visualize the workflow graph
```

## Workshop Modules

### 1. Introduction (10 minutes)

- Overview of the maritime insurance processing task
- Introduction to LangChain and LangGraph
- Overview of the LangChain ecosystem (Core, Community, OpenAI)
- Explanation of the project structure

### 2. Document Processing (15 minutes)

In this module, we'll explore how to use LangChain document loaders to process PDF and text files.

1. Open `src/document_processor.py`
2. Review the `DocumentProcessor` class and its methods
3. Understand how different document types are loaded and processed

Key concepts:
- LangChain document loaders from langchain_community
- Document processing without chunking in this implementation
- Handling multiple document types

### 3. Information Extraction (15 minutes)

In this module, we'll learn how to extract structured information from unstructured text using LangChain.

1. Open `src/information_extractor.py`
2. Review the extraction schemas defined using Pydantic
3. Understand how structured output works with LLMs

Key concepts:
- Extraction using structured output
- Pydantic schemas for structured data
- Prompt engineering for extraction

### 4. Custom Tools (15 minutes)

In this module, we'll implement custom LangChain tools for looking up vessel and company history.

1. Open `src/history_lookup.py`
2. Review the custom tool implementations
3. Understand how tools interact with mock data in `src/data/mock_data.py`

Key concepts:
- Custom LangChain tools
- Tool input schemas
- Error handling in tools

### 5. Risk Assessment (15 minutes)

In this module, we'll use LLM chains to generate risk assessments and summaries based on the extracted information and history lookups.

1. Open `src/risk_assessor.py`
2. Review the risk assessment implementation
3. Understand how to use structured output for parsing LLM responses

Key concepts:
- LLM chains with structured output
- Prompt engineering for assessment
- Using Pydantic models for structured outputs

### 6. Workflow Creation (15 minutes)

In this module, we'll use LangGraph to create a multi-step workflow that ties all the components together.

1. Open `src/main.py`
2. Review the node functions and workflow creation
3. Understand how data flows through the graph
4. Note the use of TypedDict for state management

Key concepts:
- LangGraph state management with TypedDict
- Node functions
- Graph compilation and execution

### 7. Testing and Demonstration (15 minutes)

In this module, we'll run the complete workflow and analyze the results.

1. Run the test script:
   ```bash
   python test_workflow.py
   ```

2. Review the output and understand how each component contributes to the final result

3. Visualize the workflow graph:
   ```bash
   python utils/graph_visualizer.py
   ```
   This will create a JSON file at `utils/output/workflow_graph.json` that you can visualize using tools like https://jsoncrack.com/

Key concepts:
- End-to-end testing
- Workflow visualization
- Debugging and error handling

## Extensions and Next Steps

Here are some ideas for extending the project after the workshop:

1. Add more sophisticated document processing (e.g., table extraction)
2. Implement real API calls for vessel and company history lookups
3. Add a web interface for uploading documents and viewing results
4. Implement more complex risk assessment logic
5. Add human-in-the-loop validation steps
6. Implement database storage for the processed data
7. Implement multi-vessel processing (the current implementation only processes one vessel)
8. Add error handling and retry mechanisms for API calls

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [LangChain Structured Output Guide](https://python.langchain.com/docs/modules/model_io/output_parsers/structured)

## Troubleshooting

### Common Issues

1. **Missing PDF Files**
   If the test script reports missing PDF files, ensure you've run the `utils/create_sample_pdfs.py` script first.

2. **OpenAI API Key**
   If you encounter authentication errors, check that your OpenAI API key is correctly set as an environment variable.

3. **Import Errors**
   If you encounter import errors, ensure you've installed all dependencies from requirements.txt.

4. **File Path Issues**
   The project uses relative paths from the project root. Always run scripts from the project root directory.