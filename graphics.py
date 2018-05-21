import numpy as np
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
import os, sys
import imageio



replacements = {
    'sin' : 'np.sin',
    'cos' : 'np.cos',
	'tan' : 'np.tan',
	'arccos' : 'np.arccos',
	'arcsin' : 'np.arcsin',
	'sinh' : 'np.cosh',
	'cosh' : 'np.cosh',
	'tanh' : 'np.tanh',
	'arccosh' : 'np.arccosh',
	'arcsinh' : 'np.arcsinh',
    'ln': 'np.exp',
    '^': '**',
}

# преобразование этих слов может поломать программу (так как eval)
forbidden_words = [
    'import',
    'shutil',
    'sys',
    'subprocess',
]

def string2func(string):
    ''' преобразует строку в код функции и возвращает ее '''
    for word in forbidden_words:
        if word in string:
            raise ValueError(
                '"{}" недопустимо использовать при вводе'.format(word)
            )

    for old, new in replacements.items():
        string = string.replace(old, new)

    def func(x):
        return eval(string)
    return func

def d3a2string2func(string):
    ''' преобразует строку в код функции и возвращает ее '''
    for word in forbidden_words:
        if word in string:
            raise ValueError(
                '"{}" недопустимо использовать при вводе'.format(word)
            )

    for old, new in replacements.items():
        string = string.replace(old, new)

    def func(x,y):
        return eval(string)

   # func[np.diff(func) >= 5] = np.nan

    return func


def simple_graph (string): 
	temp= string.split(', ')
	strfunc = temp[0]
	a = int(temp[1])
	b = int(temp[2])
	func = string2func(strfunc)
	x = np.linspace(a,b, 250)
	plt.plot(x, func(x))
	plt.xlim(a, b)
	plt.xlabel(r'$x$') #Метка по оси x в формате TeX
	plt.ylabel(r'$f(x)$') #Метка по оси y в формате TeX
	''' text = ""+"$"+message+"$"	'''
	'''  plt.title(text) Заголовок в формате TeX '''
	plt.grid(True) #Сетка
	plt.savefig('foo.png') 
	photo = open('foo.png', 'rb')
	return photo

def make_views(ax,angles,elevation=None, width=4, height = 3,
                prefix='tmprot_',**kwargs):
    files = []
    ax.figure.set_size_inches(width,height)
     
    for i,angle in enumerate(angles):
     
        ax.view_init(elev = elevation, azim=angle)
        fname = '%s%03d.jpeg'%(prefix,i)
        ax.figure.savefig(fname)
        files.append(fname)
     
    return files
 
def make_gif(files,output, repeat=True, delay=20):

    images = []
    for filename in files:
        images.append(imageio.imread(filename))
    imageio.mimsave('movie.gif', images)

    loop = -1 if repeat else 0
    os.system('convert -delay %d -loop %d %s %s'
              %(delay,loop," ".join(files),output))

def make_strip(files,output,**kwargs):
   
    os.system('montage -tile 1x -geometry +0+0 %s %s'%(" ".join(files),output))

 
def rotanimate(ax, angles, output, **kwargs):     
    output_ext = os.path.splitext(output)[1]
 
    files = make_views(ax,angles, **kwargs)
     
    D = { '.gif': make_gif ,
          '.jpeg': make_strip,
          '.png':make_strip}
           
    D[output_ext](files,output,**kwargs)
     
    for f in files:
        os.remove(f)
    
def movie_graph(message):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	#X, Y, Z = axes3d.get_test_data(0.05)
	
	x = y = np.arange(-10.0, 10.0, 0.1)

	#x = np.arange(-4, 9, 1)
	#y = np.arange(-4, 9,1)
	X, Y = np.meshgrid(x, y)
	fun = d3a2string2func (message)
	#pos = np.where(np.abs(np.diff(fun)) >= 0.5)[0]
	zs = np.array([fun(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
	Z = zs.reshape(X.shape)
	v=fun(3,5)
	s = ax.plot_surface(X, Y, Z, cmap=cm.jet)
	plt.axis('off') 
	angles = np.linspace(0,360,21)[:-1] 

	rotanimate(ax, angles,'movie.gif', delay=20) 
