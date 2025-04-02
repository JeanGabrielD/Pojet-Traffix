# imports

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, LSTM, Input, Dropout, Bidirectional, Masking, RepeatVector, TimeDistributed
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.preprocessing.sequence import pad_sequences
from enum import Enum


scaler = MinMaxScaler(feature_range=(0, 1))

class Models(Enum):
    LSTM = 1
    ENCODER_DECODER = 2
    BIDIRECTIONNEL = 3


def split_dataset(dataset):
    # Split into trainX and trainY
    trainX = dataset[:, :-1, :]  # All timestamps except the last
    trainY = dataset[:, 1:, :]   # All timestamps except the first (next point)
    return trainX, trainY

    # split the dataset into X and Y arrays where X are t and Y t+1
def split_dataset_window(dataset, timesteps=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - timesteps):
        dataX.append(dataset[i:i+timesteps])  # Use 'timesteps' points as input
        dataY.append(dataset[i+timesteps])   # Predict the next point
    return np.array(dataX), np.array(dataY)

from itertools import islice

def pad_or_trim(features, seq_length):
    features = list(features)  # Assurer une liste
    if len(features) < seq_length:
        # Padding avec (0, 0)
        features += [(0.0, 0.0)] * (seq_length - len(features))
    else:
        # Trimming
        features = features[:seq_length]

    return np.array(features, dtype=np.float32)  # Retourner un tableau NumPy propre

# preprocessing
def preprocessing(file, ratio_train=0.8, seq_length=None):
    # load dataset
    dataframe = pd.read_csv(file)
    
    # Group by trajet_id while keeping the sequence structure
    grouped = dataframe.groupby('trajet_id')
    
    # Initialize lists to store sequences and their IDs
    sequences = []
    trajet_ids = []
    
    for trajet_id, group in grouped:
        # Get coordinates for this trajectory
        coords = group[['latitude', 'longitude']].values
        sequences.append(coords)
        trajet_ids.append(trajet_id)
    
    # Determine the maximum sequence length
    if seq_length is None:
        seq_length = max(len(seq) for seq in sequences)
    
    # Pad or trim sequences to the same length
    padded_sequences = []
    for seq in sequences:
        if len(seq) < seq_length:
            # Pad with zeros
            padded = np.pad(seq, ((0, seq_length - len(seq)), (0, 0)), 
                          mode='constant', constant_values=0)
        else:
            # Trim to seq_length
            padded = seq[:seq_length]
        padded_sequences.append(padded)
    
    # Convert to numpy array
    dataset = np.array(padded_sequences)
    
    # Normalize each feature separately across all sequences
    num_sequences, _, num_features = dataset.shape
    
    # Reshape for normalization (combine sequence and time dimensions)
    reshaped_data = dataset.reshape(-1, num_features)
    
    # Apply MinMaxScaler
    scaled_data = scaler.fit_transform(reshaped_data)
    
    # Reshape back to original structure
    dataset = scaled_data.reshape(num_sequences, seq_length, num_features)
    
    # Split dataset into train and test sets
    train_size = int(len(dataset) * ratio_train)
    test_size = len(dataset) - train_size
    trainset = dataset[:train_size]
    testset = dataset[train_size:]
    
    # Also split the trajet_ids for reference
    train_ids = trajet_ids[:train_size]
    test_ids = trajet_ids[train_size:]
    
    # Split into input and target
    trainX, trainY = split_dataset(trainset)
    testX, testY = split_dataset(testset)
    
    return trainX, trainY, testX, testY, train_ids, test_ids
# implementation        
def simple_lstm_model(trainX,trainY, lstm_layers = 1, lstm_cells=64, epochs= 50, batch_size=64, validation_split=0.1):

    inputs_x = Input(shape=(trainX.shape[1], trainX.shape[2]))
    # Add the Masking layer
    masked_x = Masking(mask_value=0.0)(inputs_x)
    # Add the LSTM layer to ignore (0,0) padded values
    outputs_y = LSTM(lstm_cells, return_sequences=True)(masked_x)
    for _ in range(lstm_layers-1):
        outputs_y = LSTM(lstm_cells, return_sequences=True)(outputs_y)
    # Add the Dense output layer
    outputs_y = Dense(trainX.shape[2])(outputs_y)
    # create the model
    model = Model(inputs=inputs_x, outputs=outputs_y)

    model.compile(loss='mse', optimizer='adam')
    history = model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, validation_split=validation_split, verbose=1)

    return model, history

