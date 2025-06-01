import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
  } from "@/components/ui/resizable"
import { Left } from "./Left"
import { Center } from "./Center"
import { Right } from "./Right"
import { FileProvider } from "./FileContext"

export function ThreePanel() {
  return (
    <FileProvider>
      <div className="h-screen w-screen flex flex-col">
        <ResizablePanelGroup direction="horizontal" className="flex-1 h-full w-full">
          <Left />
          <ResizableHandle />
          <Center />
          <ResizableHandle />
          <Right />
        </ResizablePanelGroup>
      </div>
    </FileProvider>
  )
}
  