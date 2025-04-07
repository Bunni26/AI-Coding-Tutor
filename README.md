# AI-Powered Coding Tutor Chatbot

An intelligent chatbot designed to help programmers and students learn coding concepts, debug code, and improve their programming skills.

## Features

- Natural language processing for programming queries
- Code generation and explanation
- Debugging assistance
- Code optimization suggestions
- Multi-language support (Python, Java, C++, JavaScript, etc.)
- Interactive learning experience
- Personalized responses based on user expertise

## Tech Stack

- Backend: Flask
- Frontend: React.js
- AI: OpenAI GPT-4/Codex API
- Framework: LangChain
- Database: Firebase (optional)

## Setup

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```
4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
5. Start the backend server:
   ```bash
   python app.py
   ```
6. Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

## Project Structure

```
.
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models/
│   ├── routes/
│   └── services/
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 