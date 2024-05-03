## Project README 🚀

### Project Overview:
This project utilizes various libraries and tools to create a system for logging in with Google, extracting text from PDF documents, splitting text into chunks, generating embeddings, and setting up a conversational question-answering chain.

### Libraries Used:
- `streamlit`: For creating interactive web applications.
- `firebase_admin`: For Firebase authentication.
- `PyPDF2`: For reading PDF documents.
- `langchain`: A library for text processing and question-answering.
- `dotenv`: For loading environment variables.
- `pathlib`: For working with file paths.
- `pyttsx3`: For text-to-speech conversion.

### Functionality:
1. **Login with Google:**
   - Users can log in using their Google account.
   - The system handles authentication using Firebase.

2. **Text Extraction:**
   - PDF documents are processed to extract text.
   - Text is split into manageable chunks for further processing.

3. **Embeddings Generation:**
   - Google Generative AI is used to generate embeddings for text chunks.
   - Embeddings are stored in a vector store using FAISS.

4. **Question-Answering Chain:**
   - A conversational question-answering chain is set up.
   - Users can ask detailed questions based on the provided context.

### Usage:
1. Run the `user_input` function with PDF documents and a user question to interact with the system.
2. The system automatically processes the PDFs, generates embeddings, and sets up the question-answering chain.
3. Users can ask questions based on the provided context and receive answers.

### Note:
- Ensure to replace the Firebase credentials file with your actual credentials.
- Make sure to have the necessary models and files in place for the system to function correctly.

### Contributors:
- This project was developed by Anjishnu Kumar,Abhijeet Kumar

### Feedback and Support:
- For any feedback, issues, or support, please contact abhku21aiml@cmrit.ac.in.

### Happy Coding! 🌟