"""
Testes unitários para DeepVisionNet.

Execute com: pytest test_deepvisionnet.py -v
"""

import pytest
import numpy as np
import tensorflow as tf
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from DeepVisionNet import DeepVisionNet


class TestDeepVisionNet:
    """Classe de testes para DeepVisionNet."""
    
    @pytest.fixture
    def config(self):
        """Configuração de teste."""
        return {
            'epochs': 2,
            'batch_size': 32,
            'learning_rate': 0.001,
            'validation_split': 0.1,
            'conv_filters': [16, 32],
            'dense_units': 64,
            'dropout_rate': 0.3,
            'early_stopping_patience': 2,
            'output_dir': 'test_results'
        }
    
    @pytest.fixture
    def dvn(self, config):
        """Instância do DeepVisionNet para testes."""
        return DeepVisionNet(config)
    
    def test_initialization(self, dvn, config):
        """Testa inicialização do modelo."""
        assert dvn.config == config
        assert dvn.model is None
        assert dvn.history is None
    
    def test_default_config(self):
        """Testa configuração padrão."""
        dvn = DeepVisionNet()
        assert dvn.config['epochs'] == 20
        assert dvn.config['batch_size'] == 128
        assert dvn.config['learning_rate'] == 0.001
    
    def test_load_data(self, dvn):
        """Testa carregamento de dados."""
        (x_train, y_train), (x_test, y_test) = dvn.load_data()
        
        # Verifica shapes
        assert x_train.shape == (60000, 28, 28, 1)
        assert x_test.shape == (10000, 28, 28, 1)
        assert y_train.shape == (60000,)
        assert y_test.shape == (10000,)
        
        # Verifica normalização
        assert x_train.min() >= 0.0
        assert x_train.max() <= 1.0
        
        # Verifica tipo
        assert x_train.dtype == np.float32
    
    def test_build_model(self, dvn):
        """Testa construção do modelo."""
        model = dvn.build_model()
        
        # Verifica se o modelo foi criado
        assert model is not None
        assert dvn.model is not None
        
        # Verifica input e output shapes
        assert model.input_shape == (None, 28, 28, 1)
        assert model.output_shape == (None, 10)
        
        # Verifica número de camadas
        assert len(model.layers) > 5
    
    def test_model_compilation(self, dvn):
        """Testa compilação do modelo."""
        dvn.build_model()
        
        # Verifica optimizer
        assert isinstance(dvn.model.optimizer, tf.keras.optimizers.Adam)
        
        # Verifica loss
        assert dvn.model.loss == 'sparse_categorical_crossentropy'
    
    def test_get_callbacks(self, dvn):
        """Testa criação de callbacks."""
        dvn.build_model()
        callbacks_list = dvn.get_callbacks()
        
        # Verifica se callbacks foram criados
        assert len(callbacks_list) == 4
        
        # Verifica tipos
        callback_types = [type(cb).__name__ for cb in callbacks_list]
        assert 'ModelCheckpoint' in callback_types
        assert 'EarlyStopping' in callback_types
        assert 'ReduceLROnPlateau' in callback_types
        assert 'CSVLogger' in callback_types
    
    def test_training_small_sample(self, dvn):
        """Testa treinamento com amostra pequena."""
        # Carrega dados
        (x_train, y_train), (x_test, y_test) = dvn.load_data()
        
        # Usa apenas uma pequena amostra para teste rápido
        x_train_small = x_train[:1000]
        y_train_small = y_train[:1000]
        x_test_small = x_test[:200]
        y_test_small = y_test[:200]
        
        # Constrói e treina
        dvn.build_model()
        history = dvn.train(x_train_small, y_train_small, x_test_small, y_test_small)
        
        # Verifica se o treinamento ocorreu
        assert history is not None
        assert 'accuracy' in history.history
        assert 'loss' in history.history
        assert len(history.history['accuracy']) <= dvn.config['epochs']
    
    def test_evaluate(self, dvn):
        """Testa avaliação do modelo."""
        # Prepara dados
        (x_train, y_train), (x_test, y_test) = dvn.load_data()
        x_train_small = x_train[:500]
        y_train_small = y_train[:500]
        x_test_small = x_test[:100]
        y_test_small = y_test[:100]
        
        # Treina modelo
        dvn.build_model()
        dvn.train(x_train_small, y_train_small, x_test_small, y_test_small)
        
        # Avalia
        metrics = dvn.evaluate(x_test_small, y_test_small)
        
        # Verifica métricas
        assert 'test_loss' in metrics
        assert 'test_accuracy' in metrics
        assert 0.0 <= metrics['test_accuracy'] <= 1.0
        assert metrics['test_loss'] >= 0.0
    
    def test_save_model(self, dvn, tmp_path):
        """Testa salvamento do modelo."""
        dvn.build_model()
        
        # Salva modelo
        model_path = tmp_path / "test_model.keras"
        dvn.save_model(model_path)
        
        # Verifica se o arquivo foi criado
        assert model_path.exists()
    
    def test_prediction_shape(self, dvn):
        """Testa shape das predições."""
        dvn.build_model()
        
        # Cria dados de teste
        x_test = np.random.rand(10, 28, 28, 1).astype('float32')
        
        # Faz predições
        predictions = dvn.model.predict(x_test)
        
        # Verifica shape
        assert predictions.shape == (10, 10)
        
        # Verifica se são probabilidades (soma ~1)
        assert np.allclose(predictions.sum(axis=1), 1.0, atol=1e-5)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
