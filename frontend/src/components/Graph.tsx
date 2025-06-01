'use client';

import React, { useRef, useEffect } from 'react';
import cytoscape from 'cytoscape';
import coseBilkent from 'cytoscape-cose-bilkent';

cytoscape.use(coseBilkent);

interface NodeData {
  id: string;
  label: string;
}

interface EdgeData {
  source: string;
  target: string;
  weight: number;
}

interface GraphProps {
  nodes: NodeData[];
  edges: EdgeData[];
  onNodeClick?: (nodeId: string) => void;
}

const Graph: React.FC<GraphProps> = ({ nodes, edges, onNodeClick }) => {
  const cyRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!cyRef.current) return;

    const cy = cytoscape({
      container: cyRef.current,
      elements: [
        ...nodes.map(n => ({ data: { id: n.id, label: n.label } })),
        ...edges.map(e => ({ data: { source: e.source, target: e.target, weight: e.weight } })),
      ],
      style: [
        {
          selector: 'node',
          style: {
            label: 'data(label)',
            'background-color': '#3B82F6',
            'color': '#ffffff',
            'text-outline-color': '#1E3A8A',
            'text-outline-width': 2,
            'font-size': 12,
          },
        },
        {
          selector: 'edge',
          style: {
            width: 'mapData(weight, 0, 1, 1, 6)',
            'line-color': '#60A5FA',
            'curve-style': 'bezier',
          },
        },
      ],
      layout: {
        name: 'cose-bilkent',
      },
    });

    cy.on('tap', 'node', (evt) => {
      const node = evt.target;
      if (onNodeClick) onNodeClick(node.id());
    });

    return () => cy.destroy();
  }, [nodes, edges]);

  return <div ref={cyRef} style={{ width: '100%', height: '100%' }} />;
};

export default Graph; 