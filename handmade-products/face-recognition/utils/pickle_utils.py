import pickle


def save_pickle(file_path, data):
    with open(file_path, "wb") as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(file_path):
    with open(file_path, "rb") as handle:
        data = pickle.load(handle)

    return data
