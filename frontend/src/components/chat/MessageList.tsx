import ReactMarkdown from 'react-markdown';
import { Message } from '@/types/index';

type Props = {
  messages: Message[];
};

export default function MessageList({ messages }: Props) {
  return (
    <div className="space-y-4 mb-4 max-h-[calc(100vh-200px)] overflow-y-auto">
      {messages.map(msg => (
        <div 
          key={msg.id} 
          className={`p-4 rounded-lg max-w-[80%] ${msg.role === 'user' 
            ? 'ml-auto bg-blue-100 text-blue-900' 
            : 'mr-auto bg-gray-100 text-gray-900'}`}
        >
          <ReactMarkdown className="prose text-sm">{msg.content}</ReactMarkdown>
          {msg.createdAt && (
            <div className="text-xs mt-1 text-gray-500">
              {new Date(msg.createdAt).toLocaleTimeString()}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}