import torch.nn as nn
import torch

class EncoderRNN(nn.Module):
    r"""
    Converts low level features into higher level features

    Args:
        vocab_size (int): size of input
        hidden_size (int): the number of features in the hidden state `h`
        n_layers (int, optional): number of recurrent layers (default: 1)
        bidirectional (bool, optional): if True, becomes a bidirectional encoder (defulat: False)
        rnn_cell (str, optional): type of RNN cell (default: gru)
        dropout_p (float, optional): dropout probability for the output sequence (default: 0)

    Inputs: inputs
        - **inputs**: list of sequences, whose length is the batch size and within which each sequence is a list of token IDs.

    Returns: output, hidden
        - **output** (batch, seq_len, hidden_size): tensor containing the encoded features of the input sequence
        - **hidden** (num_layers * num_directions, batch, hidden_size): tensor containing the features in the hidden state `h`

    Examples::

        >>> listener = Listener(feat_size, hidden_size, dropout_p=0.5, n_layers=5)
        >>> output = listener(inputs)
    """
    def __init__(self, vocab_size, hidden_size, dropout_p=0.5, layer_size=5, bidirectional=True, rnn_cell='gru'):
        super(EncoderRNN, self).__init__()
        self.rnn_cell = nn.LSTM if rnn_cell.lower() == 'lstm' else nn.GRU if rnn_cell.lower() == 'gru' else nn.RNN
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.input_dropout = nn.Dropout(dropout_p)
        self.rnn = self.rnn_cell(
            input_size=vocab_size,
            hidden_size=hidden_size,
            num_layers=layer_size,
            bias=True,
            batch_first=True,
            bidirectional=bidirectional,
            dropout=dropout_p
        )


    def forward(self, inputs):
        """ Applies a multi-layer RNN to an input sequence """
        embedded = self.embedding(inputs)
        embedded = self.input_dropout(embedded)
        if self.training:
            self.rnn.flatten_parameters()
        outputs, hiddens = self.rnn(embedded)

        return outputs, hiddens