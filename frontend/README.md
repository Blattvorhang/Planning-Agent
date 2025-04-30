# AI Learning Planner Frontend

这是AI学习规划助手的前端项目，使用React + Next.js + Tailwind CSS + shadcn/ui构建。

## 开发环境要求

- Node.js 18.0.0 或更高版本
- npm 9.0.0 或更高版本

## 安装依赖

```bash
cd frontend
npm install
```

## 开发运行

```bash
npm run dev
```

默认情况下，开发服务器将在 http://localhost:3000 启动。

## 构建生产版本

```bash
npm run build
npm start
```

## 项目结构

```
frontend/
├── src/
│   ├── app/              # Next.js 应用页面
│   ├── components/       # UI组件
│   ├── hooks/           # 自定义Hooks
│   ├── lib/             # 工具函数
│   └── types/           # TypeScript类型定义
├── public/              # 静态资源
└── package.json         # 项目配置文件
```

## 后端API

后端API服务运行在 http://localhost:8000，前端项目已配置代理，可以直接使用相对路径（如 `/api/learn`）访问后端接口。 