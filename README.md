# 🎓 EdTech Assistant

EdTech Assistant is an AI-powered educational support system that helps students:
- 📚 Understand academic concepts using retrieval-based answers
- ✍️ Practice with auto-generated questions
- 🗃️ Log every interaction in a MySQL database

Built using: **FastAPI**, **Streamlit**, **LangChain**, **MySQL**, **ChromaDB**, and **HuggingFace embeddings**

---

## ⚙️ How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/VinayKul2k24/Edtech-Assistant.git
cd Edtech-Assistant
```
### 2. Install Requirements
```bash
pip install -r requirements.txt
```
### 3. Add PDFs
```bash
knowledge_base/
├── dsa.pdf
├── algebra.pdf
```
### 4. Run the FastAPI Server
```bash
python main.py
```
### 5. Run the Streamlit App
```bash
streamlit run app.py
```



