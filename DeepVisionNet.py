import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tensorflow as tf

# Função para carregar o conjunto de dados MNIST e treinar o modelo
def train_model():
    # Carregar o conjunto de dados MNIST
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Normalizar os valores dos pixels para o intervalo [0, 1]
    x_train = x_train / 255.0
    x_test = x_test / 255.0

    # Adicionar uma dimensão de canal para as imagens (para uso em redes neurais convolucionais)
    x_train = x_train[..., tf.newaxis]
    x_test = x_test[..., tf.newaxis]

    # Construir o modelo
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    # Compilar o modelo
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # Atualizar a área de exibição
    display_text.set("Treinando o modelo...")
    window.update()

    # Configurar a barra de progresso
    progress_bar['value'] = 0
    progress_bar['maximum'] = 10

    # Treinar o modelo
    for epoch in range(10):
        model.fit(x_train, y_train, epochs=1, validation_data=(x_test, y_test))
        progress_bar['value'] = epoch + 1
        window.update()

        # Obter a loss e accuracy atualizadas
        loss, accuracy = model.evaluate(x_test, y_test)

        # Atualizar a área de exibição com as porcentagens
        display_text.set(f"Treinando o modelo...\nEpoch: {epoch + 1}\nLoss: {loss*100:.2f}%\nAccuracy: {accuracy*100:.2f}%")
        window.update()

    # Avaliar o modelo após o treinamento completo
    loss, accuracy = model.evaluate(x_test, y_test)
    messagebox.showinfo("Resultado", f"Loss: {loss}\nAccuracy: {accuracy}")

    # Atualizar a área de exibição
    display_text.set("Treinamento concluído.")
    window.update()

# Cria a janela principal
window = tk.Tk()
window.title("Treinamento do Modelo")
window.geometry("300x250")

# Cria a área de exibição
display_text = tk.StringVar()
display_label = tk.Label(window, textvariable=display_text)
display_label.pack(pady=20)

# Cria a barra de progresso
progress_bar = ttk.Progressbar(window, orient='horizontal', length=200, mode='determinate')
progress_bar.pack(pady=10)

# Cria o botão de treinamento
train_button = tk.Button(window, text="Treinar Modelo", command=train_model)
train_button.pack(pady=10)

# Inicia o loop da interface gráfica
window.mainloop()
