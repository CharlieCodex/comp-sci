import numpy as np


def minibatch_sequencer(raw_data, batch_size, sequence_size, nb_epochs):
    data = np.array(raw_data)
    data_len = data.shape[0]
    nb_batches = (data_len - 1) // (batch_size * sequence_size)
    if nb_batches < 0:
        assert Exception("Not enough data, even for a single batch."
                         "Try using a smaller batch_size.")
    rounded_data_len = nb_batches * batch_size * sequence_size
    xdata = np.reshape(data[0:rounded_data_len],
                       [batch_size, nb_batches * sequence_size])
    ydata = np.reshape(data[1:rounded_data_len + 1],
                       [batch_size, nb_batches * sequence_size])

    for epoch in range(nb_epochs):
        for batch in range(nb_batches):
            x = xdata[:, batch * sequence_size:(batch + 1) * sequence_size]
            y = ydata[:, batch * sequence_size:(batch + 1) * sequence_size]
            # to continue the text from epoch to epoch do not reset rnn state!
            x = np.roll(x, -epoch, axis=0)
            y = np.roll(y, -epoch, axis=0)
            yield x, y, epoch


if __name__ == "__main__":
    import json
    data = []

    with open("example_data.txt") as file:
        data = json.load(file)

    for batch in minibatch_sequencer(data, 200, 20, 1):
        print(batch)
