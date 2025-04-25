# Maritime Insurance Processing Workshop Guide

This guide will walk you through building a multi-step workflow using LangChain and LangGraph to process maritime insurance documents, extract key information, look up vessel and company history, and generate risk assessments.

## Workshop Duration: 1.5 hours

## Prerequisites

- Python 3.8+
- Basic understanding of Python
- OpenAI API key (set as environment variable `OPENAI_API_KEY`)

## Setup (10 minutes)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd maritime-insurance-tutorial
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

## Workshop Modules

### 1. Introduction (10 minutes)

- Overview of the maritime insurance processing task
- Introduction to LangChain and LangGraph
- Explanation of the project structure

### 2. Document Processing (15 minutes)

In this module, we'll explore how to use LangChain document loaders to process PDF and text files.

1. Open `src/document_processor.py`
2. Review the `DocumentProcessor` class and its methods
3. Understand how different document types are loaded and processed

Key concepts:
- LangChain document loaders
- Document processing and chunking
- Handling multiple document types

### 3. Information Extraction (15 minutes)

In this module, we'll learn how to extract structured information from unstructured text using LangChain extraction chains.

1. Open `src/information_extractor.py`
2. Review the extraction schemas defined using Pydantic
3. Understand how extraction chains work with LLMs

Key concepts:
- Extraction chains
- Pydantic schemas for structured data
- Prompt engineering for extraction

### 4. Custom Tools (15 minutes)

In this module, we'll implement custom LangChain tools for looking up vessel and company history.

1. Open `src/history_lookup.py`
2. Review the custom tool implementations
3. Understand how tools interact with external data sources (mock data in this case)

Key concepts:
- Custom LangChain tools
- Tool input schemas
- Error handling in tools

### 5. Risk Assessment (15 minutes)

In this module, we'll use LLM chains to generate risk assessments and summaries based on the extracted information and history lookups.

1. Open `src/risk_assessor.py`
2. Review the risk assessment chain implementation
3. Understand how to parse LLM outputs into structured data

Key concepts:
- LLM chains
- Prompt engineering for assessment
- Parsing unstructured LLM outputs

### 6. Workflow Creation (15 minutes)

In this module, we'll use LangGraph to create a multi-step workflow that ties all the components together.

1. Open `src/main.py`
2. Review the node functions and workflow creation
3. Understand how data flows through the graph

Key concepts:
- LangGraph state management
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

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)