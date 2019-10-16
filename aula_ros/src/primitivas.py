#ACENTOS OCASIONAM  ERRO NO PROGRAMA!!
#primitivas referentes ao led, buzzer, botoes, lcd, teclado, potenciometro
import sys, traceback
import Adafruit_GPIO.SPI as SPI
import Adafruit_ADS1x15  as ADS
from smbus import SMBus #importa biblioteca que contem I2C
import time #importando biblioteca de tempo
bus = SMBus(1) #configura o canal do i2c para o canal 1 e renomeia para 'bus'
lcd05 = 0x63 #endereco do lcd
adc = ADS.ADS1115(address=0x4a, busnum=1)
PCF = [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27] #lista com todos os PCFs

bus = SMBus(1) #configura o canal do i2c para o canal 1

#funcao para ligar buzzer
def buzzer(estado):
        if (estado == True):
                bus.write_byte(PCF[7],255)
        else:
                bus.write_byte(PCF[7],0)

#Funcao para acionar botao
  #Entradas: i [0 - 7] -> indica o botao habilitado
def button(i):
        #ler = bus.read_byte(PCF[1]) #leitura do respectivo pcf do botao
        mask = 2**i
        if(i >= 0 and i <= 7):
                if (mask & bus.read_byte(PCF[1])) == 0:
                        return False
                else:
                        return True
        else:
                print "Algum argumento do botao esta invalido!!!"
                sys.exit(0)
#Funcao para acender, apagar, ou comutar leds
  #Entradas: write  = 0 e led  [0 - 7] -> acende led
  #Entradas: write  = 1 e led  [0 - 7] -> apaga led
  #Entradas: write  = 2 e led  [0 - 7] -> comuta led
  #Entradas: write [0-2] e led > 8 -> acao afeta todos leds

def led(write, led):
        if(led >= 0 and led <= 8 and write >= 0 and write <= 2):
                if(led >= 0 and led <= 7):
                        mask = 2**led
                if(led == 8):
                        mask = 255
                #Acende led
                if (write == 0):
                        dado = bus.read_byte(PCF[0]) & ~(mask)
			bus.write_byte(PCF[0],dado)
                #Apaga led
                if(write == 1):
                        dado = bus.read_byte(PCF[0]) | mask
                        bus.write_byte(PCF[0],dado)
                #Comuta led
                if(write == 2):
                        dado = bus.read_byte(PCF[0]) ^ mask
                        bus.write_byte(PCF[0],dado)

        else:
                print "Algum argumento do led esta invalido!!!"
                sys.exit(0)

def leds(ensemble_leds):
	bus.write_byte(PCF[0], ensemble_leds)

#Funcao para iniciar o lcd
def lcd_init():
        #0 - sem operacao
        #19 - liga backlight
        #12 - limpa tela e coloca cursor no inicio
        #6 - pisca cursor
        buf=[0,19,12,6]
        bus.write_i2c_block_data(lcd05,0,buf)

def lcd_comando(comando):
        if(type(comando) == int):
                bus.write_byte_data(lcd05,0,comando) #manda um comando para o lcd
        else:
                bus.write_i2c_block_data(lcd05,0,comando)


#Funcao para escrever uma string no lcd
def lcd_escrever(palavra):
        if(type(palavra) == str):
                lista = palavra.split('\n')
                for i in range(len(lista)):
                        for j in range(len(lista[i])):
                                palavra1 = lista[i]
                                a = ord(palavra1[j]) #transforma de char para ascII
                                bus.write_byte_data(lcd05,0,a) #escreve no lcd
                        if i<len(lista)-1:
                                bus.write_byte_data(lcd05,0,13)
        else:
                palavra1 = str(palavra) #transforma para string
                tamanho = len(palavra1) #le tamanho da string
                for i in range(tamanho):
                        a = ord(palavra1[i]) #transforma de char para ascII
                        bus.write_byte_data(lcd05,0,a) #escreve no lcd

