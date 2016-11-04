def  test(suiv):
    x = [1,2,3,4,5,6,7,8,9,10]
    y = ['a','b','c']
    while (True):
        (yield None)
        suiv.send(x)
        suiv.send(y)
    suiv.close()

def pipe(suiv):
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

"""
# TODO Sphinx documentation
"""
def ring_buffer(next, window, offset):
	try :
		buffer = [None]*window*4
		write_index = 0
		read_index = 0
		while True :
			input = yield
			# data size between indexes
			data_size =  write_index - read_index if read_index < write_index else window - read_index + write_index
			# add new data to buffer
			for j in range (0, len(input)):
				buffer[write_index] = input[j]
				write_index = (write_index + 1 ) % len(buffer)

			while(data_size > window):
				# send a window (testing the case we must concatenate the beginning and end of the buffer)
				if (read_index < (read_index + window)%len(buffer)):
					next.send(buffer[read_index : read_index + window])
				else:
					next.send(buffer[read_index : len(buf)] + buffer[0 : (window - len(buffer) + read_index)])
				read_index = (read_index + offset) % len(buffer)
				data_size =  write_index - read_index if read_index < write_index else window - read_index + write_index
	except GeneratorExit:
		next.close()


def sub():
    try:
        while True:
            input=yield
            print("Sink :", input)
    except GeneratorExit:
        print("ici")


sink = sub()
next(sink)
buf = ring_buffer(sink, 4, 2 )
next(buf)
source = test(buf)
next(source)
next(source)
