import os
import psycopg2
import PyPDF2
from langchain_huggingface import HuggingFaceEmbeddings

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=1000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Function to generate embeddings for text chunks
def generate_embeddings(text_chunks):
    
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "YOUR_HUGGINGFACE_API_KEY"  # Replace with your API key
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"  # Specify the model
    )
    
    # Generate embeddings for the text chunks
    embeddings = embedding_model.embed_documents(text_chunks)
    return embeddings

# Function to store data in PostgreSQL
def store_embeddings_in_postgresql(text_chunks, embeddings):
    """Store text chunks and their corresponding embeddings in PostgreSQL."""
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="YOUR_DBNAME", 
        user="YOUR_USERNAME", 
        password="PASSWORD", 
        host="localhost"
    )
    cur = conn.cursor()
    
    for text, embedding in zip(text_chunks, embeddings):
        cur.execute("""
            INSERT INTO documents (text, embedding)
            VALUES (%s, %s)
        """, (text, embedding))
    conn.commit()
    print("Embeddings stored in PostgreSQL successfully.")
    
    cur.close() 
    conn.close() 

# Function to retrieve and display stored data
def retrieve_and_display_data():
    conn = psycopg2.connect(
        dbname="YOUR_DBNAME", 
        user="YOUR_USERNAME", 
        password="PASSWORD", 
        host="localhost" 
    )
    cursor = conn.cursor()

    # Retrieve text and embeddings
    cursor.execute("SELECT text, embedding FROM documents")
    records = cursor.fetchall()
    
    # Display the results
    for record in records:
        text, embedding = record
        print("Text:", text[:100], "...")  # Print first 100 characters of text
        print("Embedding:", embedding[:5], "...")  # Print first 5 values of the embedding
        print()

    cursor.close()
    conn.close()

# Main script execution
if __name__ == "__main__":
    pdf_path = "doc1.pdf"  # Path to your PDF document

    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Split text into chunks
    text_chunks = split_text_into_chunks(pdf_text)

    # Generate embeddings for the text chunks
    embeddings = generate_embeddings(text_chunks)

    # Store text chunks and embeddings in PostgreSQL
    store_embeddings_in_postgresql(text_chunks, embeddings)

    # Retrieve and display stored data
    retrieve_and_display_data()