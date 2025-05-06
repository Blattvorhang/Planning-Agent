'use client';

import { useState } from 'react';
import { ChatMessage, ApiResponse,  Question } from '@/types';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import QuizController from '@/components/QuizController/QuizController';
import { mapServerQuestions } from '@/lib/mapServerQuestions';
export default function LearningAgentPage() {
  const [learningGoal, setLearningGoal] = useState('');
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (!learningGoal.trim()) {
      alert('请输入学习目标');
      return;
    }

    setIsLoading(true);
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 90000); // 90秒超时

      const response = await fetch('/api/learn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: learningGoal,
          user_portrait: {
            metadata: {},
            learning_profile: {},
          },
        }),
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ApiResponse = await response.json();
      const newMessages: ChatMessage[] = [
        { role: 'user', content: learningGoal },
        { role: 'system', content: data.answer },
      ];

      // 使用mapServerQuestions转换题目数据
      const mappedQuestions = mapServerQuestions(data.exam_questions.questions);
      
      setChatHistory((prev) => [...prev, ...newMessages]);
      setQuestions(mappedQuestions);
      setLearningGoal('');
    } catch (error) {
      alert('发生错误，请重试');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50 dark:from-gray-900 dark:to-gray-800 px-4 py-10">
      <div className="container mx-auto max-w-4xl">
        {/* 聊天历史记录 */}
        <div className="bg-white dark:bg-gray-900 rounded-xl shadow p-6 mb-8">
          <div className="space-y-4 max-h-[400px] overflow-y-auto">
            {chatHistory.map((msg, idx) => (
              <div 
                key={idx} 
                className={`p-4 rounded-lg ${msg.role === 'user' 
                  ? 'ml-auto bg-blue-100 dark:bg-blue-900 max-w-[80%]' 
                  : 'mr-auto bg-gray-100 dark:bg-gray-800 max-w-[80%]'}`}
              >
                {msg.content}
              </div>
            ))}
          </div>
        </div>

        {/* 学习目标输入 */}
        <div className="bg-white dark:bg-gray-900 rounded-xl shadow p-6 mb-8">
          <Textarea
            value={learningGoal}
            onChange={(e) => setLearningGoal(e.target.value)}
            placeholder="请输入学习目标..."
            className="mb-4 min-h-[100px]"
          />
          <Button
            onClick={handleSubmit}
            disabled={isLoading}
            className="w-full"
          >
            {isLoading ? '生成中...' : '生成学习计划'}
          </Button>
        </div>

        {/* 题目控制器 */}
        {questions.length > 0 && (
          <div className="bg-white dark:bg-gray-900 rounded-xl shadow p-6">
            <h2 className="text-xl font-bold mb-4">学习测试</h2>
            <QuizController questions={questions} />
          </div>
        )}
      </div>
    </div>
  );
}