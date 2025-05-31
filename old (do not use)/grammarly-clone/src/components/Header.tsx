import type React from 'react'

interface HeaderProps {
  isSidebarCollapsed: boolean
  onToggleSidebar: () => void
  onToggleMobileMenu: () => void
}

const Header: React.FC<HeaderProps> = ({
  isSidebarCollapsed,
  onToggleSidebar,
  onToggleMobileMenu
}) => {
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 shadow-sm relative z-30">
      {/* Left side */}
      <div className="flex items-center space-x-4">
        {/* Hamburger menu for mobile */}
        <button
          className="md:hidden p-2 hover:bg-gray-100 rounded-lg"
          onClick={onToggleMobileMenu}
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        {/* Grammarly logo */}
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
            <span className="text-white font-bold text-lg">G</span>
          </div>
          <span className="hidden sm:block text-gray-900 font-medium">Grammarly</span>
        </div>
      </div>

      {/* Center - Document title */}
      <div className="flex-1 flex justify-center">
        <div className="max-w-md">
          <input
            type="text"
            defaultValue="Demo document"
            className="text-center text-gray-900 font-medium bg-transparent border-none outline-none hover:bg-gray-50 px-3 py-1 rounded"
          />
        </div>
      </div>

      {/* Right side */}
      <div className="flex items-center space-x-3">
        {/* Goals badge */}
        <div className="hidden sm:flex items-center space-x-2 bg-gray-100 px-3 py-1.5 rounded-full">
          <div className="w-2 h-2 bg-green-500 rounded-full" />
          <span className="text-sm text-gray-700 font-medium">Goals</span>
        </div>

        {/* Overall score badge */}
        <div className="hidden sm:flex items-center space-x-2 bg-green-100 px-3 py-1.5 rounded-full">
          <span className="text-sm font-semibold text-green-700">98</span>
          <span className="text-sm text-green-700">Overall score</span>
        </div>

        {/* Sidebar toggle */}
        <button
          className="p-2 hover:bg-gray-100 rounded-lg hidden md:block"
          onClick={onToggleSidebar}
        >
          <svg
            className={`w-5 h-5 transition-transform ${isSidebarCollapsed ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </header>
  )
}

export default Header
