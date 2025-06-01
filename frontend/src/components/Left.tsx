"use client";
import React from "react";
import { ResizablePanel } from "@/components/ui/resizable";
import {
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
  } from "@/components/ui/accordion";
  import { useFileContext } from "./FileContext";
import { First } from "./leftcomp/First";
import { Second } from "./leftcomp/Second";
import { Third } from "./leftcomp/Third";
import { Fourth } from "./leftcomp/Fourth";

export function Left() {
  const { openFile } = useFileContext();
  return (
    <ResizablePanel defaultSize={15} minSize={10} maxSize={40}>
      <div className="h-full flex p-2 bg-white">
        <Accordion type="multiple" className="w-full" defaultValue={["LLAMA4-HACK"]}>
          {/* LLAMA4-HACK project root */}
          <First />
          {/* Other top-level accordions */}
          <Second />
          <Third />
          <Fourth />
        </Accordion>
      </div>
    </ResizablePanel>
  );
}

