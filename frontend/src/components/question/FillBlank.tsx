'use client';
import { FillInTheBlankQuestion } from '@/types';
import { useState } from 'react';

type Props = {
  data: FillInTheBlankQuestion;
  onSubmit: (userAnswer: string, isCorrect: boolean) => void;
};

export default function FillInTheBlank({ data, onSubmit }: Props) {
  const [input, setInput] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);

  const handleSubmit = () => {
    const correct = input.trim().toLowerCase() === data.correctAnswer.toLowerCase();
    setIsCorrect(correct);
    setSubmitted(true);
    onSubmit(input, correct);
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <p className="font-medium mb-3">{data.question}</p>
      <div className="flex gap-2 mb-3">
        <input
          className="flex-1 border p-2 rounded"
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={submitted}
          placeholder="请输入你的答案"
        />
        <button
          className="bg-blue-500 text-white px-4 rounded"
          onClick={handleSubmit}
          disabled={submitted}
        >
          提交
        </button>
      </div>

      {submitted && (
        <div className={isCorrect ? 'text-green-600' : 'text-red-600'}>
          {isCorrect ? '回答正确！🎉' : `回答错误，正确答案是：${data.correctAnswer}`}
        </div>
      )}
    </div>
  );
}