export interface Option {
  label: string;
  content: string;
}

export interface Question {
  type: 'multiple_choice' | 'fill_in_blank';
  question_text: string;
  options: Option[] | null;
  correct_answer: string;
}

export interface ExamQuestions {
  questions: Question[];
}

export interface ChatMessage {
  role: 'user' | 'system';
  content: string;
}

export interface ApiResponse {
  learning_goal: string;
  answer: string;
  exam_questions: ExamQuestions;
  user_portrait: any;
} 