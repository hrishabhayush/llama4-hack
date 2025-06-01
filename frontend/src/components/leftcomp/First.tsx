import {
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
  } from "@/components/ui/accordion";
import React, { useEffect, useState } from "react";
import { File, MousePointer2 } from 'lucide-react';

export function First() {
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
                <div className="mb-2">
                  <label className="inline-flex items-center gap-1 cursor-pointer px-2 py-1 rounded bg-gray-100 hover:bg-gray-200 text-xs font-medium">
                    Choose file <MousePointer2 className="w-4 h-4" />
                    <input
                      type="file"
                      accept="application/pdf"
                      className="hidden"
                      onChange={async e => {
                        const file = e.target.files?.[0];
                        if (file) {
                          const success = await uploadPDF(file);
                          alert(success ? 'Upload successful!' : 'Upload failed!');
                        }
                      }}
                    />
                  </label>
                </div>
              </div>
              <div className="mb-2">
                <div className="font-semibold text-xs mb-1">Uploaded PDFs</div>
                <ul className="text-xs pl-2">
                  {uploadedFiles.length === 0 && <li className="text-muted-foreground">No files uploaded yet.</li>}
                  {uploadedFiles.map(f => (
                    <li
                      key={f}
                      className="flex items-center gap-1"
                    >
                      <File className="w-3 h-3 mr-1 shrink-0" />
                      {f}
                    </li>
                  ))}
                </ul>
              </div>
              <Accordion type="multiple" className="w-full" defaultValue={["frontend", "src", "components"]}>
                {/* Frontend folder */}
                {/* <AccordionItem value="frontend"> 
                </AccordionItem> */}
              </Accordion>
            </AccordionContent>
          </AccordionItem>
    );
}