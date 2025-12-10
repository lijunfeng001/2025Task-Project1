import json
import datetime

class SimpleChatBot:
    def __init__(self):
        """初始化聊天机器人"""
        self.user_name = "朋友"  
        self.bot_name = "小智"   
        self.history_file = "chat_history.txt"  
        self.chat_history = []  
        
       
        self.load_history()
        
        print(f"你好！我是{self.bot_name}，一个简单的聊天机器人。")
        print("我可以：1.和你聊天 2.告诉你时间 3.记住我们的对话 4.简单计算 5.查询天气")
    
    def load_history(self):
        """加载之前的聊天记录"""
        try:
           
            with open(self.history_file, 'r', encoding='utf-8') as f:
                
                lines = f.readlines()
                self.chat_history = [line.strip() for line in lines if line.strip()]
                print(f"读取了 {len(self.chat_history)} 条历史记录")
        except:
          
            print("这是我们的第一次对话！")
            self.chat_history = []
    
    def save_history(self):
        """保存聊天记录到文件"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                for line in self.chat_history:
                    f.write(line + '\n')
        except:
            print("保存记录时出错了，但我们可以继续聊天")
    
    def add_to_history(self, speaker, message):
        """把一句话添加到历史记录"""
        
        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M")
        record = f"[{time_str}] {speaker}: {message}"
        self.chat_history.append(record)
        
        
        if len(self.chat_history) > 50:
            self.chat_history = self.chat_history[-50:]
        
        
        self.save_history()
    
    def get_current_time(self):
        """获取当前时间"""
        now = datetime.datetime.now()
        
      
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        weekday = weekdays[now.weekday()]
        
        return f"今天是{now.year}年{now.month}月{now.day}日 星期{weekday} {now.hour:02d}:{now.minute:02d}"
    
    def simple_calculate(self, text):
        """做简单的数学计算"""
        try:
            
            text = text.replace("加", "+")
            text = text.replace("减", "-")
            text = text.replace("乘", "*")
            text = text.replace("除以", "/")
            text = text.replace("除", "/")
            
       
            for word in ["计算", "算一下", "等于多少", "="]:
                text = text.replace(word, "")
            
           
            text = text.replace(" ", "")
            
           
            safe_chars = "0123456789+-*/(). "
            for char in text:
                if char not in safe_chars:
                    return "抱歉，我只能计算简单的加减乘除哦"
            
           
            result = eval(text)
            return f"{text} = {result}"
            
        except:
            return "抱歉，我没算出来，请换一个简单点的算式"
    
    def get_weather(self, city="北京"):
        """获取天气信息（简化版）"""
       
        weather_data = {
            "北京": "🌤️ 晴天，15-25°C，适合外出",
            "上海": "☁️ 多云，18-26°C，微风",
            "广州": "🌧️ 阵雨，24-30°C，记得带伞",
            "深圳": "⛅ 阴天，23-29°C，湿度较高",
            "杭州": "🌤️ 晴天，16-24°C，空气质量良"
        }
        
       
        for known_city in weather_data:
            if known_city in city or city in known_city:
                return weather_data[known_city]
        
        
        return f"🌤️ {city}天气：晴间多云，20-28°C（示例数据）"
    
    def show_history(self):
        """显示聊天历史"""
        if not self.chat_history:
            return "我们还没有聊过天呢！"
        
       
        recent = self.chat_history[-10:]
        result = "最近的聊天记录：\n"
        result += "-" * 30 + "\n"
        
        for record in recent:
            result += record + "\n"
        
        result += "-" * 30
        return result
    
    def get_response(self, user_input):
        """根据用户输入生成回复"""
        
    
        input_lower = user_input.lower()
        
      
        
        # 1. 退出命令
        if input_lower in ["退出", "exit", "quit", "bye", "再见"]:
            return "exit", f"再见{self.user_name}！记得常来找我聊天哦～"
        
        # 2. 时间命令
        if input_lower in ["时间", "现在几点", "今天几号", "日期"]:
            return "normal", self.get_current_time()
        
        # 3. 天气命令
        if "天气" in input_lower:
            # 提取城市名
            city = "北京"  # 默认
            for c in ["北京", "上海", "广州", "深圳", "杭州"]:
                if c in user_input:
                    city = c
                    break
            return "normal", self.get_weather(city)
        
        # 4. 计算命令
        if any(word in input_lower for word in ["计算", "算一下", "+", "-", "*", "/"]):
            return "normal", self.simple_calculate(user_input)
        
        # 5. 历史命令
        if input_lower in ["历史", "聊天记录", "记录", "history"]:
            return "normal", self.show_history()
        
        # 6. 帮助命令
        if input_lower in ["帮助", "help", "功能", "你会什么"]:
            help_text = """
