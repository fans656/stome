import React from 'react';
import App from '../src/App';
import Local from '../src/Local';

export default class Comp extends React.Component {
  render() {
    return (
      <App page="local"><Local/></App>
    );
  }
}
