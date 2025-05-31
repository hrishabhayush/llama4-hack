import React from 'react';

function Sidebar() {
  return (
    <div className="w-72 bg-gray-100 p-4 overflow-y-auto">
      <h2 className="text-lg font-bold mb-4">Suggestions</h2>
      {/* Example suggestion card */}
      <div className="bg-white shadow p-2 mb-2">
        <p>It looks like 'demonstrativelylongword' might be too long or misspelled—consider revising.</p>
        <button className="mt-2 bg-blue-500 text-white px-2 py-1 rounded">Apply</button>
      </div>
    </div>
  );
}

export default Sidebar; 