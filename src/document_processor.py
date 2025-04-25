from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def load_pdf(self, file_path):
        """Load a PDF file and split into chunks"""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
        
    def load_text(self, file_path):
        """Load a text file"""
        loader = TextLoader(file_path)
        documents = loader.load()
        return documents
        
    def process_documents(self, pdf_paths, text_paths):
        """Process all documents and return combined content"""
        all_documents = []
        
        for pdf_path in pdf_paths:
            all_documents.extend(self.load_pdf(pdf_path))
            
        for text_path in text_paths:
            all_documents.extend(self.load_text(text_path))
            
        return all_documents