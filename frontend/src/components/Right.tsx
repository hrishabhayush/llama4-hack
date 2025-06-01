"use client";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Image, SendHorizontal, CircleStop, Infinity, MessageSquare } from "lucide-react"
import React, { useState } from "react";

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

export function Right() {

  const [selectedRole, setSelectedRole] = useState("Agent");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Handler for image upload
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // You can handle the file here (e.g., upload, preview, etc.)
      console.log("Selected image:", file);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input.trim(),
      role: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulate response delay
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `${userMessage.content}`,
        role: 'assistant',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1200);
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleStop = () => {
    setIsLoading(false);
  };

  return (
    <ResizablePanel defaultSize={35} minSize={10} maxSize={40}>
      <div className="h-full flex flex-col p-6 bg-white">
        {/* Messages area */}
        <div className="flex-1 overflow-y-auto mb-4 space-y-3">
          {messages.map((message) => (
            <div key={message.id} className="w-full">
              <div className={`w-full ${message.role === 'user'
                  ? 'bg-gray-700 text-white rounded-lg px-3 py-2'
                  : 'text-muted-foreground px-3'
                }`}>
                <p className="text-sm">{message.content}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Unified input box */}
        <div className="w-full bg-white border border-input rounded-xl p-3 flex flex-col gap-2">
          {/* Context label */}
          <div className="text-xs text-muted-foreground flex items-center gap-2">
            <span className="font-medium">@ Add context</span>
          </div>
          {/* Textarea */}
          <Textarea
            placeholder="Plan, search, write anything"
            className="mb-0 bg-white border-white border-none shadow-none resize-none focus-visible:ring-0 focus-visible:border-none"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          {/* Action row */}
          <div className="flex items-center gap-2 mt-1">
            {/* Dropdown (Agent/Ask) */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="font-semibold">{selectedRole}</Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-25" align="start">
                <DropdownMenuItem onClick={() => setSelectedRole("Agent")}>
                  <Infinity />
                  <span className="text-xs">Agent</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSelectedRole("Ask")}>
                  <MessageSquare />
                  <span className="text-xs">Ask</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
            <div className="flex items-center gap-2 ml-auto">
              {/* Image upload button */}
              <label className="cursor-pointer">
                <Image />
                <input type="file" accept="image/*" className="hidden" onChange={handleImageUpload} />
              </label>
              {/* Send/Stop button */}
              <button onClick={isLoading ? handleStop : handleSend} className="cursor-pointer">
                {isLoading ? <CircleStop /> : <SendHorizontal />}
              </button>
            </div>
          </div>
        </div>
      </div>
    </ResizablePanel>
  )
}