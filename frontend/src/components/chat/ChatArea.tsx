import { useState } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { Message } from '@/types/index';

export default function ChatArea() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (text: string) => {
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
    };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: text }),
      });

      if (!response.ok) throw new Error('请求失败');
      
      const data = await response.json();
      setMessages(prev => [...prev, {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: data.reply,
      }]);
    } catch (error) {
      console.error('请求出错:', error);
      setMessages(prev => [...prev, {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: '抱歉，请求过程中出现错误',
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white shadow p-4 rounded-md">
      <MessageList messages={messages} />
      <MessageInput onSend={handleSend} isLoading={isLoading} />
    </div>
  );
}