// Instructions: Create the main App component with header and two-pane layout structure

import React, { useState } from 'react'
import Header from './components/Header'
import Editor from './components/Editor'
import Sidebar from './components/Sidebar'

interface Suggestion {
  id: string
  type: 'spelling' | 'grammar' | 'clarity'
  title: string
  description: string
  originalWord: string
  replacement: string
}

function App() {
  const [suggestions, setSuggestions] = useState<Suggestion[]>([])
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  const addSuggestion = (originalWord: string) => {
    const newSuggestion: Suggestion = {
      id: `suggestion-${Date.now()}`,
      type: 'spelling',
      title: 'Correct your spelling',
      description: `Did you mean '${originalWord.replace(/(.{4})(.+)(.{4})/, '$1-$2-$3')}'?`,
      originalWord,
      replacement: originalWord.replace(/(.{4})(.+)(.{4})/, '$1-$2-$3')
    }

    setSuggestions(prev => [...prev, newSuggestion])
  }

  const removeSuggestion = (id: string) => {
    setSuggestions(prev => prev.filter(s => s.id !== id))
  }

  const acceptSuggestion = (suggestion: Suggestion) => {
    // This would replace the word in the editor
    // For now, just remove the suggestion
    removeSuggestion(suggestion.id)
  }

  return (
    <div className="h-screen flex flex-col bg-white font-inter">
      <Header
        isSidebarCollapsed={isSidebarCollapsed}
        onToggleSidebar={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        onToggleMobileMenu={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      />

      <div className="flex-1 flex overflow-hidden">
        <div
          className={`flex-1 transition-all duration-300 ${isSidebarCollapsed ? 'mr-0' : 'mr-0 md:mr-96'
            }`}
        >
          <Editor onAddSuggestion={addSuggestion} />
        </div>

        <div
          className={`fixed right-0 top-16 bottom-0 w-96 bg-gray-50 border-l border-gray-200 transition-transform duration-300 z-20 ${isSidebarCollapsed ? 'translate-x-full' : 'translate-x-0'
            } md:translate-x-0 ${isMobileMenuOpen ? 'translate-x-0' : 'translate-x-full md:translate-x-0'
            }`}
        >
          <Sidebar
            suggestions={suggestions}
            onAcceptSuggestion={acceptSuggestion}
            onDismissSuggestion={removeSuggestion}
          />
        </div>
      </div>

      {/* Mobile overlay */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-10 md:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </div>
  )
}

export default App