#funcao para ler teclado
def teclado():
        lowb = bus.read_byte_data(lcd05,1) #le o lowbyte 
        highb = bus.read_byte_data(lcd05,2) #le o high byte
        tec = highb<<8+ lowb
        #print(highb,lowb,tec)
        #Mapeamento Teclado
        digito = 'x'
        if (lowb == 1):
                digito = '1'
		lcd_escrever(digito)
	if (lowb == 2):
                digito = '2'
                lcd_escrever(digito)
	if (lowb ==4):
                digito = '3'
                lcd_escrever(digito)
	if (lowb == 8):
                digito = '4'
                lcd_escrever(digito)
        if (lowb == 16):
                digito = '5'
                lcd_escrever(digito)
	if (lowb == 32):
                digito = '6'
                lcd_escrever(digito)
	if (lowb == 64):
                digito = '7'
                lcd_escrever(digito)
	if (lowb == 128):
                digito = '8'
                lcd_escrever(digito)
	if (tec == 256):
                digito = '9'
                lcd_escrever(digito)
	if (tec == 512):
                digito = ' '
		lcd_comando(32)
	if (tec == 1024):
                digito = 0
                lcd_escrever(digito)
	if (tec == 2048):
                digito = '*'
		lcd_comando(8)
	time.sleep(0.3)
	return digito

def configuraSPI(porta, select):
        if((porta == 0) or (select == 0) or (select == 1)):
                #definicao da porta e select do SPI
                SPI_PORT = porta
                SPI_DEVICE = select
        else:
                #sai do programa se for informado um valor invalido
                sys.exit()
        #Configuracao do canal SPI
        return(ADC.MCP3008(spi = SPI.SpiDev(SPI_PORT, SPI_DEVICE)))

def lepot(canal):
        if canal == 0:
                #leitura do canal 0 do AD
                value = 100-(adc.read_adc(0))*100/32767
        elif canal == 1:
                #leitura do canal 1 do AD
                value = 100-(adc.read_adc(1))*100/32767

        else:
		print("Canal escolhido invalido")
                #sai do programa se for informado um valor invalido
                sys.exit()
        #retorna o valor convertido da leitura do AD pra porcentagem, de 0 a 100
        return(value)

