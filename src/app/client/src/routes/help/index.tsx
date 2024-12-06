import { createFileRoute } from "@tanstack/react-router";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import ReactMarkdown from "react-markdown";

import readme from "/workspaces/NIDS/README.md?raw";
import userGuide from "/workspaces/NIDS/docs/USERGUIDE.md?raw";
import aiReadMe from "/workspaces/NIDS/src/ai/README.md?raw";

export const Route = createFileRoute("/help/")({
  component: () => (
    <div className="p-8 max-w-4xl mx-auto font-sans">
      <h1 className="text-4xl font-bold mb-6 text-primary">NIDS Help Page</h1>

      <Tabs defaultValue="file1" className="space-y-4">
        <TabsList className="grid w-full grid-cols-3 mb-4">
          <TabsTrigger value="file1">Main ReadME</TabsTrigger>
          <TabsTrigger value="file2">User Guide</TabsTrigger>
          <TabsTrigger value="file3">AI</TabsTrigger>
        </TabsList>

        <TabsContent value="file1" className="markdown-content">
          <ReactMarkdown>{readme}</ReactMarkdown>
        </TabsContent>

        <TabsContent value="file2" className="markdown-content">
          <ReactMarkdown>{userGuide}</ReactMarkdown>
        </TabsContent>

        <TabsContent value="file3" className="markdown-content">
          <ReactMarkdown>{aiReadMe}</ReactMarkdown>
        </TabsContent>
      </Tabs>
    </div>
  ),
});
