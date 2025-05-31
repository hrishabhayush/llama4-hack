import type React from 'react'

interface Suggestion {
  id: string
  type: 'spelling' | 'grammar' | 'clarity'
  title: string
  description: string
  originalWord: string
  replacement: string
}

interface SuggestionCardProps {
  suggestion: Suggestion
  onAccept: () => void
  onDismiss: () => void
}

const SuggestionCard: React.FC<SuggestionCardProps> = ({
  suggestion,
  onAccept,
  onDismiss
}) => {
  const getIcon = () => {
    switch (suggestion.type) {
      case 'spelling':
        return (
          <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
            <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        )
      case 'grammar':
        return (
          <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center flex-shrink-0">
            <svg className="w-4 h-4 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
        )
      case 'clarity':
        return (
          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
            <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
        )
      default:
        return (
          <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0">
            <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        )
    }
  }

  const getTypeLabel = () => {
    switch (suggestion.type) {
      case 'spelling': return 'Correctness'
      case 'grammar': return 'Grammar'
      case 'clarity': return 'Clarity'
      default: return 'Suggestion'
    }
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start space-x-3">
        {/* Icon */}
        {getIcon()}

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2 mb-1">
            <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
              {getTypeLabel()}
            </span>
          </div>

          <h4 className="text-sm font-semibold text-gray-900 mb-1">
            {suggestion.title}
          </h4>

          <p className="text-sm text-gray-600 mb-3">
            {suggestion.description}
          </p>

          {/* Action buttons */}
          <div className="flex items-center space-x-2">
            <button
              onClick={onAccept}
              className="px-3 py-1.5 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 transition-colors"
            >
              Accept
            </button>
            <button
              onClick={onDismiss}
              className="px-3 py-1.5 text-gray-600 text-sm font-medium rounded-md hover:bg-gray-100 transition-colors"
            >
              Dismiss
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SuggestionCard
