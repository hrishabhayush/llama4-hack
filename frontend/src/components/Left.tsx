"use client";
import React from "react";
import { ResizablePanel } from "@/components/ui/resizable";
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion";

export function Left() {
  return (
    <ResizablePanel defaultSize={15} minSize={10} maxSize={40}>
      <div className="h-full flex p-2 bg-white">
        <Accordion type="multiple" className="w-full" defaultValue={["LLAMA4-HACK"]}>
          {/* LLAMA4-HACK project root */}
          <AccordionItem value="LLAMA4-HACK">
            <AccordionTrigger className="text-xs py-1 min-h-0 font-bold tracking-wide">LLAMA4-HACK</AccordionTrigger>
            <AccordionContent className="pl-2">
              <Accordion type="multiple" className="w-full" defaultValue={["frontend", "src", "components"]}>
                {/* Frontend folder */}
                <AccordionItem value="frontend">
                  <AccordionTrigger className="text-xs py-1 min-h-0">frontend</AccordionTrigger>
                  <AccordionContent className="pl-2">
                    <div className="text-xs py-0.5">.next/</div>
                    <div className="text-xs py-0.5">node_modules/</div>
                    <div className="text-xs py-0.5">public/</div>
                    {/* src folder */}
                    <Accordion type="multiple" className="w-full" defaultValue={["src", "components"]}>
                      <AccordionItem value="src">
                        <AccordionTrigger className="text-xs py-1 min-h-0 ml-2">src</AccordionTrigger>
                        <AccordionContent className="pl-2">
                          <div className="text-xs py-0.5 ml-2">app/</div>
                          {/* components folder */}
                          <Accordion type="multiple" className="w-full" defaultValue={["components"]}>
                            <AccordionItem value="components">
                              <AccordionTrigger className="text-xs py-1 min-h-0 ml-4">components</AccordionTrigger>
                              <AccordionContent className="pl-2">
                                <div className="text-xs py-0.5 ml-4">ui/</div>
                                <div className="text-xs py-0.5 ml-4">Center.tsx</div>
                                <div className="text-xs py-0.5 ml-4">Left.tsx</div>
                                <div className="text-xs py-0.5 ml-4">Right.tsx</div>
                                <div className="text-xs py-0.5 ml-4">ThreePanel.tsx</div>
                              </AccordionContent>
                            </AccordionItem>
                          </Accordion>
                          <div className="text-xs py-0.5 ml-2">lib/</div>
                        </AccordionContent>
                      </AccordionItem>
                    </Accordion>
                    <div className="text-xs py-0.5">.gitignore</div>
                    <div className="text-xs py-0.5">components.js...</div>
                    <div className="text-xs py-0.5">eslint.config.mjs</div>
                    <div className="text-xs py-0.5">next-env.d.ts</div>
                    <div className="text-xs py-0.5">next.config.ts</div>
                    <div className="text-xs py-0.5">package-lock.json</div>
                    <div className="text-xs py-0.5">package.json</div>
                    <div className="text-xs py-0.5">postcss.config...</div>
                    <div className="text-xs py-0.5">README.md</div>
                    <div className="text-xs py-0.5">tsconfig.json</div>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </AccordionContent>
          </AccordionItem>
          {/* Other top-level accordions */}
          <AccordionItem value="NOTEPADS">
            <AccordionTrigger className="text-xs py-1 min-h-0 font-bold tracking-wide">NOTEPADS</AccordionTrigger>
          </AccordionItem>
          <AccordionItem value="OUTLINE">
            <AccordionTrigger className="text-xs py-1 min-h-0 font-bold tracking-wide">OUTLINE</AccordionTrigger>
          </AccordionItem>
          <AccordionItem value="TIMELINE">
            <AccordionTrigger className="text-xs py-1 min-h-0 font-bold tracking-wide">TIMELINE</AccordionTrigger>
          </AccordionItem>
        </Accordion>
      </div>
    </ResizablePanel>
  );
}

