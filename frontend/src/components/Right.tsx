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
import { Image, SendHorizonal, Infinity, MessageSquare } from "lucide-react"
import React, { useState } from "react";



export function Right() {

  const [selectedRole, setSelectedRole] = useState("Agent");

  // Handler for image upload
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // You can handle the file here (e.g., upload, preview, etc.)
      console.log("Selected image:", file);
    }
  };

    return (
        <ResizablePanel defaultSize={35} minSize={10} maxSize={40}>
          <div className="h-full flex flex-col justify-end p-6 bg-white">
            {/* Unified input box */}
            <div className="w-full bg-white border border-input rounded-xl p-3 flex flex-col gap-2">
              {/* Context label */}
              <div className="text-xs text-muted-foreground flex items-center gap-2">
                <span className="font-medium">@ Add context</span>
              </div>
              {/* Textarea */}
              <Textarea placeholder="Plan, search, write anything" className="mb-0 bg-white border-white border-none shadow-none resize-none focus-visible:ring-0 focus-visible:border-none" />
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
                  {/* Send button (icon placeholder) */}
                  <SendHorizonal />
                </div>
              </div>
            </div>
          </div>
        </ResizablePanel>
    )
}