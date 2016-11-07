from ringBuffer import *

#Function which send tabs into the pipeline
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
inp = source(buf)
next(inp)
