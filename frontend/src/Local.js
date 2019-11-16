import React from 'react';
import { Layout, Menu, Drawer, message } from 'antd';

export default class Comp extends React.Component {
  render() {
    return (
      <div>
        <h1>local</h1>
      </div>
    );
  }

  componentDidMount = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8080');
      if (res.status === 200) {
        console.log(res);
      } else {
        message.warning(await res.text());
      }
    } catch (e) {
      message.error('Failed to connect local server');
    }
  }
}
