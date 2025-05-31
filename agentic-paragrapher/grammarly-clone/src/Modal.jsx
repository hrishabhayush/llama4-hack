import React from 'react';

function Modal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded shadow-lg w-96">
        <h2 className="text-lg font-bold mb-4">Generate Paragraph</h2>
        <input type="text" placeholder="Topic or Prompt" className="w-full mb-4 p-2 border" />
        <div className="flex space-x-2 mb-4">
          <select className="flex-1 p-2 border">
            <option>Tone: Formal</option>
            <option>Tone: Informal</option>
            <option>Tone: Conversational</option>
          </select>
          <select className="flex-1 p-2 border">
            <option>Length: Short</option>
            <option>Length: Medium</option>
            <option>Length: Long</option>
          </select>
        </div>
        <div className="flex justify-end space-x-2">
          <button onClick={onClose} className="bg-gray-300 px-4 py-2 rounded">Cancel</button>
          <button onClick={onClose} className="bg-blue-500 text-white px-4 py-2 rounded">Generate</button>
        </div>
      </div>
    </div>
  );
}

export default Modal; 