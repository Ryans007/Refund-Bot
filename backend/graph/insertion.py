import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')

PATH = Path(__file__).resolve().parent.parent / 'data/base_conhecimento_ifood_genai-exemplo.csv'

# Carregar o CSV
df = pd.read_csv(PATH)

# Converter cada linha em um documento
documents = []
for idx, row in df.iterrows():
    content = " | ".join([f"{col}: {row[col]}" for col in df.columns])
    documents.append(Document(page_content=content, metadata={"row_index": idx}))

# Dividir documentos se necessário
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documents)

# Criar embeddings e vector store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

# Salvar para reutilizar
vectorstore.save_local("faiss_index")