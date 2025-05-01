'use client';

import { useState, useRef } from 'react';
import { useTypewriter } from '@/hooks/useTypewriter';
import { Question, ChatMessage, ApiResponse } from '@/types';
import ReactMarkdown from 'react-markdown';
import { animateScroll } from 'react-scroll';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Send, Loader2 } from 'lucide-react';

export default function LearningAgentPage() {
  const [learningGoal, setLearningGoal] = useState('');
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [userAnswer, setUserAnswer] = useState('');
  const [feedback, setFeedback] = useState('');
  const [showExam, setShowExam] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const chatContainerRef = useRef<HTMLDivElement>(null);
  const feedbackRef = useRef<HTMLDivElement>(null);

  const { displayText: systemResponse, isTyping } = useTypewriter(
    chatHistory.length > 0 ? chatHistory[chatHistory.length - 1].content : '',
    20
  );

  const handleSubmit = async () => {
    if (!learningGoal.trim()) {
      alert('Please enter a learning goal');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('/api/learn', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: learningGoal,
          user_portrait: {
            metadata: {},
            learning_profile: {},
          },
        }),
      });

      const data: ApiResponse = await response.json();
      
      const newMessages: ChatMessage[] = [
        { role: 'user', content: learningGoal },
        { role: 'system', content: data.answer },
      ];
      
      setChatHistory((prev) => [...prev, ...newMessages]);
      setQuestions(data.exam_questions.questions);
      setCurrentQuestion(data.exam_questions.questions[0]);
      setShowExam(true);
      setLearningGoal('');
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred, please try again');
    } finally {
      setIsLoading(false);
    }
  };

  const checkAnswer = () => {
    if (!currentQuestion || !userAnswer) {
      alert('Please answer the question first');
      return;
    }

    const isCorrect = userAnswer.toLowerCase() === currentQuestion.correct_answer.toLowerCase();
    const feedback = isCorrect
      ? '✅ Correct!'
      : `❌ Incorrect, the correct answer is: ${currentQuestion.correct_answer}`;
    
    setFeedback(feedback);
    
    setTimeout(() => {
      if (feedbackRef.current) {
        animateScroll.scrollTo(feedbackRef.current.offsetTop, {
          duration: 500,
          smooth: true,
        });
      }
    }, 100);
  };

  const nextQuestion = () => {
    if (questionIndex < questions.length - 1) {
      setQuestionIndex(prev => prev + 1);
      setCurrentQuestion(questions[questionIndex + 1]);
      setUserAnswer('');
      setFeedback('');
    } else {
      alert('Quiz completed!');
      setShowExam(false);
      setQuestionIndex(0);
      setCurrentQuestion(null);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gradient-to-b from-white to-gray-50/50 dark:from-gray-900 dark:to-gray-800/50">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Hero Section */}
        <div className="text-center mb-12 max-w-2xl mx-auto">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-violet-600 bg-clip-text text-transparent leading-tight">
            AI Learning Assistant
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 mx-auto max-w-xl">
            Enter your learning goals and let AI create a personalized learning plan for you
          </p>
        </div>
        
        <div className="grid gap-8 lg:grid-cols-[2fr_1fr] items-start max-w-[1200px] mx-auto">
          {/* Left Column: Chat Interface */}
          <Card className="p-8 shadow-lg bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm">
            <div className="mb-8">
              <Label 
                htmlFor="learning-goal" 
                className="text-xl font-medium mb-4 block text-gray-700 dark:text-gray-200 text-center"
              >
                Learning Goal
              </Label>
              <div className="max-w-2xl mx-auto">
                <Textarea
                  id="learning-goal"
                  value={learningGoal}
                  onChange={(e) => setLearningGoal(e.target.value)}
                  placeholder="Enter what you want to learn or skills you want to develop..."
                  className="min-h-[120px] text-lg resize-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 w-full"
                />
              </div>
            </div>
            
            <div className="flex justify-center mb-8">
              <Button
                onClick={handleSubmit}
                disabled={isLoading}
                className="px-8 py-6 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl transition-all duration-200 disabled:opacity-50 flex items-center space-x-3 text-lg h-auto"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-6 w-6 animate-spin" />
                    <span>Generating...</span>
                  </>
                ) : (
                  <>
                    <Send className="h-6 w-6" />
                    <span>Send</span>
                  </>
                )}
              </Button>
            </div>

            <ScrollArea className="h-[500px] rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
              <div ref={chatContainerRef} className="p-6 space-y-6">
                {chatHistory.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`p-6 rounded-xl ${
                      msg.role === 'user' 
                        ? 'bg-blue-50 dark:bg-blue-900/30 ml-16 border border-blue-100 dark:border-blue-800' 
                        : 'bg-gray-50 dark:bg-gray-900/50 mr-16 border border-gray-100 dark:border-gray-800'
                    }`}
                  >
                    <div className="font-medium mb-3 text-base text-gray-600 dark:text-gray-400">
                      {msg.role === 'user' ? 'You:' : 'AI:'}
                    </div>
                    <div className="prose prose-lg dark:prose-invert max-w-none">
                      <ReactMarkdown>
                        {msg.role === 'system' && idx === chatHistory.length - 1
                          ? systemResponse
                          : msg.content}
                      </ReactMarkdown>
                    </div>
                  </div>
                ))}
                {isTyping && (
                  <div className="flex items-center justify-center space-x-2 text-gray-400 p-4">
                    <div className="w-3 h-3 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-3 h-3 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-3 h-3 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                )}
              </div>
            </ScrollArea>
          </Card>

          {/* Right Column: Exam Interface */}
          {showExam && currentQuestion && (
            <Card className="p-8 shadow-lg bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm sticky top-24">
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-200">Practice Quiz</h2>
                <span className="px-6 py-3 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-lg font-medium">
                  {questionIndex + 1}/{questions.length}
                </span>
              </div>
              
              <div className="mb-8">
                <p className="text-lg mb-8 text-gray-700 dark:text-gray-300 leading-relaxed">
                  {currentQuestion.question_text}
                </p>
                
                {currentQuestion.type === 'multiple_choice' ? (
                  <RadioGroup
                    value={userAnswer}
                    onValueChange={setUserAnswer}
                    className="space-y-4"
                  >
                    {currentQuestion.options?.map((option) => (
                      <div 
                        key={option.label}
                        className="relative flex items-start p-6 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-150 border border-gray-200 dark:border-gray-700"
                      >
                        <div className="flex items-center h-6">
                          <RadioGroupItem 
                            value={option.label} 
                            id={option.label}
                            className="w-5 h-5"
                          />
                        </div>
                        <Label 
                          htmlFor={option.label}
                          className="ml-4 flex-1 cursor-pointer text-lg text-gray-700 dark:text-gray-300"
                        >
                          <span className="font-medium">{option.label}.</span> {option.content}
                        </Label>
                      </div>
                    ))}
                  </RadioGroup>
                ) : (
                  <Input
                    value={userAnswer}
                    onChange={(e) => setUserAnswer(e.target.value)}
                    placeholder="Enter your answer..."
                    className="text-lg p-6 focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700"
                  />
                )}
              </div>

              <div ref={feedbackRef} className="space-y-6">
                {feedback && (
                  <div className={`p-6 rounded-xl text-lg ${
                    feedback.startsWith('✅') 
                      ? 'bg-green-50 dark:bg-green-900/30 text-green-800 dark:text-green-200' 
                      : 'bg-red-50 dark:bg-red-900/30 text-red-800 dark:text-red-200'
                  }`}>
                    {feedback}
                  </div>
                )}
                
                <div className="flex space-x-4">
                  <Button 
                    onClick={checkAnswer}
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-lg py-6 h-auto"
                  >
                    Submit Answer
                  </Button>
                  {feedback && (
                    <Button 
                      onClick={nextQuestion}
                      className="flex-1 bg-gray-600 hover:bg-gray-700 text-white text-lg py-6 h-auto"
                    >
                      Next Question
                    </Button>
                  )}
                </div>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}