def sete_segm_on(digit, number):
	#habilita os 4 digitos do 7 segmentos
	buf = 240 | bus.read_byte(PCF[6])
	bus.write_byte(PCF[6],buf)
	
	if digit == 1:
		if number == 0:
			bus.write_byte(PCF[6],244)
			buf = 199 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 1:
			bus.write_byte(PCF[6],254)
			buf = 247 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 2:
			bus.write_byte(PCF[6],248)
			buf = 207 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 3:
			bus.write_byte(PCF[6],248)
			buf = 231 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 4:
			bus.write_byte(PCF[6],242)
			buf = 247 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 5:
			bus.write_byte(PCF[6],241)
			buf = 231 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 6:
			bus.write_byte(PCF[6],241)
			buf = 199 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 7:
			bus.write_byte(PCF[6],252)
			buf = 247 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 8:
			bus.write_byte(PCF[6],240)
			buf = 199 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 9:
			bus.write_byte(PCF[6],240)
			buf = 231 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 10:
			bus.write_byte(PCF[6],240)
			buf = 215 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 11:
			bus.write_byte(PCF[6],243)
			buf = 199 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 12:
			bus.write_byte(PCF[6],245)
			buf = 207 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 13:
			bus.write_byte(PCF[6],250)
			buf = 199 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 14:
			bus.write_byte(PCF[6],241)
			buf = 207 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 15:
			bus.write_byte(PCF[6],241)
			buf = 223 & (60 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
		elif number == 16:
			buf = 251 & bus.read_byte(PCF[4])
			bus.write_byte(PCF[4],buf)
		else:
			print("Not a valid number!\n");
			sys.exit(0)

	elif digit == 2:
		if number == 0:
			buf = 31 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 252 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 191 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 1:
			buf = 223 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 255 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 191 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 2:
			buf = 159 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 252 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 127 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 3:
			buf = 159 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 254 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 63 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 4:
			buf = 95 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 255 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 63 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 5:
			buf = 63 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 254 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 63 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 6:
			buf = 63 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 252 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 63 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 7:
			buf = 159 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 255 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 191 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 8:
			buf = 31 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 252 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 63 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 9:
			buf = 31 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 254 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 63 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)			
		elif number == 10:
			buf = 31 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 253 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 63 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 11:
			buf = 127 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 252 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 63 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 12:
			buf = 63 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 252 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 255 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 13:
			buf = 223 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 252 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 63 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 14:
			buf = 63 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 252 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 127 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 15:
			buf = 63 & (224 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 253 & (3 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 127 & (224 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 16:
			buf = 223 & bus.read_byte(PCF[3])
			bus.write_byte(PCF[3],buf)
		else:
			print("Not a valid number!\n");
			sys.exit(0)
	elif digit == 3:
		if number == 0:
			buf = 233 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 227 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 1:
			buf = 253 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 251 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 2:
			buf = 241 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 231 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 3:
			buf = 241 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 243 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 4:
			buf = 229 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 251 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 5:
			buf = 227 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 243 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 6:
			buf = 227 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 227 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 7:
			buf = 249 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 251 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 8:
			buf = 225 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 227 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 9:
			buf = 225 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 243 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 10:
			buf = 225 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 235 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 11:
			buf = 231 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 227 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 12:
			buf = 235 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 231 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 13:
			buf = 245 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 227 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 14:
			buf = 227 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 231 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 15:
			buf = 227 & (30 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 239 & (30 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
		elif number == 16:
			buf = 253 & bus.read_byte(PCF[3])
			bus.write_byte(PCF[3],buf)
		else:
			print("Not a valid number!\n");
			sys.exit(0)

	elif digit == 4:
		if number == 0:
			buf = 254 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 63 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 254 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],95)
		elif number == 1:
			buf = 255 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 191 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 255 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],223)
		elif number == 2:
			buf = 255 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 63 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 254 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],63)
		elif number == 3:
			buf = 255 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 63 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 255 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],31)
		elif number == 4:
			buf = 254 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 191 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 255 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],159)
		elif number == 5:
			buf = 254 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 127 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 255 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],31)
		elif number == 6:
			buf = 254 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 127 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 254 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],31)
		elif number == 7:
			buf = 255 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 63 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 255 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],223)
		elif number == 8:
			buf = 254 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 63 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 254 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],31)
		elif number == 9:
			buf = 254 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 63 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 255 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],31)
		elif number == 10:
			buf = 254 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 63 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 254 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],159)
		elif number == 11:
			buf = 254 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 255 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 254 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],31)
		elif number == 12:
			buf = 254 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 127 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 254 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],127)
		elif number == 13:
			buf = 255 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 191 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 254 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],31)
		elif number == 14:
			buf = 254 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 127 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 254 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],63)
		elif number == 15:
			buf = 254 & (1 | bus.read_byte(PCF[5]))
			bus.write_byte(PCF[5],buf)
			buf = 127 & (192 | bus.read_byte(PCF[4]))
			bus.write_byte(PCF[4],buf)
			buf = 254 & (1 | bus.read_byte(PCF[3]))
			bus.write_byte(PCF[3],buf)
			bus.write_byte(PCF[2],176)
		elif number == 16:
			buf = 239 & bus.read_byte(PCF[2])
			bus.write_byte(PCF[2],239)
		else:
			print("Not a valid number!\n");
			sys.exit(0)
	else:
		print("Not a valid digit!\n");
		sys.exit(0)

