import React, { use, useEffect, useState } from "react";
import { Layout, Card, Input, Button, List, Typography,Spin } from "antd";
import { LoadingOutlined } from '@ant-design/icons';
const { Header, Content, Footer } = Layout;
const { Text } = Typography;

interface Message {
  role: "user" | "bot";
  content: string;
}


export default function Chatbot() {

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    localStorage.setItem("message",  input);
    setLoading(true);
    setMessages([...messages, userMessage]);
    const options: RequestInit = {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: input }),
    };
    const response = await fetch('http://127.0.0.1:8000/api/convo/chat_agent/', options);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Error: ${response.status} - ${errorText}`);
    }else{
      const responseData = await response.json();
      console.log(responseData);

      localStorage.setItem("tree", JSON.stringify(responseData.tree));
      localStorage.setItem("reply",  responseData.result);


      const botMessage: Message = { role: "bot", content: responseData.result};
      setMessages((prev) => [...prev, botMessage]);

      setInput("");
      setLoading(false);

    }

    

    
  };

  useEffect(() => {
    const message = localStorage.getItem("message");
    const reply = localStorage.getItem("reply");

    if (message && reply) {
      const userMessage: Message = { role: "user", content: message };
      const botMessage: Message = { role: "bot", content: reply };

      setMessages([...messages, ...[userMessage,botMessage]]);
    }
  }, []);

  return (
    <div style={{ minHeight: "100vh"}}>
 

      <Input.Group compact style={{ width: 400 }}>
        <Input
          style={{ width: "80%" }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onPressEnter={sendMessage}
          placeholder="Type a message..."
        />
        <Button type="primary" onClick={sendMessage}>
          Send
        </Button>
      </Input.Group>
    <Content style={{ paddingTop: "20px", display: "flex" }}>
      <Card style={{ width: 400, height: "70vh", overflow: "auto" }}>
        <List
          dataSource={messages}
          renderItem={(msg, index) => (
            <List.Item key={index} style={{ textAlign: msg.role === "user" ? "right" : "left" }}>
              <Text strong={msg.role === "user"}>{msg.content}</Text>
            </List.Item>
          )}
        />
        <Spin fullscreen spinning={loading} indicator={<LoadingOutlined spin />} size="large" />
      </Card>
    </Content>

  </div>
  )
}
