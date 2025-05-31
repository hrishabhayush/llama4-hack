"use client";
import React, { createContext, useContext, useState, ReactNode } from "react";

// File type
export type FileType = {
  name: string;
  path: string;
  content: string;
};

const initialFiles: FileType[] = [
  {
    name: "Left.tsx",
    path: "frontend/src/components/Left.tsx",
    content: "// Content of Left.tsx...",
  },
  {
    name: "Right.tsx",
    path: "frontend/src/components/Right.tsx",
    content: "// Content of Right.tsx...",
  },
  {
    name: "Center.tsx",
    path: "frontend/src/components/Center.tsx",
    content: "// Content of Center.tsx...",
  },
  {
    name: "ThreePanel.tsx",
    path: "frontend/src/components/ThreePanel.tsx",
    content: "// Content of ThreePanel.tsx...",
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
    const file = initialFiles.find((f) => f.name === fileName);
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