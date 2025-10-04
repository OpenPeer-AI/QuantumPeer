from typing import Optional
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class OpenPeerLLMInterface:
    def __init__(
        self,
        model_path: str,
        checkpoint: str,
        device: str
    ):
        self.device = device
        self.model_path = f"{model_path}/{checkpoint}"
        self.model = None
        self.tokenizer = None
        self._load_model()
        
    def _load_model(self):
        """Load the model and tokenizer"""
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path
            ).to(self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
        
    def generate(
        self,
        prompt: str,
        quantum_state: Optional[np.ndarray] = None,
        max_length: int = 100
    ) -> str:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not properly initialized")
            
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        if quantum_state is not None:
            self._apply_quantum_state(quantum_state)
            
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
    def _apply_quantum_state(self, quantum_state: np.ndarray):
        if self.model is None:
            return
            
        state_magnitude = np.abs(quantum_state) ** 2
        attention_modifier = torch.tensor(
            state_magnitude, 
            device=self.device
        ).float()
        
        with torch.no_grad():
            for layer in self.model.transformer.h[:1]:
                if hasattr(layer, 'attn'):
                    attention = layer.attn
                    if hasattr(attention, 'c_attn'):
                        weights = attention.c_attn.weight
                        scale = attention_modifier[:weights.size(0)].reshape(-1, 1)
                        attention.c_attn.weight.data *= scale