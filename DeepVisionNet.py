"""
DeepVisionNet - MNIST Classification with Convolutional Neural Networks

A modern implementation of CNN for MNIST digit classification with extensive
features including model checkpointing, early stopping, and comprehensive logging.
"""

import argparse
import logging
import os
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # Set backend for non-interactive mode

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DeepVisionNet:
    """Deep learning model for MNIST digit classification."""
    
    def __init__(self, config=None):
        """
        Initialize the DeepVisionNet model.
        
        Args:
            config (dict): Configuration parameters for the model
        """
        self.config = config or self._default_config()
        self.model = None
        self.history = None
        
    def _default_config(self):
        """Return default configuration."""
        return {
            'epochs': 20,
            'batch_size': 128,
            'learning_rate': 0.001,
            'validation_split': 0.1,
            'conv_filters': [32, 64],
            'dense_units': 128,
            'dropout_rate': 0.5,
            'early_stopping_patience': 5,
            'output_dir': 'results'
        }
    
    def load_data(self):
        """
        Load and preprocess MNIST dataset.
        
        Returns:
            tuple: (x_train, y_train), (x_test, y_test)
        """
        logger.info("Loading MNIST dataset...")
        mnist = keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        
        # Normalize pixel values to [0, 1]
        x_train = x_train.astype('float32') / 255.0
        x_test = x_test.astype('float32') / 255.0
        
        # Reshape for CNN input (add channel dimension)
        x_train = np.expand_dims(x_train, -1)
        x_test = np.expand_dims(x_test, -1)
        
        logger.info(f"Training samples: {x_train.shape[0]}")
        logger.info(f"Test samples: {x_test.shape[0]}")
        logger.info(f"Image shape: {x_train.shape[1:]}")
        
        return (x_train, y_train), (x_test, y_test)
    
    def build_model(self, input_shape=(28, 28, 1), num_classes=10):
        """
        Build the CNN architecture.
        
        Args:
            input_shape (tuple): Shape of input images
            num_classes (int): Number of output classes
            
        Returns:
            keras.Model: Compiled model
        """
        logger.info("Building model architecture...")
        
        model = keras.Sequential([
            layers.Input(shape=input_shape),
            
            # First convolutional block
            layers.Conv2D(self.config['conv_filters'][0], (3, 3), 
                         activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            # Second convolutional block
            layers.Conv2D(self.config['conv_filters'][1], (3, 3), 
                         activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            # Dense layers
            layers.Flatten(),
            layers.Dense(self.config['dense_units'], activation='relu'),
            layers.Dropout(self.config['dropout_rate']),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        # Compile model
        optimizer = keras.optimizers.Adam(learning_rate=self.config['learning_rate'])
        model.compile(
            optimizer=optimizer,
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        logger.info(f"Model built with {model.count_params():,} parameters")
        
        return model
    
    def get_callbacks(self):
        """
        Create training callbacks.
        
        Returns:
            list: List of Keras callbacks
        """
        output_dir = Path(self.config['output_dir'])
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        callback_list = [
            callbacks.ModelCheckpoint(
                filepath=output_dir / f'model_best_{timestamp}.keras',
                monitor='val_accuracy',
                save_best_only=True,
                mode='max',
                verbose=1
            ),
            callbacks.EarlyStopping(
                monitor='val_loss',
                patience=self.config['early_stopping_patience'],
                restore_best_weights=True,
                verbose=1
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7,
                verbose=1
            ),
            callbacks.CSVLogger(
                output_dir / f'training_log_{timestamp}.csv'
            )
        ]
        
        return callback_list
    
    def train(self, x_train, y_train, x_val=None, y_val=None):
        """
        Train the model.
        
        Args:
            x_train: Training data
            y_train: Training labels
            x_val: Validation data (optional)
            y_val: Validation labels (optional)
            
        Returns:
            History: Training history
        """
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
        
        logger.info("Starting training...")
        
        # Prepare validation data
        if x_val is None:
            validation_split = self.config['validation_split']
            validation_data = None
        else:
            validation_split = 0.0
            validation_data = (x_val, y_val)
        
        # Train model
        self.history = self.model.fit(
            x_train, y_train,
            batch_size=self.config['batch_size'],
            epochs=self.config['epochs'],
            validation_split=validation_split,
            validation_data=validation_data,
            callbacks=self.get_callbacks(),
            verbose=1
        )
        
        logger.info("Training completed!")
        return self.history
    
    def evaluate(self, x_test, y_test):
        """
        Evaluate model on test data.
        
        Args:
            x_test: Test data
            y_test: Test labels
            
        Returns:
            dict: Evaluation metrics
        """
        logger.info("Evaluating model on test data...")
        
        test_loss, test_accuracy = self.model.evaluate(x_test, y_test, verbose=0)
        
        metrics = {
            'test_loss': test_loss,
            'test_accuracy': test_accuracy
        }
        
        logger.info(f"Test Loss: {test_loss:.4f}")
        logger.info(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        
        return metrics
    
    def save_model(self, filepath=None):
        """
        Save the trained model.
        
        Args:
            filepath (str): Path to save the model
        """
        if filepath is None:
            output_dir = Path(self.config['output_dir'])
            output_dir.mkdir(exist_ok=True)
            filepath = output_dir / 'model_final.keras'
        
        self.model.save(filepath)
        logger.info(f"Model saved to {filepath}")
    
    def plot_history(self, save_path=None):
        """
        Plot training history.
        
        Args:
            save_path (str): Directory to save plots
        """
        if self.history is None:
            logger.warning("No training history available")
            return
        
        if save_path is None:
            save_path = Path(self.config['output_dir'])
        else:
            save_path = Path(save_path)
        
        save_path.mkdir(exist_ok=True)
        
        # Plot accuracy
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 2, 1)
        plt.plot(self.history.history['accuracy'], label='Training Accuracy')
        plt.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.title('Model Accuracy')
        plt.legend()
        plt.grid(True)
        
        # Plot loss
        plt.subplot(1, 2, 2)
        plt.plot(self.history.history['loss'], label='Training Loss')
        plt.plot(self.history.history['val_loss'], label='Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Model Loss')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path / 'training_history.png', dpi=300, bbox_inches='tight')
        logger.info(f"Training plots saved to {save_path / 'training_history.png'}")
        plt.close()
    
    def save_summary(self, filepath=None):
        """
        Save model summary to file.
        
        Args:
            filepath (str): Path to save summary
        """
        if filepath is None:
            output_dir = Path(self.config['output_dir'])
            output_dir.mkdir(exist_ok=True)
            filepath = output_dir / 'model_summary.txt'
        
        with open(filepath, 'w') as f:
            self.model.summary(print_fn=lambda x: f.write(x + '\n'))
        
        logger.info(f"Model summary saved to {filepath}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='DeepVisionNet - MNIST Classification'
    )
    parser.add_argument('--epochs', type=int, default=20,
                       help='Number of training epochs (default: 20)')
    parser.add_argument('--batch-size', type=int, default=128,
                       help='Batch size for training (default: 128)')
    parser.add_argument('--learning-rate', type=float, default=0.001,
                       help='Learning rate (default: 0.001)')
    parser.add_argument('--output-dir', type=str, default='results',
                       help='Output directory for results (default: results)')
    
    args = parser.parse_args()
    
    # Configuration
    config = {
        'epochs': args.epochs,
        'batch_size': args.batch_size,
        'learning_rate': args.learning_rate,
        'validation_split': 0.1,
        'conv_filters': [32, 64],
        'dense_units': 128,
        'dropout_rate': 0.5,
        'early_stopping_patience': 5,
        'output_dir': args.output_dir
    }
    
    try:
        # Initialize model
        dvn = DeepVisionNet(config)
        
        # Load data
        (x_train, y_train), (x_test, y_test) = dvn.load_data()
        
        # Build model
        dvn.build_model()
        dvn.save_summary()
        
        # Train model
        dvn.train(x_train, y_train, x_test, y_test)
        
        # Evaluate model
        metrics = dvn.evaluate(x_test, y_test)
        
        # Save results
        dvn.save_model()
        dvn.plot_history()
        
        logger.info("="*50)
        logger.info("Training completed successfully!")
        logger.info(f"Final Test Accuracy: {metrics['test_accuracy']*100:.2f}%")
        logger.info(f"Results saved to: {config['output_dir']}/")
        logger.info("="*50)
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
