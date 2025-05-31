import React from 'react';
import Sidebar from './Sidebar';
import Editor from './Editor';
import Toolbar from './Toolbar';

function App() {
  return (
    <div className="flex flex-col h-screen">
      <Toolbar />
      <div className="flex flex-1">
        <Sidebar />
        <Editor />
      </div>
    </div>
  );
}

export default App; 