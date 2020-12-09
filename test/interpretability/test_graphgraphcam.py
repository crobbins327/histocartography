"""Unit test for interpretability.saliency_explainer.graph_gradcam_explainer"""
import unittest
import numpy as np
import cv2 
import torch 
import yaml
from copy import deepcopy
from dgl.data.utils import load_graphs

from histocartography.interpretability.saliency_explainer.graph_gradcam_explainer import GraphGradCAMExplainer

BASE_S3 = 's3://mlflow/'


class GraphGradCAMTestCase(unittest.TestCase):
    """GraphGradCAMTestCase class."""

    def setUp(self):
        """Setting up the test."""
    
    def test_graphgradcam(self):
        """Test Graph GradCAM.
        """

        # 1. load a cell graph
        cell_graph, label_dict = load_graphs('../data/283_dcis_4.bin')
        cell_graph = cell_graph[0]

        # 2. run the explainer
        explainer = GraphGradCAMExplainer(
            model_path=BASE_S3 + '29b7f5ee991e4a3e8b553b49a1c3c05a/artifacts/model_best_val_weighted_f1_score_0'
        )
        importance_scores, logits = explainer.process(cell_graph)

        # 3. print output 
        print('Number of nodes:', cell_graph.number_of_nodes())
        print('Number of edges:', cell_graph.number_of_edges())
        print('Node features:', cell_graph.ndata['feat'].shape)
        print('Node centroids:', cell_graph.ndata['centroid'].shape)
        print('Importance scores:', importance_scores.shape)
        print('Logits:', logits.shape)

    def tearDown(self):
        """Tear down the tests."""


if __name__ == "__main__":
    model = GraphGradCAMTestCase()
    model.test_graphgradcam()
