import { MultipleChoiceQuestion } from '@/types';
import { useState } from 'react';

type Props = {
  data: MultipleChoiceQuestion;
  onSelect: (optionId: string, isCorrect: boolean) => void;
};

export default function MultipleChoice({ data, onSelect }: Props) {
  const [selected, setSelected] = useState<string | null>(null);
  const [showAnswer, setShowAnswer] = useState(false);

  const handleClick = (id: string) => {
    if (showAnswer) return; // 防止重复选择
    setSelected(id);
    setShowAnswer(true);
    const isCorrect = id === data.correct_answer;
    onSelect(id, isCorrect);
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <p className="font-medium mb-3">{data.question}</p>
      <ul className="space-y-2">
        {data.options.map(option => {
          const isSelected = selected === option.id;
          const isCorrect = option.id === data.correct_answer;

          let bgClass = '';
          if (showAnswer) {
            if (isCorrect) bgClass = 'bg-green-100 border-green-500';
            else if (isSelected) bgClass = 'bg-red-100 border-red-500';
            else bgClass = 'bg-gray-50';
          } else if (isSelected) {
            bgClass = 'bg-blue-100 border-blue-500';
          }

          return (
            <li
              key={option.id}
              onClick={() => handleClick(option.id)}
              className={`cursor-pointer p-2 border rounded ${bgClass}`}
            >
              {option.label}
            </li>
          );
        })}
      </ul>
    </div>
  );
}