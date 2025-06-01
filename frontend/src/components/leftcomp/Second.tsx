import {
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
  } from "@/components/ui/accordion";
  import { useFileContext } from "../FileContext";

export function Second() {
    const { openFile } = useFileContext();
    
    return (
        <AccordionItem value="BUBBLE-MAP">
            <AccordionTrigger className="text-xs py-1 min-h-0 font-bold tracking-wide">BUBBLE-MAP</AccordionTrigger>
            <AccordionContent className="pl-2">
                <div className="text-xs py-0.5 ml-2 cursor-pointer hover:bg-accent rounded px-1" onClick={() => openFile("KnowledgeGraph.graph")}>KnowledgeGraph.graph</div>
            </AccordionContent>
        </AccordionItem>
    );
}