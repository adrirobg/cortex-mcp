"""Collaborative Intelligence Module for Phase 2.7.

This module implements hybrid collaborative intelligence that combines
the deterministic reliability of the Motor de Estrategias with the
adaptive intelligence of Claude for enhanced strategic analysis.

Key Components:
- WorkflowController: Orchestrates collaborative multi-step workflows
- DelegationEngine: Handles delegation to Claude intelligence
- CollaborationDetector: Identifies optimal collaboration points
- ResultIntegrator: Merges Claude refinements with deterministic analysis
"""

from .workflow_controller import CollaborativeWorkflowController
from .delegation_engine import DelegationEngine
from .collaboration_detector import CollaborationDetector
from .result_integrator import ResultIntegrator

__all__ = [
    "CollaborativeWorkflowController",
    "DelegationEngine", 
    "CollaborationDetector",
    "ResultIntegrator"
]