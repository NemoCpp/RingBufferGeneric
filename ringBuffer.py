#Coroutine of a Ringbuffer 

def coroutine(func):
    """
    Decorator that allows to forget about the first call of a coroutine .next()
    method or .send(None)
    This call is done inside the decorator
    :param func: the coroutine to decorate
    """
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next(cr)
        return cr
    return start 

@coroutine
def ring_buffer(next, window, covering):
    """
    Ring buffer inside a coroutine that allows to bufferize received data
    Hand send it to next method when window size is reached. A covering size
    can be set to include this amount of the previous data with the next send.
    :param next: next coroutine to send data
    :param window: data size to send
    :param covering: data size sent with the next window
    """
    try:
        buffer = [None]*window*4
        write_index = 0
        read_index = 0
        offset = window - covering
        while True :
            input = yield
            if input is None:
                continue
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

   