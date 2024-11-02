from fastapi import FastAPI,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

import os
import psycopg2
import uuid
import PyPDF2
from langchain_huggingface import HuggingFaceEmbeddings

app = FastAPI()



def extractTextFromPDF(text_url):
    text = ""
    with open(text_url,"rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def splitTextIntoChunks(text,chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0,len(text),chunk_size)]


def generateEmbeddings(text_chunks):
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "HUGGING_FACE_API_KEY"
    
    embedding_model = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )
    
    embeddings = embedding_model.embed_documents(text_chunks)
    return embeddings

def storeEmbeddingsInDB(embedding_id,text_chunks,embeddings):
    
    conn = psycopg2.connect(
        dbname = "DBNAME",
        user = "USERNAME",
        password = "PASSWORD",
        host = "localhost"
    )
    
    cur = conn.cursor()
    
    for text,embedding in zip(text_chunks,embeddings):
        cur.execute("""
            INSERT INTO embeddings (embedding_id,text, embedding)
            VALUES (%s, %s,%s)
        """, (embedding_id,text, embedding))
    conn.commit()
    print("Embeddings stored in PostgreSQL successfully.")
    
    cur.close()  
    conn.close()  
    
    return embedding_id
    

class EmbeddingRequestBody(BaseModel):
    title: str
    content_url : Optional[str] = None
    text_content : Optional[str] = None
    
class ErrorResponse(BaseModel):
    status : str
    message : str
    reason : str
    error_code : str
    
class SuccessResponse(BaseModel):
    status : str
    message : str
    embedding_id : str

@app.post('/api/v1/embeddings')
async def createEmbeddings(request:EmbeddingRequestBody):
    if not request.text_content and not request.content_url:
        error_response = ErrorResponse(
            status="Error",
            message="Embedding Failed.",
            reason="Either content url or text content must be provided.",
            error_code="400_BAD_REQUEST"
        )
        
        raise HTTPException(
            status_code =400,
            detail = error_response.dict()
        )
        
    if request.content_url :
        text = extractTextFromPDF(request.content_url)
    else :
        text = request.text_content
        
    text_chunks = splitTextIntoChunks(text)
    embeddings = generateEmbeddings(text_chunks)
    
    
    try:
        
        embedding_id = str(uuid.uuid4())
        stored_id = storeEmbeddingsInDB(embedding_id,text_chunks,embeddings)
        success_response = SuccessResponse(
            status="Success",
            message="Content successfully processed and embedding stored.",
            embedding_id=stored_id
        )  
        
        return success_response
    
    except Exception as e :
        error_response = ErrorResponse(
            status="Error",
            message="Embedding Failed",
            reason = str(e),
            error_code="500_INTERNAL_ERROR"
        ) 
        
        raise HTTPException(status_code=500,detail=error_response.dict())
         