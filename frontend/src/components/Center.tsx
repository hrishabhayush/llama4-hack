"use client";
import React from "react";
import { useFileContext } from "./FileContext";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { ResizablePanel } from "@/components/ui/resizable";
import Graph from "./Graph";

export function Center() {
  const { openFiles, activeFile, setActiveFileByName, closeFile, updateFileContent } = useFileContext();

  // Parse graph data from file content
  const parseGraphData = (content: string) => {
    try {
      return JSON.parse(content);
    } catch (error) {
      console.error("Error parsing graph data:", error);
      return { nodes: [], edges: [] };
    }
  };

  return (
    <ResizablePanel defaultSize={60} minSize={20}>
      <div className="flex-1 h-full w-full flex flex-col min-h-0 overflow-hidden">
        {openFiles.length === 0 ? (
          <div className="flex-1 h-full w-full flex items-center justify-center">
            <span className="text-muted-foreground text-xs">No file open</span>
          </div>
        ) : (
          <Tabs value={activeFile?.name || undefined} onValueChange={setActiveFileByName} className="w-full h-full flex-1 flex flex-col min-h-0 overflow-hidden">
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
              <TabsContent key={file.name} value={file.name} className="flex-1 flex flex-col h-full w-full min-h-0 overflow-hidden p-0">
                {/* Directory path */}
                <div className="text-xs text-muted-foreground px-4 py-2 border-b bg-muted">
                  {file.path}
                </div>
                
                {/* Render content based on file type */}
                {file.type === 'graph' ? (
                  /* Graph visualization */
                  <div className="flex-1 h-full w-full min-h-0 overflow-hidden">
                    <Graph 
                      {...parseGraphData(file.content)} 
                      onNodeClick={(nodeId) => console.log('Clicked node:', nodeId)}
                    />
                  </div>
                ) : (
                  /* Editable file content for text files */
                  <div className="flex-1 flex flex-col h-full w-full min-h-0 overflow-y-auto overflow-x-hidden items-center">
                    <textarea
                      className="p-4 font-mono text-xs bg-white h-full outline-none resize-none min-h-0 flex-1"
                      style={{ maxWidth: '153ch', width: '100%' }}
                      value={file.content}
                      onChange={e => updateFileContent(file.name, e.target.value)}
                      spellCheck={false}
                      wrap="soft"
                    />
                  </div>
                )}
              </TabsContent>
            ))}
          </Tabs>
        )}
      </div>
    </ResizablePanel>
  );
}
        