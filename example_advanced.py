"""
Exemplo de uso avançado do DeepVisionNet com data augmentation e configuração customizada.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importar o módulo
sys.path.append(str(Path(__file__).parent))

from DeepVisionNet import DeepVisionNet
import tensorflow as tf
from tensorflow import keras


def create_data_augmentation():
    """
    Cria um pipeline de data augmentation para melhorar a generalização.
    
    Returns:
        keras.Sequential: Pipeline de augmentação
    """
    return keras.Sequential([
        keras.layers.RandomRotation(0.1),
        keras.layers.RandomTranslation(height_factor=0.1, width_factor=0.1),
        keras.layers.RandomZoom(0.1),
    ])


def advanced_training_example():
    """Exemplo de treinamento avançado com data augmentation."""
    
    # Configuração customizada
    config = {
        'epochs': 30,
        'batch_size': 64,
        'learning_rate': 0.0005,
        'validation_split': 0.15,
        'conv_filters': [64, 128],
        'dense_units': 256,
        'dropout_rate': 0.4,
        'early_stopping_patience': 7,
        'output_dir': 'results_advanced'
    }
    
    print("="*60)
    print("DeepVisionNet - Treinamento Avançado")
    print("="*60)
    
    # Inicializa modelo
    dvn = DeepVisionNet(config)
    
    # Carrega dados
    (x_train, y_train), (x_test, y_test) = dvn.load_data()
    
    # Cria modelo com data augmentation
    dvn.build_model()
    
    # Opcional: Adicionar data augmentation manualmente
    # data_augmentation = create_data_augmentation()
    # x_train_aug = data_augmentation(x_train, training=True)
    
    # Treina
    dvn.train(x_train, y_train, x_test, y_test)
    
    # Avalia
    metrics = dvn.evaluate(x_test, y_test)
    
    # Salva resultados
    dvn.save_model()
    dvn.plot_history()
    dvn.save_summary()
    
    print("\n" + "="*60)
    print(f"Treinamento concluído!")
    print(f"Acurácia Final: {metrics['test_accuracy']*100:.2f}%")
    print(f"Loss Final: {metrics['test_loss']:.4f}")
    print("="*60)
    
    return dvn, metrics


def predict_example(model_path='results/model_final.keras'):
    """
    Exemplo de como fazer predições com um modelo salvo.
    
    Args:
        model_path (str): Caminho para o modelo salvo
    """
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Carrega modelo
    model = keras.models.load_model(model_path)
    
    # Carrega dados de teste
    mnist = keras.datasets.mnist
    (_, _), (x_test, y_test) = mnist.load_data()
    
    # Preprocessa
    x_test = x_test.astype('float32') / 255.0
    x_test = np.expand_dims(x_test, -1)
    
    # Seleciona algumas imagens aleatórias
    indices = np.random.choice(len(x_test), 9, replace=False)
    
    # Faz predições
    predictions = model.predict(x_test[indices])
    predicted_labels = np.argmax(predictions, axis=1)
    
    # Visualiza resultados
    plt.figure(figsize=(10, 10))
    for i, idx in enumerate(indices):
        plt.subplot(3, 3, i + 1)
        plt.imshow(x_test[idx].squeeze(), cmap='gray')
        plt.title(f"Real: {y_test[idx]}, Pred: {predicted_labels[i]}")
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('predictions_example.png', dpi=150)
    print("Predições salvas em 'predictions_example.png'")


if __name__ == "__main__":
    # Executa treinamento avançado
    model, metrics = advanced_training_example()
    
    # Demonstra predições (opcional)
    # predict_example()
