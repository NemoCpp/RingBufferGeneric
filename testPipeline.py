import numpy as np  
from ringBuffer import *
import sidekit

#Function which send tabs into the pipeline
@coroutine
def audio_reader(next_routine, audio_file):
    input_filename = audio_file
    sampling_rate = 16000
    if input_filename.endswith('.sph') or input_filename.endswith('.pcm')\
            or input_filename.endswith('.wav') or input_filename.endswith('.raw'):
        x, rate = sidekit.frontend.io.read_audio(input_filename, sampling_rate)

    # add random noise to avoid any issue due to zeros
    np.random.seed(0)
    if x.ndim == 1:
        x += 0.0001 * np.random.randn(x.shape[0])
    elif x.ndim == 2:
        x[:, 0] += 0.0001 * np.random.randn(x.shape[0])
        if x.shape[1] == 2:
            x[:, 1] += 0.0001 * np.random.randn(x.shape[0])

    (yield None)
    idx = 0
    next_routine.send(x)
    next_routine.close()

@coroutine
def  source(suiv):
    x = [1,2,3,4,5,6,7,8,9,10]
    y = ['a','b','c']
    while (True):
        (yield None)
        suiv.send(x)
        suiv.send(y)
    suiv.close()

#Send every other value
@coroutine
def everyOtherValue(suiv):
    try :
        while True:
            input=yield
            print("Pipe :", input)
            lettre = 1
            while (lettre < len(input)):
                suiv.send(input[lettre])
                lettre = lettre+2;
    except GeneratorExit:
        suiv.close()

#Buffer
@coroutine
def buffer(suiv):
    try :
        buf1 = [None] * 2
        while(True):
            i = 0
            while(i<2):
                input = yield
                print("Buffer :", input)
                buf1[i] = input
                i+= 1
            suiv.send(buf1)
    except GeneratorExit:
        suiv.close()

#Output of the pipeline, print the result of the treatment
@coroutine
def sink():
    try:
        while True:
            input=yield
            print("Sink :", input)
    except GeneratorExit:
        print("ici")


output = sink()
buf = ring_buffer(output, 4, 2 )
inp = audio_reader(buf, "test.raw")
try : 
    next(inp)
except StopIteration :
    print("That's all folks")
