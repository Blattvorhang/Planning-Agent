'use client';
import { useState } from 'react';
import { MultipleChoiceQuestion, FillInTheBlankQuestion } from '@/types';
import MultipleChoice from '@/components/question/MultipleChoice';
import FillInTheBlank from '@/components/question/FillBlank';

type Question = MultipleChoiceQuestion | FillInTheBlankQuestion;

type Props = {
    questions: Question[];
};

export default function QuizController({ questions }: Props) {
    const [current, setCurrent] = useState(0);
    const [answered, setAnswered] = useState(false);
    const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
    const [userAnswer, setUserAnswer] = useState<string | null>(null);

    const currentQuestion = questions[current];

    const handleSelectChoice = (selectedId: string, correct: boolean) => {
        setUserAnswer(selectedId);
        setIsCorrect(correct);
        setAnswered(true);
    };

    const handleSubmitBlank = (userAnswer: string, correct: boolean) => {
        setUserAnswer(userAnswer);
        setIsCorrect(correct);
        setAnswered(true);
    };

    const handleNext = () => {
        setAnswered(false);
        setIsCorrect(null);
        setUserAnswer(null);
        setCurrent((prev) => prev + 1);
    };

    return (
        <div className="max-w-xl mx-auto mt-8">
            {currentQuestion ? (
                <>
                    {currentQuestion.hasOwnProperty('options') ? (
                        <MultipleChoice
                            data={currentQuestion as MultipleChoiceQuestion}
                            onSelect={handleSelectChoice}
                        />
                    ) : (
                        <FillInTheBlank
                            data={currentQuestion as FillInTheBlankQuestion}
                            onSubmit={handleSubmitBlank}
                        />
                    )}

                    {answered && (
                        <div className="mt-4 flex justify-between items-center">
                            <p className={isCorrect ? 'text-green-600' : 'text-red-600'}>
                                {isCorrect ? (
                                    '回答正确！🎉'
                                ) : (
                                    <>
                                        回答错误，正确答案是：
                                        {('correctAnswer' in currentQuestion)
                                            ? currentQuestion.correctAnswer
                                            : currentQuestion.options.find(
                                                option => option.id === currentQuestion.correctId
                                            )?.label}
                                    </>
                                )}
                            </p>
                            <button
                                className="px-4 py-2 bg-blue-500 text-white rounded"
                                onClick={handleNext}
                            >
                                下一题
                            </button>
                        </div>
                    )}
                </>
            ) : (
                <p className="text-center text-lg mt-10">你已经完成所有题目！🎉</p>
            )}
        </div>
    );
}