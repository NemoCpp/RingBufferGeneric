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

def buffercirculaire(suiv, fenetre, decalage):
	try : 
		buffer = [None]*fenetre*4
		ecriture = 0
		lecture = 0
		while True : 
			input = yield
			print("Un truc :", input)
			#Calcul écart entre les deux pointeurs, si buffer > fenetre 
			taille =  ecriture - lecture if lecture < ecriture else fenetre - lecture + ecriture 
			#tant qu'on n'a pas rempli le buffer 
			for j in range (0, len(input)):
				buffer[ecriture] = input[j]
				ecriture = (ecriture + 1 ) % len(buffer)	

			while(taille > fenetre):
				#Si la totalité du tableau n'est pas à cheval sur la fin et le début du tableau 
				if (lecture < (lecture + fenetre)%len(buffer)):
					suiv.send(buffer[lecture : lecture + fenetre])
				else: 
					suiv.send(buffer[lecture : len(buf)] + buffer[0 : (fenetre - len(buffer) + lecture)])
				lecture = (lecture + decalage) % len(buffer)
				taille =  ecriture - lecture if lecture < ecriture else fenetre - lecture + ecriture 			
	except GeneratorExit: 
		suiv.close()


def sub():
    try:
        while True:
            input=yield
            print("Sink :", input)
    except GeneratorExit:
        print("ici")


sink = sub()
next(sink)
buf = buffercirculaire(sink, 4, 2 )
next(buf)
source = test(buf)
next(source)
next(source)

   