# Maritime Insurance Processing Tutorial

This tutorial demonstrates how to use LangChain and LangGraph to build a multi-step workflow for processing maritime insurance documents, extracting key information, looking up vessel and company history, and generating risk assessments.

## Project Structure

```
maritime_insurance_tutorial/
├── README.md
├── requirements.txt
├── data/
│   ├── company_info.pdf
│   ├── insurance_offer.pdf
│   ├── broker_email.txt
│   └── mock_data.py
├── src/
│   ├── main.py                  # Entry point that ties everything together
│   ├── document_processor.py    # Document loading and text extraction
│   ├── information_extractor.py # Extract key info from documents
│   ├── history_lookup.py        # Custom tools for IMO/company lookups
│   ├── risk_assessor.py         # Generate risk assessment and summaries
│   └── models.py                # Pydantic models for structured data
└── utils/
    └── graph_visualizer.py      # Optional: Visualize the LangGraph workflow
```

## Setup

TODO:
explain how to install devbox
explain:
`cp .env.template .env.local`
edit .env.local (add openai key)

`$ devbox shell`
`$ pip install -r requirements.txt`
`$ python -m src.main`

also, move data out of src, like README suggests?

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Create sample PDF and text files in the `data` directory:
   - `company_info.pdf`: A PDF containing company information and vessel IMO numbers
   - `insurance_offer.pdf`: A PDF containing insurance offer details
   - `broker_email.txt`: A text file containing the email cover text from the broker

## Running the Application

To run the application, execute the following command:

```bash
python src/main.py
```

This will:

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

## Workshop Flow

1. **Introduction (10 minutes)**

   - Overview of the maritime insurance processing task
   - Introduction to LangChain and LangGraph

2. **Document Processing (15 minutes)**

   - Explain document loaders
   - Implement the document processor

3. **Information Extraction (15 minutes)**

   - Explain extraction chains
   - Implement the information extractor

4. **Custom Tools (15 minutes)**

   - Explain custom tools in LangChain
   - Implement the history lookup tools

5. **Risk Assessment (15 minutes)**

   - Explain LLM chains
   - Implement the risk assessor

6. **Workflow Creation (15 minutes)**

   - Explain LangGraph
   - Implement the main workflow

7. **Testing and Demonstration (15 minutes)**

   - Run the complete workflow
   - Discuss the results

8. **Q&A and Extensions (10 minutes)**
   - Answer questions
   - Discuss possible extensions

## Key Learning Points

1. How to use LangChain document loaders to process different file types
2. How to extract structured information from unstructured text
3. How to create custom tools for external data lookups
4. How to use LLMs for assessment and summarization
5. How to build a multi-step workflow using LangGraph
6. How to use Pydantic for data modeling and validation

