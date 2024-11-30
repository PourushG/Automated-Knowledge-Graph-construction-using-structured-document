import spacy
import networkx as nx
import matplotlib.pyplot as plt
from tika import parser
import PyPDF2
import tempfile
import os
import streamlit as st

# Load pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

# Step 1: Document Parsing
import mimetypes

def parse_text_from_file(file_path):
    # Guess the file type
    mime_type, _ = mimetypes.guess_type(file_path)

    try:
        if mime_type == "application/pdf":
            # Handle PDFs
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = "".join([page.extract_text() for page in reader.pages])
            return text
        elif mime_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            # Handle DOCX/DOC
            raw = parser.from_file(file_path)
            return raw['content']
        elif mime_type == "text/plain":
            # Handle plain text files
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        else:
            raise ValueError("Unsupported file format. Please upload a PDF, DOCX, DOC, or TXT file.")
    except Exception as e:
        return f"Error processing file: {e}"


# Extract Entities and Relationships
from spacy.matcher import DependencyMatcher

def extract_entities_relationships(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print("Entities Found:", entities)

    matcher = DependencyMatcher(nlp.vocab)
    
    # Define patterns for subject-verb-object relationships
    pattern = [
        {"RIGHT_ID": "verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        {"LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "nsubj"}},
        {"LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ID": "object", "RIGHT_ATTRS": {"DEP": "dobj"}}
    ]
    matcher.add("SVO", [pattern])
    matches = matcher(doc)

    relationships = []
    for match_id, token_ids in matches:
        verb = doc[token_ids[0]].text
        subject = doc[token_ids[1]].text
        object_ = doc[token_ids[2]].text
        print(f"Match: {subject} {verb} {object_}")
        relationships.append((subject, verb, object_))
    
    # Capture additional relationships (e.g., prepositional objects)
    for token in doc:
        if token.dep_ == "ROOT":  # Main verb
            subject = [w.text for w in token.lefts if w.dep_ == "nsubj"]
            object_ = [w.text for w in token.rights if w.dep_ in {"dobj", "pobj"}]
            if subject and object_:
                relationships.append((subject[0], token.text, object_[0]))
    
    return entities, relationships


# Build Knowledge Graph
def build_graph(entities, relationships):
    graph = nx.DiGraph()
    for entity, label in entities:
        graph.add_node(entity, label=label)
    for subject, relation, object_ in relationships:
        graph.add_edge(subject, object_, label=relation)
    return graph

# Visualize Knowledge Graph
def visualize_graph(graph):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")
    edge_labels = nx.get_edge_attributes(graph, "label")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.title("Knowledge Graph Visualization")
    st.pyplot(plt)

# Dynamic Prompting for Refinement
def run_dynamic_prompting(graph):
    st.subheader("Dynamic Knowledge Graph Refinement")
    st.write("Refine your graph by adding entities and relationships.")

    entity_input = st.text_input("Add a new entity:")
    entity_label = st.selectbox("Select entity type:", ["ORG", "LOC", "PERSON", "DATE", "EVENT", "OTHER"])
    if st.button("Add Entity"):
        graph.add_node(entity_input, label=entity_label)
        st.write(f"Entity '{entity_input}' added to the graph!")

    subject_input = st.text_input("Subject of the relationship:")
    relation_input = st.text_input("Relationship (e.g., works_at, located_in):")
    object_input = st.text_input("Object of the relationship:")
    if st.button("Add Relationship"):
        graph.add_edge(subject_input, object_input, label=relation_input)
        st.write(f"Relationship '{subject_input} {relation_input} {object_input}' added to the graph!")

# Main Pipeline Integration
def main_pipeline():
    st.title("Automated Knowledge Graph Builder")
    
    # File Upload
    st.subheader("Upload Document")
    uploaded_file = st.file_uploader("Choose a file (PDF, DOCX, or TXT):", type=["pdf", "docx", "doc", "txt"])
    
    if uploaded_file:
        # Save the file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            file_path = temp_file.name

        st.subheader("Processing Document...")
        document_text = parse_text_from_file(file_path)
        if "Error processing file" in document_text:
            st.error(document_text)  # Display error to the user
        else:
            st.write("Extracted Text:")
            st.text_area("Extracted Text", document_text, height=200)

            st.subheader("Extracting Entities and Relationships...")
            entities, relationships = extract_entities_relationships(document_text)
            st.write("Entities:")
            st.write(entities)
            st.write("Relationships:")
            st.write(relationships)

            graph = build_graph(entities, relationships)
            st.subheader("Visualizing Knowledge Graph")
            visualize_graph(graph)

            run_dynamic_prompting(graph)


if __name__ == "__main__":
    main_pipeline()
