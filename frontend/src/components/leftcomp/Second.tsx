import {
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
  } from "@/components/ui/accordion";
  import { useFileContext } from "../FileContext";

export function Second() {
    return (
        <AccordionItem value="BUBBLE-MAP">
            <AccordionTrigger className="text-xs py-1 min-h-0 font-bold tracking-wide">BUBBLE-MAP</AccordionTrigger>
        </AccordionItem>
    )
}