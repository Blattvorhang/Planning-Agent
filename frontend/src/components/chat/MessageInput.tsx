import { useState } from 'react';

type Props = {
  onSend: (text: string) => void;
  isLoading: boolean;
};

export default function MessageInput({ onSend, isLoading }: Props) {
  const [text, setText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim() && !isLoading) {
      onSend(text);
      setText('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        className="flex-1 border rounded p-2"
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="输入消息..."
        disabled={isLoading}
      />
      <button 
        type="submit" 
        className="bg-blue-500 text-white px-4 rounded disabled:opacity-50"
        disabled={isLoading}
      >
        {isLoading ? '发送中...' : '发送'}
      </button>
    </form>
  );
}