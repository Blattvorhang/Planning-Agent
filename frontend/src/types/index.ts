export interface Option {
  label: string;
  content: string;
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

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  createdAt?: string; // 可选的时间戳字段
}

export interface ChoiceOption  {
  id: string;
  label: string;
};

export interface MultipleChoiceQuestion  {
  id: string;
  question: string;
  options: ChoiceOption[];
  correctId: string; // 标准答案
};

export interface FillInTheBlankQuestion  {
  id: string;
  question: string;      // 题干，支持有空格/提示词
  correctAnswer: string; // 标准答案
};

export type Question = MultipleChoiceQuestion | FillInTheBlankQuestion;