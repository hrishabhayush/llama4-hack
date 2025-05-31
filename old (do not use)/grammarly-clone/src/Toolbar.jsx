import React from 'react';

function Toolbar() {
  return (
    <div className="flex items-center justify-between h-16 bg-white border-b border-gray-200 px-4">
      <div className="text-xl font-bold">Agentic Paragrapher</div>
      <div className="flex space-x-4">
        <button className="flex items-center space-x-1">
          <span>Generate Paragraph</span>
          {/* Placeholder for magic wand icon */}
        </button>
        <button className="flex items-center space-x-1">
          <span>Save</span>
          {/* Placeholder for disc icon */}
        </button>
        <button className="flex items-center space-x-1">
          <span>Settings</span>
          {/* Placeholder for gear icon */}
        </button>
      </div>
    </div>
  );
}

export default Toolbar; 