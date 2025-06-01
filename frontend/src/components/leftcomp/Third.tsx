import {
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
  } from "@/components/ui/accordion";
  import { useFileContext } from "../FileContext";

export function Third() {
    return (
        <AccordionItem value="OUTLINE">
            <AccordionTrigger className="text-xs py-1 min-h-0 font-bold tracking-wide">OUTLINE</AccordionTrigger>
        </AccordionItem>
    )
}