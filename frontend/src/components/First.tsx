import {
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
  } from "@/components/ui/accordion";
  import { useFileContext } from "./FileContext";

export function First() {
    const { openFile } = useFileContext();
    return (
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
                                {/* Clickable files */}
                                <div className="text-xs py-0.5 ml-4 cursor-pointer hover:bg-accent rounded px-1" onClick={() => openFile("Center.tsx")}>Center.tsx</div>
                                <div className="text-xs py-0.5 ml-4 cursor-pointer hover:bg-accent rounded px-1" onClick={() => openFile("Left.tsx")}>Left.tsx</div>
                                <div className="text-xs py-0.5 ml-4 cursor-pointer hover:bg-accent rounded px-1" onClick={() => openFile("Right.tsx")}>Right.tsx</div>
                                <div className="text-xs py-0.5 ml-4 cursor-pointer hover:bg-accent rounded px-1" onClick={() => openFile("ThreePanel.tsx")}>ThreePanel.tsx</div>
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
    );
}