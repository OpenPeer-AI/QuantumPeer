import numpy as np
from quantum_circuit import QuantumCircuit
from quantum_topology import ChernSimonsTopology

class CircuitVisualizer:
    def __init__(self, circuit: QuantumCircuit):
        self.circuit = circuit
        
    def draw_circuit(self) -> str:
        """Generate ASCII visualization of quantum circuit"""
        output = []
        output.append("Quantum Circuit:")
        output.append("-" * 40)
        
        for i, gate in enumerate(self.circuit.gates):
            output.append(f"Gate {i}: {gate.gate_type}")
            if gate.gate_type == "CNOT":
                output.append("  |control⟩ ──●──")
                output.append("            │")
                output.append("  |target⟩  ─⊕─")
            else:
                output.append(f"  |ψ⟩ ──{gate.gate_type}──")
            output.append("")
            
        return "\n".join(output)
        
    def draw_topology(self) -> str:
        """Generate ASCII visualization of topology"""
        output = []
        output.append("Topology Layout:")
        output.append("-" * 40)
        
        for i in range(self.circuit.topology.depth):
            connections = [j for j in range(self.circuit.topology.depth) 
                         if (i,j) in self.circuit.topology.connections]
            line = [f"Q{i}"]
            for j in range(self.circuit.topology.depth):
                if j in connections:
                    line.append("──●──")
                else:
                    line.append("─────")
            output.append("".join(line))
            
        return "\n".join(output)
        
    def get_state_visualization(self, state: np.ndarray) -> str:
        """Visualize quantum state"""
        output = []
        output.append("Quantum State:")
        output.append("-" * 40)
        
        # Show amplitudes and probabilities
        for i, amplitude in enumerate(state):
            prob = np.abs(amplitude) ** 2
            binary = format(i, f'0{self.circuit.topology.depth}b')
            output.append(f"|{binary}⟩: {amplitude:.3f} (Prob: {prob:.3f})")
            
        return "\n".join(output)