def encoder_decoder_model(trainX,trainY, encoder_lstm_cells=64, decoder_lstm_cells=64, epochs= 50, batch_size=64, validation_split=0.1):

    # Définir l'encodeur
    encoder_inputs = Input(shape=(trainX.shape[1], trainX.shape[2]))
    encoder_lstm = LSTM(encoder_lstm_cells, return_state=True)
    encoder_outputs, state_h, state_c = encoder_lstm(encoder_inputs)

    # Définir le décodeur
    decoder_inputs = Input(shape=(trainX.shape[1], trainX.shape[2]))
    decoder_lstm = LSTM(decoder_lstm_cells, return_sequences=True, return_state=True)
    decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=[state_h, state_c])
    decoder_dense = Dense(trainX.shape[2])  # Prédire latitude et longitude
    decoder_outputs = decoder_dense(decoder_outputs)

    # Créer le modèle
    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
    # Compilation du modèle 
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])


    history = model.fit(
        [trainX, trainY], trainY,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split
    )

    return model, history


def encoder_decoder_bidirectional_model(trainX,trainY, encoder_lstm_cells=64, decoder_lstm_cells=64, epochs= 50, batch_size=64, validation_split=0.1):

    # 6. Construction du modèle encodeur-décodeur bidirectionnel
    input_shape = (trainX.shape[1], trainX.shape[2])  # Forme d'entrée : (séquence, caractéristiques)
    output_shape = (trainY.shape[1], trainY.shape[2])  # Forme de sortie : (prédiction, caractéristiques)
    
    # Encodeur
    model = Sequential()
    model.add(Bidirectional(LSTM(encoder_lstm_cells, return_sequences=False, input_shape=input_shape)))  # Couche LSTM bidirectionnelle
    model.add(RepeatVector(output_shape[0]))  # Répéter le vecteur pour le décodeur

    # Décodeur
    model.add(Bidirectional(LSTM(decoder_lstm_cells, return_sequences=True)))  # Couche LSTM bidirectionnelle
    model.add(TimeDistributed(Dense(output_shape[1])))  # Couche dense pour chaque pas de temps

    # Compilation du modèle
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

    # 7. Entraînement du modèle
    history = model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, validation_split=validation_split)


    return model, history

# predictions

def prediction(model, testX=None, testY=None):
    # For Sequential models or single-input models
    if isinstance(model, Sequential) or not isinstance(model.input, list):
        testPredict = model.predict(testX)
    else:
        # For models with multiple inputs (like encoder-decoder)
        target_length = model.input[0].shape[1]  # Get expected length from model
        testX_pad = testX[:, :target_length, :]
        testY_pad = testY[:, :target_length, :]
        testPredict = model.predict([testX_pad, testY_pad])
    return testPredict

def calculate_rmse(model, history, trainX, trainY, testY, testPredict):
    # For Sequential models or single-input models
    if isinstance(model, Sequential) or not isinstance(model.input, list):
        trainPredict = model.predict(trainX)
    else:
        # For models with multiple inputs (like encoder-decoder)
        trainPredict = model.predict([trainX, trainY])

    # inverse normalisation
    # Reshape the predictions and true values to 2D
    trainPredict_reshaped = trainPredict.reshape(-1, trainPredict.shape[-1])
    trainY_reshaped = trainY.reshape(-1, trainY.shape[-1])
    testPredict_reshaped = testPredict.reshape(-1, testPredict.shape[-1])
    testY_reshaped = testY.reshape(-1, testY.shape[-1])

    # Apply inverse transformation
    trainPredict_inverse = scaler.inverse_transform(trainPredict_reshaped)
    trainY_inverse = scaler.inverse_transform(trainY_reshaped)
    testPredict_inverse = scaler.inverse_transform(testPredict_reshaped)
    testY_inverse = scaler.inverse_transform(testY_reshaped)

    # Reshape back to 3D
    trainPredict = trainPredict_inverse.reshape(trainPredict.shape)
    trainY = trainY_inverse.reshape(trainY.shape)
    testPredict = testPredict_inverse.reshape(testPredict.shape)
    testY = testY_inverse.reshape(testY.shape)

    # Calculate RMSE
    # Reshape 3D arrays to 2D
    trainY_flat = trainY.reshape(-1, trainY.shape[-1])
    trainPredict_flat = trainPredict.reshape(-1, trainPredict.shape[-1])
    testY_flat = testY.reshape(-1, testY.shape[-1])
    testPredict_flat = testPredict.reshape(-1, testPredict.shape[-1])
    min_len = min(len(testY_flat), len(testPredict_flat))
    testY_flat = testY_flat[:min_len]
    testPredict_flat = testPredict_flat[:min_len]

    # Calculate RMSE
    trainScore = history.history['loss'][-1]
    print('Train Score: %.5f MSE' % (trainScore))

    testScore = np.sqrt(mean_squared_error(testY_flat, testPredict_flat))
    print('Test Score: %.2f RMSE' % (testScore))

    return trainScore, testScore

# %%
# plotting

