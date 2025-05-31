import React, { useState } from 'react';

function Editor() {
  const [text, setText] = useState('');

  const checkGrammar = (text) => {
    // Placeholder: underline words longer than 15 characters
    return text.split(' ').map(word => word.length > 15 ? `<u>${word}</u>` : word).join(' ');
  };

  return (
    <div className="flex-1 bg-white p-5">
      <div
        contentEditable
        className="outline-none"
        onInput={(e) => setText(e.currentTarget.textContent)}
        dangerouslySetInnerHTML={{ __html: checkGrammar(text) }}
      />
    </div>
  );
}

export default Editor; 