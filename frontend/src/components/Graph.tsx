'use client';

import React, { useRef, useEffect } from 'react';
import cytoscape from 'cytoscape';
import coseBilkent from 'cytoscape-cose-bilkent';

cytoscape.use(coseBilkent);

interface NodeData {
  id: string;
  label: string;
  important?: boolean;
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
        ...nodes.map(n => ({ 
          data: { 
            id: n.id, 
            label: n.label, 
            important: n.important || false 
          },
          classes: n.important ? 'important-node' : 'regular-node'
        })),
        ...edges.map(e => ({ data: { source: e.source, target: e.target, weight: e.weight } })),
      ],
      style: [
        {
          selector: '.important-node',
          style: {
            label: 'data(label)',
            'background-color': '#000000',
            'color': '#ffffff',
            'text-outline-color': '#000000',
            'text-outline-width': 1,
            'font-size': 12,
            'width': 30,
            'height': 30,
            'text-valign': 'center',
            'text-halign': 'center',
          },
        },
        {
          selector: '.regular-node',
          style: {
            'background-color': '#000000',
            'color': '#ffffff', 
            'text-outline-color': '#000000',
            'text-outline-width': 1,
            'font-size': 8,
            'width': 10,
            'height': 10,
            'text-valign': 'center',
            'text-halign': 'center',
            'label': '', // Initially no label
          },
        },
        {
          selector: 'edge',
          style: {
            width: 'mapData(weight, 0, 1, 0.5, 2)',
            'line-color': '#000000',
            'curve-style': 'bezier',
          },
        },
      ],
      layout: {
        name: 'cose-bilkent',
        fit: true,
        padding: 30,
        animate: 'end',
        animationDuration: 1000,
      } as any,
    });

    // Handle zoom-based label visibility
    cy.on('zoom', () => {
      const zoomLevel = cy.zoom();
      console.log('Zoom level:', zoomLevel); // Debug log
      
      // Show labels for regular nodes when zoomed in (zoom > 1.2)
      if (zoomLevel > 2) {
        cy.nodes('.regular-node').forEach((node) => {
          node.style('label', node.data('label'));
        });
        console.log('Showing regular node labels');
      } else {
        cy.nodes('.regular-node').forEach((node) => {
          node.style('label', '');
        });
        console.log('Hiding regular node labels');
      }
    });

    // Initial setup - make sure regular nodes start without labels
    cy.ready(() => {
      cy.nodes('.regular-node').forEach((node) => {
        node.style('label', '');
      });
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