def plotting(testY, testPredict, max_points=100):
    # Flatten the data to 2D
    testY_flat = testY.reshape(-1, testY.shape[-1])
    testPredict_flat = testPredict.reshape(-1, testPredict.shape[-1])

    # Identify rows where all elements are [0.0, 0.0]
    mask = np.all(testY_flat == 0.0, axis=1)
    # Remove rows matching the condition
    testY_flat = np.delete(testY_flat, np.where(mask), axis=0)

    # Identify rows where all elements are [0.0, 0.0]
    mask = np.all(testPredict_flat == 0.0, axis=1)
    # Remove rows matching the condition
    testPredict_flat = np.delete(testY_flat, np.where(mask), axis=0)

    # Plot True vs Predicted Latitude (first 100 values, with shifted testY)
    fig, axs = plt.subplots(2)
    axs[0].plot(testY_flat[1:max_points, 0], label='True Latitude', alpha=0.8)
    axs[0].plot(testPredict_flat[:max_points, 0], label='Predicted Latitude', alpha=0.8)
    axs[0].legend()
 

    # Plot True vs Predicted Longitude (first 100 values, with shifted testY)
    axs[1].plot(testY_flat[1:max_points, 1], label='True Longitude', alpha=0.8)
    axs[1].plot(testPredict_flat[:max_points, 1], label='Predicted Longitude', alpha=0.8)
    axs[1].legend()
    fig.savefig("images/predict_plot")  # save figure into image
    plt.show()


# %%
# savingCSV
def saveCSV(testY, testPredict):
    for i in range(testY.shape[0]):
        df = pd.DataFrame(testY[i], columns=['latitude', 'longitude'])
        df.to_csv(f"datasets/predictions/true_{i}.csv", index=False)
        df = pd.DataFrame(testPredict[i], columns=['latitude', 'longitude'])
        df.to_csv(f"datasets/predictions/predicted_{i}.csv", index=False)
    df.to_csv("results.csv", index=False)


# courbe d'apprentissage
def plotting_courbe_apprentissage(history):
        plt.figure(figsize=(10, 5))
        
        # Courbe de loss
        plt.plot(history.history['loss'], label='Train Loss')
        #plt.plot(history.history['val_loss'], label='Validation Loss')
        
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.title('Training Progress')
        plt.legend()
        plt.grid()
        plt.savefig("images/courbe_apprentissage")  # save figure into image

        plt.show()

def plot_sequences(testY, testPredict, test_ids=None, seq_length=None, num_sequences=5):
    # Inverse transform to original scale
    testY_inverse = scaler.inverse_transform(testY.reshape(-1, 2)).reshape(testY.shape)
    testPredict_inverse = scaler.inverse_transform(testPredict.reshape(-1, 2)).reshape(testPredict.shape)

    for i in range(min(num_sequences, len(testY))):
        # Find the last non-padded timestep (where (lat, lon) != (0, 0))
        true_sequence = testY[i]  # Scaled values (before inverse transform)
        actual_length = np.max(np.where(np.any(true_sequence != [0.0, 0.0], axis=1))[0] + 1)

        plt.figure(figsize=(12, 6))
        time_steps = np.arange(actual_length)  # Only plot up to actual_length

        # Latitude plot
        plt.subplot(2, 1, 1)
        plt.plot(time_steps, testY_inverse[i, :actual_length, 0], 'b-', label='True Latitude', linewidth=2)
        plt.plot(time_steps, testPredict_inverse[i, :actual_length, 0], 'r--', label='Predicted Latitude', linewidth=2)
        plt.ylabel('Latitude (Degrees)')
        plt.title(f'Sequence {i+1}' + (f' (Trajectory ID: {test_ids[i]})' if test_ids else ''))
        plt.legend()
        plt.grid(True)

        # Longitude plot
        plt.subplot(2, 1, 2)
        plt.plot(time_steps, testY_inverse[i, :actual_length, 1], 'g-', label='True Longitude', linewidth=2)
        plt.plot(time_steps, testPredict_inverse[i, :actual_length, 1], 'm--', label='Predicted Longitude', linewidth=2)
        plt.xlabel('Time Step')
        plt.ylabel('Longitude (Degrees)')
        plt.legend()
        plt.grid(True)
        plt.savefig(f"images/sequence_{i}.png")
        plt.tight_layout()
        plt.show()

# %%
# main

def main(model=1, lstm_layers=1, lstm_cells=64, epochs=50, batch_size=64, validation_split=0.1):
    trainX, trainY, _, _, train_ids, _= preprocessing('datasets/outputs/cleaned_gpx.csv',seq_length=10)
    _, _, testX, testY, _, test_ids = preprocessing('datasets/test/cleaned_csv_test.csv',seq_length=10, ratio_train=0)
    if model == 1:
        model, history = simple_lstm_model(trainX, trainY, lstm_layers, lstm_cells, epochs, batch_size, validation_split)
    plotting_courbe_apprentissage(history)
    testPredict = prediction(model, testX, testY)
    trainScore, testScore = calculate_rmse(model, history, trainX, trainY, testY, testPredict)
    plotting(testY,testPredict, max_points=100)

    plot_sequences(testY, testPredict, test_ids=test_ids)
