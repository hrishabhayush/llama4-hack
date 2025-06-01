"use client";
import React, { createContext, useContext, useState, ReactNode } from "react";

// File type
export type FileType = {
  name: string;
  path: string;
  content: string;
  type?: 'text' | 'graph' | 'pdf'; // Add type to distinguish between text files and graph files
};

const initialFiles: FileType[] = [
  {
    name: "Left.tsx",
    path: "frontend/src/components/Left.tsx",
    content: "// Content of Left.tsx...",
    type: "text",
  },
  {
    name: "Right.tsx",
    path: "frontend/src/components/Right.tsx",
    content: "// Content of Right.tsx...",
    type: "text",
  },
  {
    name: "Center.tsx",
    path: "frontend/src/components/Center.tsx",
    content: "// Content of Center.tsx...",
    type: "text",
  },
  {
    name: "ThreePanel.tsx",
    path: "frontend/src/components/ThreePanel.tsx",
    content: "// Content of ThreePanel.tsx...",
    type: "text",
  },
  {
    name: "KnowledgeGraph.graph",
    path: "knowledge-map/KnowledgeGraph.graph",
    content: `{
  "nodes": [
    { "id": "1", "label": "What is AI?", "important": true },
    { "id": "2", "label": "Machine Learning", "important": true },
    { "id": "3", "label": "Deep Learning", "important": true },
    { "id": "4", "label": "Neural Networks", "important": true },
    { "id": "5", "label": "Natural Language Processing", "important": true },
    { "id": "6", "label": "Computer Vision", "important": false },
    { "id": "7", "label": "Reinforcement Learning", "important": false },
    { "id": "8", "label": "Supervised Learning", "important": false },
    { "id": "9", "label": "Unsupervised Learning", "important": false },
    { "id": "10", "label": "Transformers", "important": false },
    { "id": "11", "label": "GPT Models", "important": false },
    { "id": "12", "label": "BERT", "important": false },
    { "id": "13", "label": "CNN", "important": false },
    { "id": "14", "label": "RNN", "important": false },
    { "id": "15", "label": "LSTM", "important": false },
    { "id": "16", "label": "Attention Mechanism", "important": false },
    { "id": "17", "label": "Backpropagation", "important": false },
    { "id": "18", "label": "Gradient Descent", "important": false },
    { "id": "19", "label": "Overfitting", "important": false },
    { "id": "20", "label": "Transfer Learning", "important": false }
  ],
  "edges": [
    { "source": "1", "target": "2", "weight": 0.9 },
    { "source": "2", "target": "3", "weight": 0.8 },
    { "source": "2", "target": "8", "weight": 0.7 },
    { "source": "2", "target": "9", "weight": 0.7 },
    { "source": "3", "target": "4", "weight": 0.9 },
    { "source": "1", "target": "5", "weight": 0.6 },
    { "source": "1", "target": "6", "weight": 0.6 },
    { "source": "2", "target": "7", "weight": 0.6 },
    { "source": "4", "target": "13", "weight": 0.8 },
    { "source": "4", "target": "14", "weight": 0.8 },
    { "source": "14", "target": "15", "weight": 0.9 },
    { "source": "5", "target": "10", "weight": 0.8 },
    { "source": "10", "target": "11", "weight": 0.9 },
    { "source": "10", "target": "12", "weight": 0.8 },
    { "source": "10", "target": "16", "weight": 0.9 },
    { "source": "6", "target": "13", "weight": 0.8 },
    { "source": "4", "target": "17", "weight": 0.7 },
    { "source": "17", "target": "18", "weight": 0.8 },
    { "source": "2", "target": "19", "weight": 0.5 },
    { "source": "3", "target": "20", "weight": 0.7 },
    { "source": "8", "target": "18", "weight": 0.6 },
    { "source": "16", "target": "11", "weight": 0.8 },
    { "source": "16", "target": "12", "weight": 0.7 }
  ]
}`,
    type: "graph",
  },
];

type FileContextType = {
  openFiles: FileType[];
  activeFile: FileType | null;
  openFile: (fileName: string) => void;
  closeFile: (fileName: string) => void;
  setActiveFileByName: (fileName: string) => void;
  updateFileContent: (fileName: string, newContent: string) => void;
  allFiles: FileType[];
};

const FileContext = createContext<FileContextType | null>(null);

export function FileProvider({ children }: { children: ReactNode }) {
  const [openFiles, setOpenFiles] = useState<FileType[]>([]);
  const [activeFile, setActiveFile] = useState<FileType | null>(null);

  // Open a file (add to openFiles if not present, set as active)
  const openFile = (fileName: string) => {
    let file = initialFiles.find((f) => f.name === fileName);
    // Special case for bubble-map.json
    if (!file && fileName === "bubble-map.json") {
      // Fetch from backend
      fetch("http://localhost:8000/files/bubble-map.json")
        .then(res => res.json())
        .then(data => {
          const bubbleMapFile = {
            name: "bubble-map.json",
            path: "backend/files/bubble-map.json",
            content: JSON.stringify(data, null, 2),
            type: "graph" as const
          };
          setOpenFiles((prev) => {
            if (prev.find((f) => f.name === fileName)) return prev;
            return [...prev, bubbleMapFile];
          });
          setActiveFile(bubbleMapFile);
        });
      return;
    }
    // Special case for outline.txt
    if (!file && fileName === "outline.txt") {
      // Fetch from backend
      fetch("http://localhost:8000/files/outline.txt")
        .then(res => res.text())
        .then(data => {
          const outlineFile = {
            name: "outline.txt",
            path: "outline.txt",
            content: data,
            type: "text" as const
          };
          setOpenFiles((prev) => {
            if (prev.find((f) => f.name === fileName)) return prev;
            return [...prev, outlineFile];
          });
          setActiveFile(outlineFile);
        });
      return;
    }
    if (!file) return;
    setOpenFiles((prev) => {
      if (prev.find((f) => f.name === fileName)) return prev;
      return [...prev, file];
    });
    setActiveFile(file);
  };

  // Close a file (remove from openFiles, set active to last or null)
  const closeFile = (fileName: string) => {
    setOpenFiles((prev) => {
      const filtered = prev.filter((f) => f.name !== fileName);
      if (activeFile && activeFile.name === fileName) {
        setActiveFile(filtered.length ? filtered[filtered.length - 1] : null);
      }
      return filtered;
    });
  };

  // Set active file by name
  const setActiveFileByName = (fileName: string) => {
    const file = openFiles.find((f) => f.name === fileName);
    if (file) setActiveFile(file);
  };

  // Update file content
  const updateFileContent = (fileName: string, newContent: string) => {
    setOpenFiles((prev) =>
      prev.map((f) =>
        f.name === fileName ? { ...f, content: newContent } : f
      )
    );
    if (activeFile && activeFile.name === fileName) {
      setActiveFile({ ...activeFile, content: newContent });
    }
    // Persist outline.txt edits to backend
    if (fileName === "outline.txt") {
      fetch("http://localhost:8000/files/outline.txt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: newContent })
      });
    }
  };

  return (
    <FileContext.Provider
      value={{
        openFiles,
        activeFile,
        openFile,
        closeFile,
        setActiveFileByName,
        updateFileContent,
        allFiles: initialFiles,
      }}
    >
      {children}
    </FileContext.Provider>
  );
}

export function useFileContext() {
  const ctx = useContext(FileContext);
  if (!ctx) throw new Error("useFileContext must be used within a FileProvider");
  return ctx;
} 