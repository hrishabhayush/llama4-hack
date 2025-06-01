import {
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
  } from "@/components/ui/accordion";
import { useFileContext } from "../FileContext";
import React, { useEffect, useState } from "react";
import { File } from 'lucide-react';

export function First() {
    const { openFile } = useFileContext();
    const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);

    // Fetch uploaded files
    const fetchFiles = async () => {
      const res = await fetch('http://localhost:8000/api/uploaded-files');
      const data = await res.json();
      setUploadedFiles(data.files || []);
    };

    useEffect(() => {
      fetchFiles();
    }, []);

    async function uploadPDF(file: File): Promise<boolean> {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const res = await fetch('http://localhost:8000/api/upload', {
          method: 'POST',
          body: formData,
        });
        if (!res.ok) throw new Error('Upload failed');
        await res.json();
        await fetchFiles(); // Refresh file list after upload
        return true;
      } catch (e) {
        return false;
      }
    }

    return (
        <AccordionItem value="LLAMA4-HACK">
            <AccordionTrigger className="text-xs py-0.5 min-h-0 font-bold tracking-wide">LLAMA4-HACK</AccordionTrigger>
            <AccordionContent className="pl-2">
              <div className="text-xs py-0.5 mb-2">
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={async e => {
                    const file = e.target.files?.[0];
                    if (file) {
                      const success = await uploadPDF(file);
                      alert(success ? 'Upload successful!' : 'Upload failed!');
                    }
                  }}
                />
              </div>
              <div className="mb-2">
                <div className="font-semibold text-xs mb-1">Uploaded Files</div>
                <ul className="text-xs pl-2">
                  {uploadedFiles.length === 0 && <li className="text-muted-foreground">No files uploaded yet.</li>}
                  {uploadedFiles.map(f => (
                    <li key={f} className="flex items-center gap-1">
                      <File className="w-3 h-3 mr-1 shrink-0" />
                      {f}
                    </li>
                  ))}
                </ul>
              </div>
              <Accordion type="multiple" className="w-full" defaultValue={["frontend", "src", "components"]}>
                {/* Frontend folder */}
                <div className="text-xs py-0.5">Uploaded PDFs</div>
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
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </AccordionContent>
          </AccordionItem>
    );
}