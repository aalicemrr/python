import soma
import subtrair
import multiplicar
import divisao
import potencia
import raizquadrada

def calculadora():

    a = float(input("Digite o número A: "))
    b = float(input("Digite o número B: "))

    print("\nResultado:")
    print("Soma:", soma.somar(a, b))
    print("Subtração:", subtrair.subtrair(a, b))
    print("Multiplicação:", multiplicar.multiplicar(a, b))
    print("Divisão:", divisao.dividir(a, b))
    print("Potência:", potencia.potencia(a, b))
    print("Raiz Quadrada de A:", raizquadrada.raiz_quadrada(a))