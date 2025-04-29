1. 安装nodejs和npm
https://blog.csdn.net/WHF__/article/details/129362462
可能需要保持版本一直
我的是:
nodejs：v18.18.2
npm:9.8.1

2. vscode安装插件Vue Language Features

不知道你们直接运行我这个代码行不行
如果不行的话执行以下步骤

3. npm install

如果还不行就只能自己重新创一个项目，然后把我app.vue里的内容复制过去
从头创建项目的步骤如下：

1. 新建一个文件夹

2. 运行npm init vue@latest
勾选router其他不选

3. cd 刚刚创建的文件夹

4. 运行npm install 

5. 之后运行npm run dev启动项目

如果启动项目之后出现devtool影响页面，可以复制我的vite.config.js