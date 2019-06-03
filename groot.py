
class no:
	def __init__(self,valor=None):
		self.valor=valor
		self.filho_esq=None
		self.filho_dir=None
		self.pai=None # ponteiro para o nó pai
		self.altura=1 # altura do nó para o topo (raiz)

class ArvoreAVL:
	def __init__(self):
		self.raiz=None

	def __repr__(self):
		if self.raiz==None: return ''
		content='\n' # para printar a arvore
		no_atual=[self.raiz] # recebe os nós do nivel atual
		altura_atual=self.raiz.altura # altura dos nós no nivel atual
		espaco=' '*(2**(altura_atual-1)) # para separar os espaços na hora de printar a árvore
		while True:
			altura_atual+=-1 # diminui a aultra
			if len(no_atual)==0: break ## para o loop quando chegar a raiz
			linha_atual=' '
			proxima_linha=''
			proximo_no=[]

			if all(n is None for n in no_atual):
				break

			for n in no_atual:

				if n==None:
					linha_atual+='   '+espaco
					proxima_linha+='   '+espaco
					proximo_no.extend([None,None])
					continue

				if n.valor!=None:       
					buf=' '*int((5-len(str(n.valor)))/2)
					linha_atual+='%s%s%s'%(buf,str(n.valor),buf)+espaco
				else:
					linha_atual+=' '*5+espaco

				if n.filho_esq!=None:  
					proximo_no.append(n.filho_esq)
					proxima_linha+=' /'+espaco
				else:
					proxima_linha+='  '+espaco
					proximo_no.append(None)

				if n.filho_dir!=None: 
					proximo_no.append(n.filho_dir)
					proxima_linha+='\ '+espaco
				else:
					proxima_linha+='  '+espaco
					proximo_no.append(None)

			content+=(altura_atual*'   '+linha_atual+'\n'+altura_atual*'   '+proxima_linha+'\n')
			no_atual=proximo_no
			espaco=' '*int(len(espaco)/2) # diminui os espacos na hora do print para metade
		return content

	def insert(self,valor):
		if self.raiz==None:
			self.raiz=no(valor)
		else:
			self._insert(valor,self.raiz)

	def _insert(self,valor,no_atual):
		if valor<no_atual.valor:
			if no_atual.filho_esq==None:
				no_atual.filho_esq=no(valor)
				no_atual.filho_esq.pai=no_atual # set pai
				self.insere_balanceado(no_atual.filho_esq)
			else:
				self._insert(valor,no_atual.filho_esq)
		elif valor>no_atual.valor:
			if no_atual.filho_dir==None:
				no_atual.filho_dir=no(valor)
				no_atual.filho_dir.pai=no_atual # set pai
				self.insere_balanceado(no_atual.filho_dir)
			else:
				self._insert(valor,no_atual.filho_dir)
		else:
			print("Esse valor já foi inserido!")

	def print_tree(self):
		if self.raiz!=None:
			self._print_tree(self.raiz)

	def _print_tree(self,no_atual):
		if no_atual!=None:
			self._print_tree(no_atual.filho_esq)
			print ('%s, h=%d'%(str(no_atual.valor),no_atual.altura))
			self._print_tree(no_atual.filho_dir)

	def altura(self):
		if self.raiz!=None:
			return self._altura(self.raiz,0)
		else:
			return 0

	def _altura(self,no_atual,cur_height):
		if no_atual==None: return cur_height
		altura_esq=self._altura(no_atual.filho_esq,cur_height+1)
		altura_dir=self._altura(no_atual.filho_dir,cur_height+1)
		return max(altura_esq,altura_dir)

	def find(self,valor):
		if self.raiz!=None:
			return self._find(valor,self.raiz)
		else:
			return None

	def _find(self,valor,no_atual):
		if valor==no_atual.valor:
			return no_atual
		elif valor<no_atual.valor and no_atual.filho_esq!=None:
			return self._find(valor,no_atual.filho_esq)
		elif valor>no_atual.valor and no_atual.filho_dir!=None:
			return self._find(valor,no_atual.filho_dir)

	def delete_value(self,valor):
		return self.deletar_no(self.find(valor))

	def deletar_no(self,no):

		if no==None or self.find(no.valor)==None:
			print("Nó não encontrado\n!")
			return None 
		def no_menor(n): 		# retorna o no com menor valor
			atual=n
			while atual.filho_esq!=None:
				atual=atual.filho_esq
			return atual

		def filho(n): # retorna o número de nos filhos
			filhos=0
			if n.filho_esq!=None: filhos+=1
			if n.filho_dir!=None: filhos+=1
			return filhos
		no_pai=no.pai
		no_filho=filho(no)
		# CASO 1 NÓ NÃO TEM FILHO
		if no_filho==0:
			if no_pai!=None:
				if no_pai.filho_esq==no:
					no_pai.filho_esq=None
				else:
					no_pai.filho_dir=None
			else:
				self.raiz=None

		# CASO 2 NÓ TEM UM FILHO
		if no_filho==1:

			if no.filho_esq!=None:
				child=no.filho_esq
			else:
				child=no.filho_dir

			if no_pai!=None:
				if no_pai.filho_esq==no:
					no_pai.filho_esq=child
				else:
					no_pai.filho_dir=child
			else:
				self.raiz=child
			child.pai=no_pai

		# CASO 3 NO TEM 2 FILHOS
		if no_filho==2:
			successor=no_menor(no.filho_dir)
			no.valor=successor.valor
			self.deletar_no(successor)
			return

		if no_pai!=None:
			no_pai.altura=1+max(self.get_altura(no_pai.filho_esq),self.get_altura(no_pai.filho_dir))
			self.deleta_balanceado(no_pai)

	def search(self,valor):
		if self.raiz!=None:
			return self._search(valor,self.raiz)
		else:
			return False

	def _search(self,valor,no_atual):
		if valor==no_atual.valor:
			return True
		elif valor<no_atual.valor and no_atual.filho_esq!=None:
			return self._search(valor,no_atual.filho_esq)
		elif valor>no_atual.valor and no_atual.filho_dir!=None:
			return self._search(valor,no_atual.filho_dir)
		return False 



	def insere_balanceado(self,no_atual,path=[]):
		if no_atual.pai==None: return
		path=[no_atual]+path

		altura_esq =self.get_altura(no_atual.pai.filho_esq)
		altura_dir=self.get_altura(no_atual.pai.filho_dir)

		if abs(altura_esq-altura_dir)>1:
			path=[no_atual.pai]+path
			self.balancear(path[0],path[1],path[2])
			return

		new_height=1+no_atual.altura 
		if new_height>no_atual.pai.altura:
			no_atual.pai.altura=new_height

		self.insere_balanceado(no_atual.pai,path)

	def deleta_balanceado(self,no_atual):
		if no_atual==None: return

		altura_esq =self.get_altura(no_atual.filho_esq)
		altura_dir=self.get_altura(no_atual.filho_dir)

		if abs(altura_esq-altura_dir)>1:
			y=self.filho_maior(no_atual)
			x=self.filho_maior(y)
			self.balancear(no_atual,y,x)

		self.deleta_balanceado(no_atual.pai)

	def balancear(self,z,y,x):
		if y==z.filho_esq and x==y.filho_esq:
			print("ROTACAO PARA DIREITA\n")
			print(self)
			self.rotacao_direita(z)
		elif y==z.filho_esq and x==y.filho_dir:
			print("ROTACAO DUPLA PARA DIREITA\n")
			print(self)
			self.rotacao_esquerda(y)
			self.rotacao_direita(z)
		elif y==z.filho_dir and x==y.filho_dir:
			print("ROTACAO PARA ESQUERDA\n")
			print(self)
			self.rotacao_esquerda(z)
		elif y==z.filho_dir and x==y.filho_esq:
			print("ROTACAO DUPLA PARA ESQUERDA\n")
			print(self)
			self.rotacao_direita(y)
			self.rotacao_esquerda(z)
		else:
			print("DEU RUIM!\n")

	def rotacao_direita(self,z):
		sub_root=z.pai 
		y=z.filho_esq
		t3=y.filho_dir
		y.filho_dir=z
		z.pai=y
		z.filho_esq=t3
		if t3!=None: t3.pai=z
		y.pai=sub_root
		if y.pai==None:
				self.raiz=y
		else:
			if y.pai.filho_esq==z:
				y.pai.filho_esq=y
			else:
				y.pai.filho_dir=y		
		z.altura=1+max(self.get_altura(z.filho_esq),
			self.get_altura(z.filho_dir))
		y.altura=1+max(self.get_altura(y.filho_esq),
			self.get_altura(y.filho_dir))

	def rotacao_esquerda(self,z):
		sub_root=z.pai 
		y=z.filho_dir
		t2=y.filho_esq
		y.filho_esq=z
		z.pai=y
		z.filho_dir=t2
		if t2!=None: t2.pai=z
		y.pai=sub_root
		if y.pai==None: 
			self.raiz=y
		else:
			if y.pai.filho_esq==z:
				y.pai.filho_esq=y
			else:
				y.pai.filho_dir=y
		z.altura=1+max(self.get_altura(z.filho_esq),
			self.get_altura(z.filho_dir))
		y.altura=1+max(self.get_altura(y.filho_esq),
			self.get_altura(y.filho_dir))

	def get_altura(self,no_atual):
		if no_atual==None: return 0
		return no_atual.altura

	def filho_maior(self,no_atual):
		left=self.get_altura(no_atual.filho_esq)
		right=self.get_altura(no_atual.filho_dir)
		return no_atual.filho_esq if left>=right else no_atual.filho_dir


#######MAIN########

nova_arvore = ArvoreAVL()
x=0
while(True):
    x = int(input("Deseja adicionar algum numero a arvore?\n1)Sim\n2)Não\n"))
    if x!=1:
        break
    valor = int(input("Qual valor deseja adicionar a arvore?\n"))
    nova_arvore.insert(valor)
    print(nova_arvore)

