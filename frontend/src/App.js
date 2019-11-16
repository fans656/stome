import React from 'react';
import { Layout, Menu, Drawer, message } from 'antd';
import 'antd/dist/antd.min.css';
import Explorer from './Explorer';
import './App.css';

export default class App extends React.Component {
  render() {
    return (
      <Layout style={{minHeight: '100%'}}>
        {this.renderHeader()}
        {this.renderExplorer()}
      </Layout>
    );
  }

  renderHeader = () => {
    return (
      <Layout.Header style={{height: '45px', paddingLeft: 0}}>
        <Menu
          theme="dark"
          mode="horizontal"
          style={{display: 'flex', lineHeight: '40px', padding: 0}}
          selectedKeys={[]}
        >
          <Menu.Item>
            <span className="logo">Stome</span>
          </Menu.Item>
        </Menu>
      </Layout.Header>
    );
  }

  renderExplorer = () => {
    return (
      <Layout.Content className="layout-content">
        <Explorer/>
      </Layout.Content>
    );
  }
}