========== 我可以做的 ==========
1. 聊天：随便和我聊聊吧！
2. 时间：输入"时间"或"现在几点"
3. 天气：输入"天气"或"天气 上海"
4. 计算：输入"计算 15+8"或"15+8等于多少"
5. 历史：输入"历史"查看聊天记录
6. 退出：输入"退出"结束聊天
==============================
            """
            return "normal", help_text
        
        # 7. 问候语
        if any(word in input_lower for word in ["你好", "嗨", "hello", "hi"]):
            responses = [
                f"你好呀{self.user_name}！今天过得怎么样？",
                f"嗨{self.user_name}！很高兴见到你！",
                f"{self.user_name}你好！有什么我可以帮你的吗？"
            ]
            import random
            return "normal", random.choice(responses)
        
        # 8. 感谢
        if any(word in input_lower for word in ["谢谢", "感谢", "thank"]):
            return "normal", "不客气！我很乐意帮助你～"
        
        
        responses = [
            "真有趣！能多说一点吗？",
            "我明白了，继续说吧。",
            "这个我不太懂，但我很愿意学习！",
            f"{self.user_name}，你今天心情怎么样？",
            "说到这个，让我想起我们可以聊聊天气或者时间。",
            "我还在学习如何更好地聊天，请多包涵～",
            "嗯，有道理！",
            "然后呢？我在认真听哦。"
        ]
        
        import random
        return "normal", random.choice(responses)
    
    def run(self):
        """运行聊天程序"""
      
        name = input(f"{self.bot_name}: 请问你叫什么名字？ ")
        if name.strip():
            self.user_name = name.strip()
        
        print(f"{self.bot_name}: 很高兴认识你，{self.user_name}！")
        print(f"{self.bot_name}: 输入'帮助'查看我能做什么，输入'退出'结束聊天")
        print("=" * 50)
        
        
        while True:
            try:
                
                user_input = input(f"{self.user_name}: ").strip()
                
                
                if not user_input:
                    continue
                
                
                self.add_to_history(self.user_name, user_input)
                
            
                response_type, bot_response = self.get_response(user_input)
                
                
                if response_type == "exit":
                    print(f"{self.bot_name}: {bot_response}")
                    self.add_to_history(self.bot_name, bot_response)
                    break
                
                
                print(f"{self.bot_name}: {bot_response}")
                self.add_to_history(self.bot_name, bot_response)
                
            except KeyboardInterrupt:
               
                print(f"\n{self.bot_name}: 好的，我们下次再聊！")
                break
            except Exception as e:
                
                print(f"{self.bot_name}: 哎呀，出错了: {e}")
                print(f"{self.bot_name}: 我们继续聊天吧！")
        
        
        self.save_history()
        print(f"{self.bot_name}: 聊天记录已保存到 {self.history_file}")


if __name__ == "__main__":
    print("正在启动聊天机器人...")
    print("-" * 50)
   
    bot = SimpleChatBot()
    bot.run()
第一步：准备文件

1. 创建一个新文件夹，比如叫 my_chatbot
2. 在文件夹里创建一个新文件，命名为 simple_chat.py
3. 把上面的代码复制到文件里

第二步：运行程序

1. 打开命令行（Windows按Win+R，输入cmd，回车）
2. 进入你的文件夹：
   ```
   cd 你的文件夹路径
   ```
   例如：cd C:\Users\你的名字\Desktop\my_chatbot
3. 运行程序：
   ```
   python simple_chat.py
   ```
   如果提示"python不是命令"：
   · 试试 python3 simple_chat.py
   · 或者安装Python：去官网 https://www.python.org 下载安装

第三步：开始聊天

程序启动后：

```
正在启动聊天机器人...
--------------------------------------------------
你好！我是小智，一个简单的聊天机器人。
我可以：1.和你聊天 2.告诉你时间 3.记住我们的对话 4.简单计算 5.查询天气
小智: 请问你叫什么名字？
```

输入你的名字，然后就可以开始聊天了！

第四步：试试这些命令

```
你: 你好
小智: 你好呀张三！今天过得怎么样？

你: 时间
小智: 今天是2024年12月9日 星期一 14:30

你: 天气上海
小智: ☁️ 上海天气：多云，18-26°C，微风

你: 计算 15+8*2
小智: 15+8*2 = 31
