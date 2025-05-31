import React, { useState } from 'react';

function App() {
  const [activeTab, setActiveTab] = useState('suggestions');
  const [promptText, setPromptText] = useState('');
  const [editorContent, setEditorContent] = useState(`Welcome to your modern text editor! This is a sample paragraph to demonstrate the interface. 

You can type here and see how the layout works. The left sidebar is for AI prompting, and the right sidebar shows review suggestions and other tools.

Start writing your content here...`);

  return (
    <div className="min-h-screen bg-editor-bg font-sans">
      {/* Fixed Header */}
      <header className="fixed top-0 left-0 right-0 h-15 bg-white border-b border-border-light shadow-sm z-50">
        <div className="h-full flex items-center justify-between px-6">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">TE</span>
            </div>
            <span className="font-semibold text-text-primary">TextEditor</span>
          </div>

          {/* Document Title */}
          <div className="flex-1 flex justify-center">
            <h1 className="text-lg font-medium text-text-primary">Untitled Document</h1>
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-4">
            <button className="px-4 py-2 text-sm font-medium text-text-secondary hover:text-text-primary transition-colors">
              Goals
            </button>
            <button className="px-4 py-2 text-sm font-medium text-text-secondary hover:text-text-primary transition-colors">
              Score
            </button>
            <div className="w-px h-6 bg-border-light"></div>
            <button className="px-4 py-2 bg-accent-blue text-white text-sm font-medium rounded-lg hover:bg-blue-600 transition-colors">
              Share
            </button>
          </div>
        </div>
      </header>

      {/* Main Layout */}
      <div className="pt-16 flex h-screen">
        {/* Left Sidebar - Chat Box */}
        <div className="w-72 bg-sidebar-bg border-r border-border-light shadow-sm h-[calc(100vh-60px)]">
          <div className="flex flex-col h-full p-4">
            <textarea
              value={promptText}
              onChange={(e) => setPromptText(e.target.value)}
              placeholder="Ask the AI to help with your writing..."
              className="flex-1 mb-4 p-3 text-sm border border-border-light rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent"
            />
            <button
              className="w-full px-4 py-2 bg-accent-blue text-white text-sm font-medium rounded-lg hover:bg-blue-600 transition-colors"
              onClick={() => {
                /* placeholder: send prompt to LLM later */
                console.log('Sending prompt:', promptText);
              }}
            >
              Send Prompt
            </button>
          </div>
        </div>

        {/* Main Content Area - Rich Text Editor */}
        <div className="flex-1 bg-white flex flex-col">
          <div
            className="editor-content flex-1 overflow-auto p-6"
            contentEditable
            suppressContentEditableWarning={true}
            onInput={(e) => setEditorContent(e.target.innerText)}
          >
            {editorContent}
          </div>
          {/*
            If you need a bottom toolbar later, you can put it here:
            <div className="h-16 border-t">…toolbar…</div>
          */}
        </div>

        {/* Right Sidebar - Review Suggestions */}
        <div className="w-75 bg-sidebar-bg border-l border-border-light shadow-sm h-[calc(100vh-60px)]">
          {/* Tab Navigation */}
          <div className="border-b border-border-light">
            <div className="flex">
              <button
                onClick={() => setActiveTab('suggestions')}
                className={`flex-1 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${activeTab === 'suggestions'
                  ? 'border-accent-blue text-accent-blue'
                  : 'border-transparent text-text-secondary hover:text-text-primary'
                  }`}
              >
                Suggestions
              </button>
              <button
                onClick={() => setActiveTab('review')}
                className={`flex-1 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${activeTab === 'review'
                  ? 'border-accent-blue text-accent-blue'
                  : 'border-transparent text-text-secondary hover:text-text-primary'
                  }`}
              >
                Review
              </button>
            </div>
          </div>

          {/* Tab Content */}
          <div className="p-4 h-full overflow-auto">
            {activeTab === 'suggestions' && (
              <div className="space-y-4">
                <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                  <div className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-accent-red rounded-full mt-2 flex-shrink-0"></div>
                    <div>
                      <p className="text-sm font-medium text-red-800">Grammar Error</p>
                      <p className="text-xs text-red-600 mt-1">Consider changing "demonstrate" to "demonstrates"</p>
                      <button className="text-xs text-accent-blue hover:underline mt-2">Apply fix</button>
                    </div>
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                  <div className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-accent-blue rounded-full mt-2 flex-shrink-0"></div>
                    <div>
                      <p className="text-sm font-medium text-blue-800">Clarity</p>
                      <p className="text-xs text-blue-600 mt-1">This sentence could be clearer. Consider breaking it into two sentences.</p>
                      <button className="text-xs text-accent-blue hover:underline mt-2">View suggestion</button>
                    </div>
                  </div>
                </div>

                <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                  <div className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                    <div>
                      <p className="text-sm font-medium text-green-800">Enhancement</p>
                      <p className="text-xs text-green-600 mt-1">Consider using "utilize" instead of "use" for a more formal tone.</p>
                      <button className="text-xs text-accent-blue hover:underline mt-2">Apply suggestion</button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'review' && (
              <div className="space-y-4">
                <div className="text-center py-8">
                  <div className="w-16 h-16 bg-gray-100 rounded-full mx-auto flex items-center justify-center mb-4">
                    <span className="text-2xl">📋</span>
                  </div>
                  <h3 className="text-sm font-medium text-text-primary mb-2">Document Review</h3>
                  <p className="text-xs text-text-secondary">Review features coming soon...</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 