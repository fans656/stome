import React from 'react';
import { Modal, Upload, Button, Input, Tree, Popconfirm, message } from 'antd';

export default class Navigator extends React.Component {
  render() {
    return (
      <div className="horz" style={this.props.style || {}}>
        {this.renderNav()}
        {this.renderPanel()}
      </div>
    );
  }

  renderNav = () => {
    return (
      <div className="vert stretch" style={{flex: 1}}>
        <NavActions/>
        <NavList/>
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

class NavActions extends React.Component {
  render() {
    return (
      <Input.Group className="horz">
        <Button title="Current directory">.</Button>
        <Button title="Parent directory">.. </Button>
        <Input className="mono"
          style={{flex: 1}}
        />
        <Popconfirm
          title="Are you sure to delete?"
          onConfirm={this.onDelete}
          okText="Delete"
        >
          <Button icon="delete" title="Delete"/>
        </Popconfirm>
        <Button icon="swap" title="Move (edit path as target)"
        />
        <Button icon="folder-add" title="New directory (edit path as target)"
        />
        <Button icon="edit" title="Rename"
        />
        <Button icon="upload" title="Upload"
        />
        <input ref={this.fileInput}
          type="file"
          style={{display: 'none'}}
          multiple
        />
      </Input.Group>
    );
    // old
    return (
      <Input.Group className="horz">
        <Button title="Current directory" onClick={this.onCurrentDirectory}>.</Button>
        <Button title="Parent directory" onClick={this.filesystem.cdUp}>.. </Button>
        <Input className="mono"
          value={this.state.currentPath}
          onChange={ev => this.setState({currentPath: ev.target.value})}
          onPressEnter={() => this.filesystem.cd(this.state.currentPath)}
          style={{flex: 1}}
        />
        <Popconfirm
          title="Are you sure to delete?"
          onConfirm={this.onDelete}
          okText="Delete"
        >
          <Button icon="delete" title="Delete" disabled={!this.selected()}/>
        </Popconfirm>
        <Button icon="swap" title="Move (edit path as target)"
          disabled={!this.selected() || this.state.currentPath === this.filesystem.currentPath}
          onClick={this.onMove}
        />
        <Button icon="folder-add" title="New directory (edit path as target)"
          disabled={this.state.currentPath === this.filesystem.currentPath}
          onClick={this.onNewDirectory}
        />
        <Button icon="edit" title="Rename" disabled={!this.singleSelected()}
          onClick={() => this.setState({
            renameModalVisible: true,
            renameModalNewName: Path.basename(this.state.selectedPaths[0]),
          })}
        />
        <Button icon="upload" title="Upload"
          onClick={() => this.fileInput.current.click()}
        />
        <input ref={this.fileInput}
          type="file"
          style={{display: 'none'}}
          multiple
          onChange={ev => {
            getTransferManager().uploadFiles(this.state.currentPath, ev.target.files);
            this.fileInput.current.value = null;
          }}
        />
      </Input.Group>
    );
  }
}

class NavList extends React.Component {
  state = {
    nodes: [],
    currentPath: '/',
  }

  render() {
    const nodes = this.state.nodes;
    const nodeComps = nodes.map(node => (
      <Tree.TreeNode
        title={node.name}
        key={node.path}
        isLeaf={node.type !== 'dir'}
      >
      </Tree.TreeNode>
    ));
    return (
      <Tree.DirectoryTree
        key={this.state.currentPath}
        multiple
        blockNode={true}
        expandAction="doubleClick"
        dataSource={this.state.nodes}
        selectedKeys={this.state.selectedPaths}
        onSelect={this.onSelect}
        onExpand={this.onExpand}
      >
        {nodeComps}
      </Tree.DirectoryTree>
    );
  }
}

