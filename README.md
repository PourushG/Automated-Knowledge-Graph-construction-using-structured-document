# Automated-Knowledge-Graph-construction-using-structured-document
An end-to-end system for constructing knowledge graphs from structured documents. This system can extract entities, relationships, and properties from documents of various formats and automatically build and visualize a knowledge graph. It also supports schema refinement and updates for handling multiple document formats dynamically.

# Features

Automated Knowledge Graph Construction:
Extracts entities, relationships, and relevant properties from structured documents.
Inferences schemas without predefined templates, making it adaptable to various domains.

Document Parsing:
Supports multiple formats: PDF, DOCX, TXT, and more.

Dynamic Prompting for Schema Refinement:
Enables users to refine inferred schemas interactively.

Knowledge Graph Visualization:
Visualizes the graph using NetworkX and Matplotlib, displayed directly in the Streamlit web app.

Multi-Format Handling:
Automatically processes and updates the knowledge graph when new documents are added.

Extensible Framework:
Allows easy integration of additional formats or modules for specialized use cases.

# Prerequisites
Python 3.8 or higher
Required Python libraries (see requirements.txt):
streamlit
matplotlib
networkx
pdfminer.six
python-docx
Any other dependencies

# Installation
Clone this repository: git clone https://github.com/yourusername/automated-knowledge-graph-builder.git
cd automated-knowledge-graph-builder

Install dependencies:pip install -r requirements.txt
Run the application: streamlit run main_file.py

# How to Use

Upload a Document:
Choose a structured document (PDF, DOCX, TXT, etc.) from your computer.
The document will be parsed, and its text will be extracted.

Extract Entities and Relationships:
The app will infer entities and relationships from the document text.
Results will be displayed in the app.

Visualize the Knowledge Graph:
The extracted entities and relationships will be visualized as a knowledge graph within the app.

Refine the Schema:
Use the dynamic prompting interface to correct or refine the schema:
Add or remove entities and relationships.
Refine properties and definitions.

Handle Multiple Formats:
The app supports processing and updating the graph with new documents in real time.

# Technologies Used
Python:
Core programming language.
Streamlit:
Web interface for document upload and graph interaction.
NetworkX:
For creating and managing the knowledge graph.
Matplotlib:
For graph visualization.
PDFMiner and python-docx:
For parsing PDFs and DOCX files.
