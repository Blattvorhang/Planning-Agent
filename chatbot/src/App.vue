<template>
  <div class="app-container">
    <!-- 左侧导航栏 -->
    <div class="sidebar">
      <h2 class="logo">ChatBot</h2>
      <nav class="menu">
        <a href="#">首页</a>
        <a href="#">聊天</a>
        <a href="#">设置</a>
      </nav>
    </div>

    <!-- 右侧聊天界面 -->
    <div class="chat-container">
      <div class="chat-box" ref="chatBox">
        <div
          v-for="(response, index) in responses"
          :key="index"
          :class="['message-block', response.sender]"
        >
          <div class="sender-name">
            {{ response.sender === 'user' ? '用户' : '机器人' }} - {{ response.time }}
          </div>
          <div class="message-bubble">
            {{ response.text }}
          </div>
        </div>
      </div>

      <div class="input-area">
        <input
          v-model="message"
          @keypress.enter="sendMessage"
          placeholder="请输入你的消息..."
        />
        <button @click="sendMessage">发送</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: '',
      responses: []
    };
  },
  methods: {
    getCurrentTime() {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      const hour = String(now.getHours()).padStart(2, '0');
      const minute = String(now.getMinutes()).padStart(2, '0');
      return `${year}/${month}/${day} ${hour}:${minute}`;
    },
    async sendMessage() {
      const trimmed = this.message.trim();
      if (!trimmed) return;

      const userMessage = {
        sender: 'user',
        text: trimmed,
        time: this.getCurrentTime()
      };
      this.responses.push(userMessage);
      this.$nextTick(() => this.scrollToBottom());

      try {
        const response = await axios.post('http://localhost:8000/chatbot/', { message: trimmed });
        const botMessage = {
          sender: 'bot',
          text: response.data.response,
          time: this.getCurrentTime()
        };
        this.responses.push(botMessage);
      } catch (error) {
        this.responses.push({
          sender: 'bot',
          text: '出错了，请稍后再试。',
          time: this.getCurrentTime()
        });
      }

      this.message = '';
      this.$nextTick(() => this.scrollToBottom());
    },
    scrollToBottom() {
      const box = this.$refs.chatBox;
      box.scrollTop = box.scrollHeight;
    }
  }
};
</script>

<style scoped>
/* 总容器 */
.app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
}

/* 左侧导航栏 */
.sidebar {
  width: 20%;
  background-color: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.logo {
  font-size: 24px;
  margin-bottom: 40px;
}

.menu {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.menu a {
  color: white;
  text-decoration: none;
  margin: 10px 0;
  padding: 10px;
  border-radius: 8px;
  text-align: center;
  transition: background-color 0.3s;
}

.menu a:hover {
  background-color: #34495e;
}

/* 右侧聊天界面 */
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f9f9f9;
}

.chat-box {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* 每条消息块 */
.message-block {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

/* 发送人名字+时间 */
.sender-name {
  font-size: 12px;
  color: #888;
  margin-bottom: 4px;
}

/* 聊天气泡 */
.message-bubble {
  max-width: 60%;
  padding: 12px 16px;
  border-radius: 18px;
  word-wrap: break-word;
  line-height: 1.4;
}

/* 用户消息靠右 */
.message-block.user {
  align-items: flex-end;
}

.message-block.user .message-bubble {
  background-color: #d1eaff;
  text-align: right;
}

/* 机器人消息靠左 */
.message-block.bot {
  align-items: flex-start;
}

.message-block.bot .message-bubble {
  background-color: #e6e6e6;
}

/* 底部输入框 */
.input-area {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
  background-color: #fff;
}

.input-area input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  outline: none;
}

.input-area button {
  margin-left: 10px;
  padding: 10px 16px;
  font-size: 16px;
  border: none;
  background-color: #42b983;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.input-area button:hover {
  background-color: #369f75;
}
</style>
