"use client";
import React from "react";
import { useFileContext } from "./FileContext";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { ResizablePanel } from "@/components/ui/resizable";

export function Center() {
  const { openFiles, activeFile, setActiveFileByName, closeFile, updateFileContent } = useFileContext();

  return (
    <ResizablePanel defaultSize={60} minSize={20}>
      <div className="h-full flex flex-col p-0 bg-white">
        {/* Tabs for open files */}
        <Tabs value={activeFile?.name || undefined} onValueChange={setActiveFileByName} className="w-full">
          <TabsList className="rounded-none border-b bg-white h-8 min-h-0 px-2">
            {openFiles.map((file) => (
              <div key={file.name} className="flex items-center">
                <TabsTrigger value={file.name} className="text-xs px-3 py-1 min-h-0 rounded-none border-0 border-b-2 data-[state=active]:border-blue-500">
                  {file.name}
                </TabsTrigger>
                <button
                  className="ml-1 text-xs text-muted-foreground hover:text-red-500"
                  onClick={(e) => {
                    e.stopPropagation();
                    closeFile(file.name);
                  }}
                  tabIndex={-1}
                >
                  ×
                </button>
              </div>
            ))}
          </TabsList>
          {openFiles.map((file) => (
            <TabsContent key={file.name} value={file.name} className="p-0">
              {/* Directory path */}
              <div className="text-xs text-muted-foreground px-4 py-2 border-b bg-muted">
                {file.path}
              </div>
              {/* Editable file content */}
              <div className="flex-1 flex flex-col h-full w-full overflow-y-auto overflow-x-hidden items-center">
                <textarea
                  className="p-4 font-mono text-xs bg-white h-full outline-none resize-none min-h-0 flex-1"
                  style={{ maxWidth: '153ch', width: '100%' }}
                  value={file.content}
                  onChange={e => updateFileContent(file.name, e.target.value)}
                  spellCheck={false}
                  wrap="soft"
                />
              </div>
            </TabsContent>
          ))}
        </Tabs>
        {/* If no file is open, show a placeholder */}
        {openFiles.length === 0 && (
          <div className="flex-1 flex items-center justify-center text-muted-foreground text-xs">No file open</div>
        )}
      </div>
    </ResizablePanel>
  );
}
        