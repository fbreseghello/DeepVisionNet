import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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
    display_text.set("Treinando o modelo...")
    window.update()

 
    progress_bar['value'] = 0
    progress_bar['maximum'] = 10

 
    for epoch in range(10):
        model.fit(x_train, y_train, epochs=1, validation_data=(x_test, y_test))
        progress_bar['value'] = epoch + 1
        window.update()


        loss, accuracy = model.evaluate(x_test, y_test)


        display_text.set(f"Treinando o modelo...\nEpoch: {epoch + 1}\nLoss: {loss*100:.2f}%\nAccuracy: {accuracy*100:.2f}%")
        window.update()


    loss, accuracy = model.evaluate(x_test, y_test)
    messagebox.showinfo("Resultado", f"Loss: {loss}\nAccuracy: {accuracy}")


    display_text.set("Treinamento concluído.")
    window.update()

window = tk.Tk()
window.title("Treinamento do Modelo")
window.geometry("300x250")

display_text = tk.StringVar()
display_label = tk.Label(window, textvariable=display_text)
display_label.pack(pady=20)

progress_bar = ttk.Progressbar(window, orient='horizontal', length=200, mode='determinate')
progress_bar.pack(pady=10)

train_button = tk.Button(window, text="Treinar Modelo", command=train_model)
train_button.pack(pady=10)

window.mainloop()
