import os
import psycopg2
import PyPDF2
from langchain_huggingface import HuggingFaceEmbeddings

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=1000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Function to initialize Hugging Face embedding model
def initialize_embedding_model():
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "YOUR_HUGGINGFACE_API_KEY"  # Replace with your actual key
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Function to generate embeddings for text chunks
def generate_embeddings(embedding_model, text_chunks):
    return embedding_model.embed_documents(text_chunks)

# Function to connect to PostgreSQL
def connect_to_postgresql():
    return psycopg2.connect(
        dbname="YOUR_DBNAME",
        user="YOUR_USERNAME",
        password="PASSWORD",
        host="localhost"  # Adjust if necessary
    )

# Function to store text and embeddings in PostgreSQL
def store_embeddings_in_postgresql(conn, text_chunks, embeddings):
    with conn.cursor() as cur:
        insert_query = """
            INSERT INTO doc_embed (text, embedding)
            VALUES (%s, %s)
        """
        cur.executemany(insert_query, zip(text_chunks, embeddings))
    conn.commit()

# Function to retrieve and display stored data from PostgreSQL
def retrieve_and_display_data(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT text, embedding FROM doc_embed")
        for text, embedding in cur.fetchall():
            print(f"Text: {text[:100]} ...")  # Print first 100 characters
            print(f"Embedding: {embedding[:5]} ...")  # Print first 5 values of the embedding
            print()

# Main script execution
def main():
    pdf_path = "doc1.pdf"  # Path to your PDF document

    # Step 1: Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Step 2: Split the text into manageable chunks
    text_chunks = split_text_into_chunks(pdf_text)

    # Step 3: Initialize embedding model and generate embeddings
    embedding_model = initialize_embedding_model()
    embeddings = generate_embeddings(embedding_model, text_chunks)

    # Step 4: Connect to PostgreSQL and store the embeddings
    conn = connect_to_postgresql()
    store_embeddings_in_postgresql(conn, text_chunks, embeddings)

    # Step 5: Retrieve and display stored data
    retrieve_and_display_data(conn)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
