"use client";
import React from "react";
import Image from "next/image";
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
      <div className="h-full flex flex-col p-2 bg-white">
        <div className="flex items-center mb-4 pl-2">
          <Image
            src="/llama.png"
            alt="Background-removed Llama-Logo"
            width={40}
            height={40}
            className="object-contain"
          />
          <span className="mr-2 font-bold">Llama on Fly</span>
        </div>
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

