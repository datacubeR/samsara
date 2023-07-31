from utils import train_test_sequences

SEQ_LEN = 10
RESAMPLE = "2W"
INTERPOLATION = "time"
EVENTS = ["ESTABLE", "INCENDIO", "SEQUIA", "TALA", "VARIOS"]

train_data = {}
test_data = {}
for event in EVENTS:
    train_data[event], test_data[event] = train_test_sequences(
        event, RESAMPLE, INTERPOLATION, SEQ_LEN
    )
