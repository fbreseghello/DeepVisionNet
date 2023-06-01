import matplotlib
matplotlib.use('Agg')  # Define o backend do Matplotlib como 'Agg'

import matplotlib.pyplot as plt
import tensorflow as tf

def train_model():
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train / 255.0
    x_test = x_test / 255.0
    x_train = x_train[..., tf.newaxis]
    x_test = x_test[..., tf.newaxis]
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    display_text = []

    for epoch in range(10):
        model.fit(x_train, y_train, epochs=1, validation_data=(x_test, y_test))
        loss, accuracy = model.evaluate(x_test, y_test)

        display_text.append(f"Epoch: {epoch + 1}\nLoss: {loss * 100:.2f}%\nAccuracy: {accuracy * 100:.2f}%")

    # Salva os resultados em um arquivo de texto
    with open("resultado.txt", "w") as file:
        for text in display_text:
            file.write(text + "\n")

    # Plota o gráfico de precisão
    accuracy_values = [float(text.split("\nAccuracy: ")[1][:-1]) for text in display_text]
    plt.plot(range(1, 11), accuracy_values)
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Training Accuracy')
    plt.savefig('accuracy_plot.png')

    # Plota o gráfico de perda
    loss_values = [float(text.split("\nLoss: ")[1][:-1]) for text in display_text]
    plt.figure()
    plt.plot(range(1, 11), loss_values)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss')
    plt.savefig('loss_plot.png')

train_model()
