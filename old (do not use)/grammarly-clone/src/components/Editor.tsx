import type React from 'react'
import { useState, useRef, useEffect } from 'react'
import ToolbarIcons from './ToolbarIcons'

interface EditorProps {
  onAddSuggestion: (word: string) => void
}

const Editor: React.FC<EditorProps> = ({ onAddSuggestion }) => {
  const [content, setContent] = useState('')
  const editorRef = useRef<HTMLDivElement>(null)
  const [underlinedWords, setUnderlinedWords] = useState<Set<string>>(new Set())

  const checkForLongWords = (text: string) => {
    const words = text.split(/\s+/)
    const longWords = new Set<string>()

    for (const word of words) {
      // Remove punctuation for length check
      const cleanWord = word.replace(/[^\w]/g, '')
      if (cleanWord.length > 12) {
        longWords.add(word)
        if (!underlinedWords.has(word)) {
          onAddSuggestion(cleanWord)
        }
      }
    }

    setUnderlinedWords(longWords)
  }

  const handleInput = (e: React.FormEvent<HTMLDivElement>) => {
    const text = e.currentTarget.textContent || ''
    setContent(text)
    checkForLongWords(text)
  }

  const renderHighlightedText = () => {
    if (!content) return null

    const words = content.split(/(\s+)/)

    return words.map((word, index) => {
      const cleanWord = word.replace(/[^\w]/g, '')
      const shouldUnderline = cleanWord.length > 12 && cleanWord.length > 0

      if (shouldUnderline) {
        return (
          <span
            key={`${word}-${index}`}
            className="relative"
          >
            <span className="border-b-2 border-red-500 border-dashed">
              {word}
            </span>
          </span>
        )
      }

      return <span key={`${word}-${index}`}>{word}</span>
    })
  }

  useEffect(() => {
    if (editorRef.current && !content) {
      editorRef.current.focus()
    }
  }, [content])

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Editor area */}
      <div className="flex-1 p-8 overflow-y-auto">
        <div className="max-w-4xl mx-auto">
          {/* Content editable area */}
          <div className="relative">
            {/* Placeholder */}
            {!content && (
              <div className="absolute inset-0 text-gray-400 pointer-events-none">
                <p className="text-lg leading-relaxed">
                  Start writing, or paste your text here to check for grammar, spelling, and style improvements...
                </p>
              </div>
            )}

            {/* Actual editor */}
            <div
              ref={editorRef}
              contentEditable
              onInput={handleInput}
              className="min-h-96 text-lg leading-relaxed text-gray-900 outline-none"
              style={{
                fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                lineHeight: '1.6'
              }}
              suppressContentEditableWarning={true}
            />

            {/* Overlay for highlighting */}
            {content && (
              <div
                className="absolute inset-0 pointer-events-none text-lg leading-relaxed"
                style={{
                  fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                  lineHeight: '1.6',
                  color: 'transparent'
                }}
              >
                {renderHighlightedText()}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Bottom toolbar */}
      <div className="border-t border-gray-200 p-4">
        <div className="max-w-4xl mx-auto">
          <ToolbarIcons />
        </div>
      </div>
    </div>
  )
}

export default Editor