def sete_segm_off(digit):

	if digit == 0: #apaga todos os digitos
		bus.write_byte(PCF[2],255)
		bus.write_byte(PCF[3],255)
		bus.write_byte(PCF[4],255)
		bus.write_byte(PCF[5],255)
		bus.write_byte(PCF[6],15)

	elif digit == 1:
		buf = 15 | bus.read_byte(PCF[6])
		bus.write_byte(PCF[6],buf)
		buf = 60 | bus.read_byte(PCF[4])
		bus.write_byte(PCF[4],buf)
		buf = 127 & bus.read_byte(PCF[6])
		bus.write_byte(PCF[6],buf)

	elif digit == 2:
		buf = 224 | bus.read_byte(PCF[5])
		bus.write_byte(PCF[5],buf)
		buf = 3 | bus.read_byte(PCF[4])
		bus.write_byte(PCF[4],buf)
		buf = 224 | bus.read_byte(PCF[3])
		bus.write_byte(PCF[3],buf)
		buf = 191 & bus.read_byte(PCF[6])
		bus.write_byte(PCF[6],buf)

	elif digit == 3:
		buf = 30 | bus.read_byte(PCF[5])
		bus.write_byte(PCF[5],buf)
		buf = 30 | bus.read_byte(PCF[3])
		bus.write_byte(PCF[3],buf)
		buf = 223 & bus.read_byte(PCF[6])
		bus.write_byte(PCF[6],buf)

	elif digit == 4:
		buf = 1 | bus.read_byte(PCF[5])
		bus.write_byte(PCF[5],buf)
		buf = 192 | bus.read_byte(PCF[4])
		bus.write_byte(PCF[4],buf)
		buf = 1 | bus.read_byte(PCF[3])
		bus.write_byte(PCF[3],buf)
		bus.write_byte(PCF[2],255)
		buf = 239 & bus.read_byte(PCF[6])
		bus.write_byte(PCF[6],buf)
	else:
		print("Not a valid digit!\n");
		sys.exit(0)

def mapSemaforo(semaf, cor):

	if(cor == 'y' or cor == 'Y'):
		num = 2
	if(semaf%2 == 0):
		if(cor == 'r' or cor == 'R'):
			num = 1
		elif(cor == 'g' or cor == 'G'):
			num = 3
	else:
		if(cor == 'r' or cor == 'R'):
			num = 3
		elif(cor == 'g' or cor == 'G'):
			num = 1

        #LEDs vao de 1 a 30, calcula-se a posicao do LED a partir do
        #semaforo e cor escolhidos
        led = 31 - (semaf-1)*3 - num;

	#identificacao de qual pcf eh responsavel pelo led escolhido
        if(led<7): #pcf 011 responsavel por 6 primeiros leds
                pcf1=3
        elif(led<15): #pcf 100 responsavel pelos 8 leds seguintes
                pcf1=4
        elif(led<23): #pcf 101 responsavel pelos 8 leds seguintes
                pcf1=5
        else: #pcf 110 responsavel pelos 8 ultimos leds
                pcf1=6

	#calculo para identificar pino do pcf responsavel pelo led
        pin = led+2-8*(pcf1-3)
        #pino do pcf representado em hexadecimal (led=0, outros=1),
        #esta variavel sera usada como mascara para escrever na leitura
        #anterior do pcf, para que nao se altere leds de outros semaforos
        pinHex = 255 - 2**(pin-1)
        #leitura do pcf que sera modificado
	buf = bus.read_byte(PCF[pcf1])
        #modificamento da leitura feita pela mascara AND
        #(altera-se pino desejado para 0)
        buf = buf & pinHex
        #escrita no pcf do novo valor de buf
        bus.write_byte(PCF[pcf1], buf)
        #identificacao dos outros 2 leds do mesmo semaforo,
        #com o intuito de desliga-los
	if(num==2):
                led2=led+1
                led3=led-1
        if(num==1):
                led2=led-1
                led3=led-2
        if(num==3):
                led2=led+1
                led3=led+2
        #identificacao de qual pcf eh responsavel pelo led escolhido
        if(led2<7):
                pcf2=3
        elif(led2<15):
                pcf2=4
        elif(led2<23):
                pcf2=5
        else:
                pcf2=6

        #identificacao de qual pcf eh responsavel pelo led escolhido
        if(led3<7):
                pcf3=3
        elif(led3<15):
                pcf3=4
        elif(led3<23):
                pcf3=5
        else:
                pcf3=6

	#calculo para identificar pino do pcf responsavel pelo led
        pin2 = led2+2-8*(pcf2-3)
        #pino do pcf representado em hexadecimal (led=1, outros=0),
        #esta variavel sera usada como mascara para escrever na leitura
        #anterior do pcf, para que nao se altere leds de outros semaforos
        pinHex2 = 2**(pin2-1)
        #leitura do pcf que sera modificado
        buf = bus.read_byte(PCF[pcf2])
        #modificamento da leitura feita pela mascara OR
        #(altera-se pino desejado para 1)
        buf = buf | pinHex2
        #escrita no pcf do novo valor de buf
        bus.write_byte(PCF[pcf2], buf)

        #calculo para identificar pino do pcf responsavel pelo led
        pin3 = led3+2-8*(pcf3-3)
        #pino do pcf representado em hexadecimal (led=1, outros=0),
        #esta variavel sera usada como mascara para escrever na leitura
        #anterior do pcf, para que nao se altere leds de outros semaforos
        pinHex3 = 2**(pin3-1)
        #leitura do pcf que sera modificad
        buf = bus.read_byte(PCF[pcf3])
        #modificamento da leitura feita pela mascara OR
        #(altera-se pino desejado para 1)
        buf = buf | pinHex3
        #escrita no pcf do novo valor de buf
        bus.write_byte(PCF[pcf3], buf)


