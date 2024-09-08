import {
  ReactFlow,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
} from "@/components/ui/card";

// FeederMessage Type Definition
interface FeederMessage {
  id_: string;
  input: number[];
  prediction: number;
  host: string; // Host IP (target)
  target: string; // Target IP (source)
  port: number;
}

// ReactFlow component for rendering network diagram
export const NetworkFlow = ({ data }: { data: FeederMessage[] }) => {
  // Convert FeederMessage to React Flow nodes and edges
  const nodes = data.map((message) => ({
    id: `node-${message.id_}`, // Unique ID for the node
    data: { label: message.target }, // Label with target IP
    position: { x: Math.random() * 250, y: Math.random() * 250 }, // Random position
    type: "default", // Default node type
  }));

  // Add nodes for hosts (targets)
  const hostNodes = Array.from(
    new Set(data.map((message) => message.host))
  ).map((host) => ({
    id: `host-${host}`,
    data: { label: host },
    position: { x: Math.random() * 400, y: Math.random() * 400 },
    type: "input", // Mark host nodes as input nodes
  }));

  // Map to edges with 'default' type (no animation)
  const edges = data.map(
    (message) => (
      console.log(message),
      {
        id: `edge-${message.id_}`,
        source: `node-${message.id_}`, // Connects to the source node
        target: `host-${message.host}`, // Connects to the target host node
        label: `Port: ${message.port}`, // Shows the port in the edge
        type: "default", // Default edge type
      }
    )
  );

  // Combine input nodes with host nodes
  const allNodes = [...nodes, ...hostNodes];

  // Hooks for managing nodes and edges
  const [reactFlowNodes, , onNodesChange] = useNodesState(allNodes);
  const [reactFlowEdges, , onEdgesChange] = useEdgesState(edges);
  console.log(reactFlowNodes);
  console.log(reactFlowEdges);

  return (
    <div style={{ height: "100%" }}>
      <ReactFlow
        nodes={reactFlowNodes}
        edges={reactFlowEdges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
      >
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
};

// Card wrapper component for NetworkFlow
export const NetworkFlowCard = ({ data }: { data: FeederMessage[] }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Network Diagram</CardTitle>
        <CardDescription>
          Visual representation of IPs targeting hosts.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {/* Render the NetworkFlow without any styling */}
        <div style={{ height: "40vh", width: "80%" }}>
          <NetworkFlow data={data} />
        </div>
      </CardContent>
    </Card>
  );
};

export default NetworkFlowCard;
