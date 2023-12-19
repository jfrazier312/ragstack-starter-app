import os
from dotenv import load_dotenv

from ingestion.load import load_dataset, load_from_url
from ingestion.chunking import token_text_split, recursive_character_text_split
from ingestion.embeddings import open_ai_embeddings
from ingestion.storage.astradb import initialize_astra_db
from retrieval.chains import as_retriever, basic_chat, basic_chat_with_memory
from retrieval.prompts import PHILOSOPHER_PROMPT
from generation.models import chat_open_ai
from generation.query_loop import query_loop

from langchain_core.documents import Document

def load_data(): 
    {%- if cookiecutter.input_story == "Amontillado" %} 
    documents = load_from_url(
        "https://raw.githubusercontent.com/CassioML/cassio-website/main/docs/frameworks/langchain/texts/amontillado.txt",
        "data/amontillado.txt",
    )
    {%- elif cookiecutter.input_story == "Philosopher" %} 
    dataset = load_dataset("datastax/philosopher-quotes", split="train")
    documents = []
    for entry in dataset:
        metadata = {"author": entry["author"]}
        doc = Document(page_content=entry["quote"], metadata=metadata)
        documents.append(doc)
    {%- endif %}
    return documents

def split(documents):
    {%- if cookiecutter.chunk_strategy == "TokenTextSplit" %}
    split_documents = token_text_split(documents, chunk_size={{cookiecutter.chunk_size}}, chunk_overlap={{cookiecutter.chunk_overlap}})
    {%- elif cookiecutter.chunk_strategy == "RecursiveCharacterTextSplit" %}
    split_documents = recursive_character_text_split(documents, chunk_size={{cookiecutter.chunk_size}}, chunk_overlap={{cookiecutter.chunk_overlap}})
    {%- endif %}
    return split_documents


def prompt():
    {%- if cookiecutter.input_story == "Philosopher" %}
    prompt = PHILOSOPHER_PROMPT
    {%- elif cookiecutter.input_story == "Amontillado" %}
    prompt = """
    You are a very smart and helpful assistant that only knows about the provided context. Do not answer
    any questions that are not related to the context. Answer with extreme detail, pulling 
    quotes and supporting context directly from the provided context.  
    """
    {%- endif %}
    return prompt


def retrieval_chain(retriever, model, prompt):
    {%- if cookiecutter.qa_with_memory == "y" %}
    chain = basic_chat_with_memory(retriever, model, prompt)    
    {%- else %}
    chain = basic_chat(retriever, model, prompt)
    {%- endif %}
    return chain


def rag_starter_app():
    # Initialize environment variables
    load_dotenv()
    astra_db_token = os.environ["ASTRA_DB_APPLICATION_TOKEN"]
    api_endpoint = os.environ["ASTRA_DB_API_ENDPOINT"]

    # Ingestion
    documents = load_data()

    # Chunking
    split_documents = split(documents)

    # Storage / Embedding
    collection = input("Collection: ")
    embedding = open_ai_embeddings()
    vstore = initialize_astra_db(collection, embedding, astra_db_token, api_endpoint)

    print(f"Adding {len(split_documents)} documents to AstraDB...")
    vstore.add_documents(split_documents)

    # Retrieval
    my_prompt = prompt()
    retriever = as_retriever(vstore)
    model = chat_open_ai(model="{{cookiecutter.model}}")

    print(f"Initializing model with prompt:\n{my_prompt}")
    chain = retrieval_chain(retriever, model, my_prompt)

    # Generation
    query_loop(chain)


rag_starter_app()
