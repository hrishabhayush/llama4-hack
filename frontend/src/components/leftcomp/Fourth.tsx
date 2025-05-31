import {
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
  } from "@/components/ui/accordion";
  import { useFileContext } from "../FileContext";

export function Fourth() {
    return (
        <AccordionItem value="TIMELINE">
            <AccordionTrigger className="text-xs py-1 min-h-0 font-bold tracking-wide">TIMELINE</AccordionTrigger>
        </AccordionItem>
    )
}