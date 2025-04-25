import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import create_workflow
import json
from pathlib import Path

def visualize_workflow():
    """Generate a visualization of the workflow graph"""
    # Create the workflow
    workflow = create_workflow()
    
    # Get the graph definition
    graph_def = workflow.get_graph()
    
    # Convert to JSON for visualization
    graph_json = json.dumps(graph_def, indent=2)
    
    # Save to file
    output_dir = Path("utils/output")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "workflow_graph.json", "w") as f:
        f.write(graph_json)
    
    print(f"Graph definition saved to {output_dir / 'workflow_graph.json'}")
    print("You can visualize this JSON using tools like https://jsoncrack.com/ or any graph visualization library")
    
    # Print a simple text representation of the graph
    print("\nWorkflow Graph Structure:")
    print("-------------------------")
    
    # Extract nodes and edges
    nodes = graph_def.get("nodes", [])
    edges = graph_def.get("edges", [])
    
    print(f"Nodes ({len(nodes)}):")
    for node in nodes:
        print(f"  - {node}")
    
    print(f"\nEdges ({len(edges)}):")
    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        print(f"  - {source} → {target}")

if __name__ == "__main__":
    visualize_workflow()