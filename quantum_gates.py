import numpy as np
from typing import Any

class QuantumGate:
    def __init__(self, gate_type: str):
        self.gate_type = gate_type
        self.matrix = self._initialize_matrix()
        
    def _initialize_matrix(self) -> np.ndarray:
        """Initialize gate unitary matrix"""
        if self.gate_type == "H":
            return np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        elif self.gate_type == "CNOT":
            return np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 0, 1],
                           [0, 0, 1, 0]])
        elif self.gate_type == "Phase":
            return np.array([[1, 0], [0, 1j]])
        elif self.gate_type == "X":
            return np.array([[0, 1], [1, 0]])
        elif self.gate_type == "Z":
            return np.array([[1, 0], [0, -1]])
        else:
            raise ValueError(f"Unknown gate type: {self.gate_type}")
            
    def apply(self, state: np.ndarray, topology: Any) -> np.ndarray:
        """Apply gate to quantum state"""
        if self.gate_type == "H":
            return self._apply_single_qubit(state)
        elif self.gate_type == "CNOT":
            return self._apply_two_qubit(state)
        else:
            return self._apply_single_qubit(state)

    def _apply_single_qubit(self, state: np.ndarray) -> np.ndarray:
        if len(state.shape) == 1:
            state_2d = state.reshape(-1, 2)
            result = np.dot(state_2d, self.matrix.T)
            return result.flatten()
        return np.dot(state, self.matrix.T)

    def _apply_two_qubit(self, state: np.ndarray) -> np.ndarray:
        return np.dot(state.reshape(-1, 4), self.matrix.T).flatten()