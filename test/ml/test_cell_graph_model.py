"""Unit test for ml.models.cell_graph_model"""
import unittest
import torch
import dgl
import os
import yaml
from dgl.data.utils import load_graphs

from histocartography.ml import CellGraphModel
from histocartography.utils.graph import set_graph_on_cuda


IS_CUDA = torch.cuda.is_available()


class CGModelTestCase(unittest.TestCase):
    """CGModelTestCase class."""

    @classmethod
    def setUpClass(self):
        self.current_path = os.path.dirname(__file__)
        self.data_path = os.path.join(self.current_path, '..', 'data')
        self.graph_path = os.path.join(self.data_path, 'cell_graphs')
        self.graph_name = '283_dcis_4.bin'

    def test_cell_graph_model(self):
        """Test cell graph model."""

        # 1. Load a cell graph 
        graph, _ = load_graphs(os.path.join(self.graph_path, self.graph_name))
        graph = graph[0]
        graph.ndata['feat'] = torch.cat(
            (graph.ndata['feat'].float(),
            (graph.ndata['centroid']).float()),
            dim=1
        )
        graph = set_graph_on_cuda(graph) if IS_CUDA else graph
        node_dim = graph.ndata['feat'].shape[1]

        # 2. load config 
        config_fname = os.path.join(self.current_path, 'config', 'cg_model.yml')
        with open(config_fname, 'r') as file:
            config = yaml.load(file)

        model = CellGraphModel(
            gnn_params=config['gnn_params'],
            classification_params=config['classification_params'],
            node_dim=node_dim,
            num_classes=3
        )

        # 4. forward pass
        logits = model(graph)

        self.assertIsInstance(logits, torch.Tensor)
        self.assertEqual(logits.shape[0], 1)
        self.assertEqual(logits.shape[1], 3)  # 3 layers x 32 hidden dimension


    def test_pretrained_cell_graph_model(self):
        """Test cell graph model."""

        # 1. Load a cell graph 
        graph, _ = load_graphs(os.path.join(self.graph_path, self.graph_name))
        graph = graph[0]
        graph.ndata['feat'] = torch.cat(
            (graph.ndata['feat'].float(),
            (graph.ndata['centroid']).float()),
            dim=1
        )
        graph = set_graph_on_cuda(graph) if IS_CUDA else graph
        node_dim = graph.ndata['feat'].shape[1]

        # 2. load config 
        config_fname = os.path.join(self.current_path, 'config', 'cg_model.yml')
        with open(config_fname, 'r') as file:
            config = yaml.load(file)

        # model = CellGraphModel(
        #     gnn_params=config['gnn_params'],
        #     classification_params=config['classification_params'],
        #     node_dim=node_dim,
        #     num_classes=3
        # )

        local_path = os.path.join(os.path.dirname(__file__), CHECKPOINT_PATH, os.path.basename(model_path))
        download_box_link(model_path, local_path)
        self.model = torch.load(local_path)

        # 4. forward pass
        logits = model(graph)

        self.assertIsInstance(logits, torch.Tensor)
        self.assertEqual(logits.shape[0], 1)
        self.assertEqual(logits.shape[1], 3)  # 3 layers x 32 hidden dimension

    def tearDown(self):
        """Tear down the tests."""


if __name__ == "__main__":
    unittest.main()
