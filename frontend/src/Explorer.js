import React from 'react';
import _ from 'lodash';
import Path from 'path';
import { Modal, Upload, Button, Input, Tree, Popconfirm, message } from 'antd';
import Navigator from './Navigator';

export default class Explorer extends React.Component {
  render() {
    return (
      <div className="horz" style={{minHeight: '100%'}}>
        <Navigator style={{flex: 1, minHeight: '100%'}}/>
        {this.renderPanel()}
      </div>
    );
  }

  renderPanel = () => {
    return (
      <div style={{flex: 1}}>
      </div>
    );
  }
}
