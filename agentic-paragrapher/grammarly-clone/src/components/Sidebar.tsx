import type React from 'react'
import { useState } from 'react'
import SuggestionCard from './SuggestionCard'

interface Suggestion {
  id: string
  type: 'spelling' | 'grammar' | 'clarity'
  title: string
  description: string
  originalWord: string
  replacement: string
}

interface SidebarProps {
  suggestions: Suggestion[]
  onAcceptSuggestion: (suggestion: Suggestion) => void
  onDismissSuggestion: (id: string) => void
}

const Sidebar: React.FC<SidebarProps> = ({
  suggestions,
  onAcceptSuggestion,
  onDismissSuggestion
}) => {
  const [activeTab, setActiveTab] = useState<'review' | 'ai' | 'plagiarism'>('review')

  const tabs = [
    { id: 'review', label: 'Review suggestions', active: true },
    { id: 'ai', label: 'Write with AI', active: false },
    { id: 'plagiarism', label: 'Check for AI text & plagiarism', active: false }
  ]

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Tab header */}
      <div className="border-b border-gray-200 bg-white">
        <div className="flex overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as 'review' | 'ai' | 'plagiarism')}
              className={`px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${activeTab === tab.id
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab content */}
      <div className="flex-1 overflow-y-auto">
        {activeTab === 'review' && (
          <div className="p-4">
            {suggestions.length === 0 ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Great writing!</h3>
                <p className="text-gray-500">No suggestions found. Keep writing to get feedback.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {suggestions.map((suggestion) => (
                  <SuggestionCard
                    key={suggestion.id}
                    suggestion={suggestion}
                    onAccept={() => onAcceptSuggestion(suggestion)}
                    onDismiss={() => onDismissSuggestion(suggestion.id)}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'ai' && (
          <div className="p-4">
            <div className="text-center py-12">
              <div className="w-16 h-16 mx-auto mb-4 bg-blue-100 rounded-full flex items-center justify-center">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">AI Writing Assistant</h3>
              <p className="text-gray-500">AI features coming soon...</p>
            </div>
          </div>
        )}

        {activeTab === 'plagiarism' && (
          <div className="p-4">
            <div className="text-center py-12">
              <div className="w-16 h-16 mx-auto mb-4 bg-purple-100 rounded-full flex items-center justify-center">
                <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Plagiarism Check</h3>
              <p className="text-gray-500">Plagiarism detection coming soon...</p>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-gray-200 bg-white p-4">
        <button className="w-full text-left text-sm text-blue-600 hover:text-blue-800 flex items-center space-x-2">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Check for plagiarism and AI text</span>
        </button>
      </div>
    </div>
  )
}

export default Sidebar
