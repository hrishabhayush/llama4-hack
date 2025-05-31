import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
  } from "@/components/ui/resizable"

export function Center() {
    return (
        <ResizablePanel defaultSize={60} minSize={20}>
          <div className="h-full flex items-center justify-center p-6 bg-white">
            <span className="font-semibold">Progress</span>
          </div>
        </ResizablePanel>
    )
}
        