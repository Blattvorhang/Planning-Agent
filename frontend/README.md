
# 🧠 Learning Agent Frontend

An AI-powered learning assistant frontend built with **Next.js + TypeScript + Tailwind CSS**. Supports learning goal generation, markdown-based explanations, and interactive quizzes (multiple choice + fill-in-the-blank).

---

## 📁 Project Structure

```bash
src/
├── app/                     # App Router pages and layout
│   ├── layout.tsx
│   ├── page.tsx             # Main entry point (chat + input + quiz)
│   └── globals.css
├── components/
│   ├── chat/                # Chat components (ChatArea, MessageList, Input)
│   ├── question/            # Quiz components (MultipleChoice, FillInTheBlank)
│   ├── QuizController/      # Central quiz flow controller
│   ├── ui/                  # Shared UI components (Button, Textarea, etc.)
├── hooks/
│   └── useTypewriter.ts     # Typing effect hook
├── lib/
│   ├── mapServerQuestions.ts# Adapts backend quiz data to frontend format
│   └── utils.ts             # Utility functions
├── types/
│   └── index.ts             # Global type definitions

```
## 🚀 Getting Started
```bash
# Install dependencies
npm install

# Start the development server (default: http://localhost:3000)
npm run dev
```
Make sure your FastAPI backend is running at http://localhost:8000.


## 🧩 Key Features
- ✅ AI-generated learning goals and explanations
- ✅ Markdown rendering with syntax highlighting
- ✅ Multiple-choice and fill-in-the-blank quiz support
- ✅ Instant feedback with correct answer display
- ✅ Chat history with smooth UI transitions


## 🔌 API Details

Endpoint
```
POST /api/learn
```
Request Body
```
{
  "prompt": "What is a string?",
  "user_portrait": {
    "metadata": {},
    "learning_profile": {}
  }
}
```
Response Structure
```
{
  "learning_goal": "...",
  "answer": "...",
  "exam_questions": {
    "questions": [
      {
        "type": "multiple_choice" | "fill_in_blank",
        "question_text": "...",
        "options": [...],           // only for multiple choice
        "correct_answer": "..."
      }
    ]
  }
}
```
The questions are adapted to frontend format 
using ```lib/mapServerQuestions.ts.```



🛠 Development Tips

Module	Description
QuizController	Controls quiz flow, feedback, and navigation
mapServerQuestions	Maps backend question format to frontend structure
types/index.ts	Centralized types for quiz, chat, and API data
useTypewriter	Typing animation (e.g. streaming answer rendering)



⸻

📌 TODO
- Add progress indicator and scoring
- Support question bookmarking / error review
- fix some bug
- support streaming

⸻

🤝 Author
- 🧑‍💻 Frontend by: huan-linwww

