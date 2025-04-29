# Maritime Insurance Processing Tutorial

This tutorial demonstrates how to use LangChain and LangGraph to build a multi-step workflow for processing maritime insurance documents, extracting key information, looking up vessel and company history, and generating risk assessments.

## Project Structure

```
maritime_insurance_tutorial/
├── README.md
├── requirements.txt
├── src/
│   ├── data/
│   │   ├── company_info.pdf
│   │   ├── insurance_offer.pdf
│   │   ├── broker_email.txt
│   │   └── mock_data.py
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

This workshop uses Devbox, which is an open source tool that gives you a shell with all the necessary requirements, such
as the correct version of Python and a corresponding `venv`. (It does this declaratively by being built on the Nix package
manager, which is very cool!)

1. Install Devbox (either):
   (a). see [this official link](https://www.jetify.com/docs/devbox/installing_devbox)
   (b). or, if you're on Mac or Linux just run `curl -fsSL https://get.jetify.com/devbox | bash`

2. Clone this repository

3. Prepare the API key for OpenAI:

   1. run the following command in this repository: `cp .env.template .env.local`
   2. edit the new `.env.local` file and put your API key in the `OPENAI_API_KEY` variable

4. Start the devbox shell by running the command `devbox shell` (this might take a minute to install everything)

5. Now inside the devbox shell, install python dependencies with the following command: `pip install -r requirements.txt`

6. Test it out by running `python -m src.main`

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
