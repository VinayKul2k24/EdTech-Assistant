from langchain_community.document_loaders import PyPDFLoader  # More reliable than DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os


def setup_rag():
    # Get absolute path to knowledge_base
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    knowledge_path = os.path.join(base_dir, "knowledge_base")

    # Load PDFs one by one with error handling
    documents = []
    for file in os.listdir(knowledge_path):
        if file.endswith(".pdf"):
            try:
                loader = PyPDFLoader(os.path.join(knowledge_path, file))
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading {file}: {str(e)}")
                continue

    if not documents:
        raise ValueError("No valid PDF documents found in knowledge_base!")

    # More robust text splitting
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)

    # Initialize embeddings with proper settings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    # Create vector store with error handling
    try:
        vector_db = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory="./chroma_db"
        )
        print("Vector store created successfully!")
        return vector_db
    except Exception as e:
        print(f"Error creating vector store: {str(e)}")
        raise


def get_rag_answer(query: str, vector_db):
    if not vector_db:
        return "System error: Knowledge base not loaded properly"

    try:
        results = vector_db.similarity_search(query, k=2)
        if not results:
            return "No relevant information found"
        return "\n\n".join([doc.page_content for doc in results])
    except Exception as e:
        return f"Error retrieving answer: {str(e)}"