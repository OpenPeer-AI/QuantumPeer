import pytest
import torch
import numpy as np
from quantum_peer_model import QuantumPeerModel
from quantum_circuit import QuantumCircuit
from quantum_topology import ChernSimonsTopology
from quantum_gates import QuantumGate

@pytest.fixture
def model():
    return QuantumPeerModel(device="cpu")

@pytest.fixture
def quantum_circuit():
    topology = ChernSimonsTopology(depth=3)
    return QuantumCircuit(topology)

def test_circuit_initialization(quantum_circuit):
    """Test quantum circuit initialization"""
    assert quantum_circuit is not None
    assert len(quantum_circuit.gates) > 0
    gate_types = {gate.gate_type for gate in quantum_circuit.gates}
    required_gates = {"H", "CNOT", "Phase", "X", "Z"}
    assert required_gates.issubset(gate_types)

def test_quantum_evolution(quantum_circuit):
    """Test quantum state evolution"""
    initial_state = np.zeros(quantum_circuit.topology.dimension)
    initial_state[0] = 1
    
    final_state = quantum_circuit.evolve(initial_state)
    assert isinstance(final_state, np.ndarray)
    assert np.allclose(np.sum(np.abs(final_state) ** 2), 1)

def test_gate_operations():
    """Test individual quantum gates"""
    gates = {
        "H": QuantumGate("H"),
        "X": QuantumGate("X"),
        "Z": QuantumGate("Z"),
        "Phase": QuantumGate("Phase"),
        "CNOT": QuantumGate("CNOT")
    }
    
    state = np.array([1, 0])
    h_state = gates["H"].apply(state, None)
    expected = np.array([1, 1]) / np.sqrt(2)
    assert np.allclose(h_state, expected)
    
    x_state = gates["X"].apply(state, None)
    assert np.allclose(x_state, np.array([0, 1]))

@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
def test_model_gpu_support():
    """Test GPU support when available"""
    model = QuantumPeerModel(device="cuda")
    assert model.llm_interface.model.device.type == "cuda"
    response = model.generate("Test prompt")
    assert isinstance(response, str)

def test_topology_scaling():
    """Test topology scaling with different depths"""
    depths = [2, 3, 4]
    for depth in depths:
        topology = ChernSimonsTopology(depth)
        assert topology.dimension == 2 ** depth
        assert len(topology.connections) == (depth * (depth - 1)) // 2

def test_model_generation(model):
    """Test text generation with quantum enhancement"""
    prompt = "Explain quantum computing in"
    response = model.generate(
        prompt,
        max_length=50,
        quantum_params={"gates": ["H", "CNOT"]}
    )
    assert isinstance(response, str)
    assert len(response) > len(prompt)