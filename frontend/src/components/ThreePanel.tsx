import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
  } from "@/components/ui/resizable"
import { Left } from "./Left"
import { Center } from "./Center"
import { Right } from "./Right"

export function ThreePanel() {
  return (
    <div style={{ height: "100vh", width: "100vw" }}>
      <ResizablePanelGroup direction="horizontal" className="h-full w-full">
        <Left />
        <ResizableHandle />
        <Center />
        <ResizableHandle />
        <Right />
      </ResizablePanelGroup>
    </div>
  )
}
  