def iniciarSemaforo(modo):

	if modo == 0:
		buf = 255
	else:
		buf = 0

	for i in range(3,7):
		bus.write_byte(PCF[i],buf)
		time.sleep(0.01)

#Funcao ledSemaforo que recebe um valor 'led' de 1 a 30 que corresponde a um led especifico da placa de
#semaforos. O parametro 'comando' liga ou desliga o led selecionado.
#Se comando = 1, entao desligue o led. Se comando = 0, acenda o led.
#O acendimento ou desligamento de um led especifico nao afeta qualquer um dos demais leds
def ledSemaforo(led,comando):

	#selecao do indice que corresponde ao PCF
	if (led>=1 and led<=6):
		i = 3
	if (led>=7 and led<=14):
		i = 4
	if (led>=15 and led<=22):
		i = 5
	if (led>=23 and led<=30):
		i = 6
	
	#Selecao da mascara para garantir que a acao de ligar/desligar afete apenas o led especificado
	if (led==7 or led==15 or led==23):
		mask = 1
	if (led==8 or led==16 or led==24):
		mask = 2
	if (led==1 or led==9 or led==17 or led==25):
		mask = 4
	if (led==2 or led==10 or led==18 or led==26):
		mask = 8
	if (led==3 or led==11 or led==19 or led==27):
		mask = 16
	if (led==4 or led==12 or led==20 or led==28):
		mask = 32
	if (led==5 or led==13 or led==21 or led==29):
		mask = 64
	if (led==6 or led==14 or led==22 or led==30):
		mask = 128

	leitura = bus.read_byte(PCF[i])
	#time.sleep(0.1)

	#Atribuicao do buffer para ser enviado ao PFC[i]
	if(comando == 0): #Comparacao OR bit a bit
		buf = leitura | mask
	else: 
		buf = leitura & (~mask) #Comparacao AND bit a bit

	#Envio do buffer de dados ao respectivo PCF

	bus.write_byte(PCF[i],buf)
	#time.sleep(0.1)

# Test for RGBs onboard
def rgb():

        bus.write_byte(PCF[2], 79) #Y color RGB2 OFF
        bus.write_byte(PCF[3], 255) #X color RGB1 ON
        time.sleep(.5)
        bus.write_byte(PCF[3], 254) #X color RGB1 OFF
        bus.write_byte(PCF[2], 207) #Y color RGB1 ON
        time.sleep(.5)
        bus.write_byte(PCF[2], 79) #Y color RGB1 OFF
        bus.write_byte(PCF[2], 111) #X color RGB2 ON
        time.sleep(.5)
        bus.write_byte(PCF[2], 79) #X color RGB2 OFF
        bus.write_byte(PCF[2], 95) #Y color RGB2 ON
        time.sleep(.5)
        bus.write_byte(PCF[3], 254) #X color RGB1 OFF
        bus.write_byte(PCF[2], 79) #Y color RGB2 OFF
        time.sleep(.5)
