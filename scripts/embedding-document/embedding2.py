import os
import psycopg2
import PyPDF2
from langchain_huggingface import HuggingFaceEmbeddings

def get_pdf_text(pdf_file):
    content = ""
    with open(pdf_file, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            content += page.extract_text() + "\n"
    return content

def chunk_text(content, chunk_length=1000):
    return [content[i:i + chunk_length] for i in range(0, len(content), chunk_length)]

def create_embeddings(chunks):
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "api-key"
    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    chunk_embeddings = model.embed_documents(chunks)
    return chunk_embeddings

def insert_embeddings_to_db(chunks, embeddings):
    conn = psycopg2.connect(dbname="mydb", user="postgres", password="yourpsswd", host="localhost")
    cursor = conn.cursor()
    
    for chunk, embedding in zip(chunks, embeddings):
        cursor.execute("""
            INSERT INTO embeddings (document, embedding)
            VALUES (%s, %s)
        """, (chunk, embedding))
    
    conn.commit()
    print("Data successfully saved to PostgreSQL.")
    
    cursor.close()
    conn.close()

def fetch_and_print_data():
    conn = psycopg2.connect(dbname="mydb", user="postgres", password="yourpsswd", host="localhost")
    cur = conn.cursor()
    
    cur.execute("SELECT document, embedding FROM embeddings")
    rows = cur.fetchall()

    for row in rows:
        doc, embedding = row
        print("Document:", doc[:100], "...")
        print("Embedding (first 5 values):", embedding[:5], "...")
        print()

    cur.close()
    conn.close()

if __name__ == "__main__":
    pdf_file = "doc1.pdf"
    extracted_text = get_pdf_text(pdf_file)
    chunks = chunk_text(extracted_text)
    chunk_embeddings = create_embeddings(chunks)
    insert_embeddings_to_db(chunks, chunk_embeddings)
    fetch_and_print_data()
