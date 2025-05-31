# Modern Text Editor

A modern, minimal front-end web application built with React and Tailwind CSS, featuring a clean interface similar to Grammarly and Cursor.

## Features

- **Fixed Header**: App logo, document title, and action buttons (Goals, Score, Share)
- **Three-Column Layout**:
  - **Left Sidebar (250px)**: AI Assistant prompting area with quick actions and custom prompt input
  - **Main Content**: Rich text editor with support for text highlighting
  - **Right Sidebar (300px)**: Tabbed interface for Suggestions and Review
- **Modern Design**: Clean, minimal aesthetics using Inter font and Tailwind CSS
- **Text Highlighting**: Support for different highlight colors (red for errors, blue for clarity, green for enhancements)

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. Navigate to the project directory:
   ```bash
   cd website2
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Project Structure

```
website2/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── App.js             # Main application component
│   ├── index.js           # React entry point
│   └── index.css          # Global styles and Tailwind imports
├── package.json           # Project dependencies
├── tailwind.config.js     # Tailwind CSS configuration
└── postcss.config.js      # PostCSS configuration
```

## Styling

The application uses Tailwind CSS for styling with a custom configuration that includes:

- Inter font family for modern typography
- Custom color palette for the editor interface
- Responsive design principles
- Custom scrollbar styling

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

## Design System

### Colors
- Primary text: `#1f2937`
- Secondary text: `#6b7280`
- Accent blue: `#3b82f6`
- Accent red: `#ef4444`
- Background: `#fafafa`
- Sidebar background: `#ffffff`

### Typography
- Font family: Inter (fallback to system fonts)
- Line height: 1.6 for content
- Various font weights: 300, 400, 500, 600, 700

## Notes

This is a visual prototype focusing on layout and styling. The LLM integration and grammar checking functionality are not implemented - only the UI components and styling are provided. 