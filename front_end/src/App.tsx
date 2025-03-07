import React from 'react';
import './App.css';
import { Layout, Menu, theme } from 'antd';
import { Route,Routes, useNavigate } from 'react-router-dom';

import {
  MessageOutlined,
  ApartmentOutlined,
} from '@ant-design/icons'
import Chatbot from './components/chatbot/chatbot.tsx';
import FuzzyTree from './components/chatbot/fuzzyTree.tsx';
const {  Content, Sider } = Layout;

const items=[
  {
    key: '1',
    icon:<MessageOutlined />,
    label: 'Chatbot',
    description: 'Overview of the Fuzzy System',
    target:'/',
  },
  {
    key: '2',
    icon: <ApartmentOutlined />,
    label: 'Fuzzy Tree',
    description: 'Fuzzy Variables & Membership Functions of Sleep Quality',
    target:'/fuzzy-tree',
  }
  
];

function App() {

  const navigate = useNavigate();


  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const handleMenuClick = ({ key }:{key:any}) => {
    const { target } = items.find(item => item.key === key) || {};
    if (target) {
      navigate(target);
    }
  };
  return (
      <Layout className="App">
      <Sider
        theme='light'
        collapsible={false} collapsed={false}       
      >
        <Menu 
          style={{marginTop:50}} 
          theme="light" 
          mode="inline" 
          defaultSelectedKeys={['1']} 
          items={items} 
          selectable
          onClick={handleMenuClick}
        />
      </Sider>
      <Layout>
        <Content style={{ margin: '24px 16px 0' }}>
          <div
            style={{
              padding: 24,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <Routes>        
              <Route path="/"  element={<Chatbot/>} />     
              <Route path="/fuzzy-tree"  element={<FuzzyTree/>} />       
            </Routes>
          </div>
        </Content>
      </Layout>
    </Layout>
  );
}

export default App;
