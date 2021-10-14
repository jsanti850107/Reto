from flask import Flask
from flask import render_template as render
from flask import request
from flask import redirect


app= Flask(__name__)

#usuarios=["Juan", "Mariana", "Wollman", "Camilo","Cesar"]
#creacion Diccionario de usuarios
usuarios={
    "juan":{"nombre": "Juan Santiago","usuario":"juan","td":"Cedula de Ciudadania", "clave":"1234", "foto":"img","rol":"SuperAdmin"},
    "mariana":{"nombre": "Mariana","usuario":"mariana","td":"Cedula de Ciudadania", "clave":"1234", "foto":"img","rol":"Admin"},
    "cesar":{"nombre": "Cesar","usuario":"cesar","td":"Cedula de Ciudadania", "clave":"1234", "foto":"img","rol":"Admin"},
    "wollman":{"nombre": "Wollman","usuario":"wollman","td":"Cedula de Ciudadania", "clave":"1234", "foto":"img","rol":"UsuarioFinal"},
    "camilo":{"nombre": "Camilo","usuario":"camilo","td":"Cedula de Ciudadania", "clave":"1234", "foto":"img","rol":"UsuarioFinal"},
}
productos={
    1:"Beattle",
    2:"Taos",
    3:"T-Cross TSI",
    4:"Gol",
}

#declaracion de variables
sesion_iniciada=False
nom=""
rol=""
resultado=""
busqueda=""
resultadoed=""
busquedaed=""
#funcion para inicalizar variables
def inivar():
    global sesion_iniciada,nom,rol,resultado,busqieda
    sesion_iniciada=False
    nom=""
    rol=""
    resultado=""
    busqueda=""

#ruta principal
@app.route("/")
def home():
    inivar()
    return render("inicio.html")

#ruta para ingresar
@app.route("/ingreso",methods=["GET", "POST"])
def ingreso():
    global sesion_iniciada
    global nom,rol
    #si el metodo es get envia al login, significa que no se ha logueado
    if request.method=="GET":
        return render("login.html",sesion_iniciada=sesion_iniciada)
    else:   
        #asigna a variables los campos del formulario login
        nom=request.form["nombre"]    
        pwd=request.form["psw"]    
        #verifica el usuario y la contraseña
        if nom in usuarios and pwd == usuarios[nom]["clave"]:
            sesion_iniciada=True
            rol=usuarios[nom]["rol"]
            return redirect("/servicios")
        else:
            return "usuario y/o contraseña incorrecta <a href='/ingreso'>Volver</a>"

#inicializa valores y redirige al Home
@app.route("/home")
def home1():
    inivar()
    return redirect("/")

#inicializa variables y redirige al login
@app.route("/salir")
def salir():
    inivar()
    return redirect("/ingreso")

@app.route("/volver",methods=["GET","POST"])
def volver():
    return redirect("/servicios")

@app.route("/servicios", methods=["GET"])
def servicios():
    return render("servicios.html",nom=nom,rol=rol)

@app.route("/servicios/dash", methods=["GET"])
def dash():
    return render("dashboard.html",nom=nom,rol=rol)
#//////////////////////////

#ruta que muestra perfil de usuario
@app.route("/usuarios/<id_usuario>", methods=["GET"])
def info_usuario(id_usuario):
    if id_usuario in usuarios:
        return render("pusuario.html",nom=nom,rol=rol,usuarios=usuarios,resultado=resultado)
    else:
        return f"error, el usuario {id_usuario} no existe"

#renderizar pagina edusuario
@app.route("/usuario/editar", methods=["GET"])
def editar_usuario():
    return render("edusuario.html",nom=nom,rol=rol,usuarios=usuarios,resultadoed=resultadoed)

#busqueda usuario para editar
@app.route("/busuarioe",methods=["POST"])
def busuarioe():
    global resultadoed,busquedaed
    busquedaed=""
    busquedaed=request.form["buscar"]
    #return f"{busqueda}"
    if busquedaed in usuarios:
        resultadoed=usuarios[busquedaed]
        return redirect("/usuario/editar")
    else:
        return "no encontrado"

@app.route("/gedicion",methods=["POST"])
def gedicion():
    
    global busquedaed,resultadoed,nom
    nombre=request.form["nom"]    
    usu=request.form["usu"] 
    tdoc=request.form["tdoc"] 
    clav=request.form["clav"] 
    foto=request.form["foto"] 
    rol=request.form["rol"]

    if usu == busquedaed:
        usuarios[usu]['nombre']=nombre
        usuarios[usu]['td']=tdoc
        usuarios[usu]['clave']=clav
        usuarios[usu]['foto']=foto
        usuarios[usu]['rol']=rol
        nom=usu
        resultadoed=""
        busquedaed=""
        return redirect("/usuario/editar")
        
    else:
        if usu in usuarios:
            return"usuario existe"
        else:
            nom=usu
            usuarios[usu]=usuarios.pop(busquedaed)
            usuarios[usu]['nombre']=nombre
            usuarios[usu]['usuario']=usu
            usuarios[usu]['td']=tdoc
            usuarios[usu]['clave']=clav
            usuarios[usu]['foto']=foto
            usuarios[usu]['rol']=rol
            resultadoed=""
            busquedaed=""
            return redirect("/usuario/editar")
             

@app.route("/salvar",methods=["POST"])
def salvar():
    nombre=request.form["nom"]    
    usu=request.form["usu"] 
    tdoc=request.form["tdoc"] 
    clav=request.form["clav"] 
    foto=request.form["foto"] 
    rol=request.form["rol"] 
    usuarios.setdefault(usu,{'nombre':nombre,'usuario':usu,'td':tdoc,'clave':clav,'foto':foto,'rol':rol})
    return redirect("/servicios")

@app.route("/usuario/buscar",methods=["GET"])
def busuario():
    return render("busuarios.html",nom=nom,rol=rol,usuarios=usuarios,resultado=resultado)

@app.route("/buscar",methods=["POST"])
def buscar():
    global resultado
    busqueda=""
    busqueda=request.form["buscar"]
    if busqueda in usuarios:
        resultado=usuarios[busqueda]
        return redirect("/usuario/buscar")
    else:
        return "no encontrado"

#Ruta para renderizar pagina de visualizar usuarios
@app.route("/usuarios/visualizar", methods=["GET"])
def vusuarios():
    return render("vusuarios.html",nom=nom,rol=rol,usuarios=usuarios)

#render al pagina eusuario
@app.route("/usuario/eliminar", methods=["GET"])
def eusuario():
    return render("eusuario.html",nom=nom,rol=rol,usuarios=usuarios,resultado=resultado)

"busca usuario a eliminar"
@app.route("/eliminar",methods=["POST"])
def eliminar():
    global resultado, busqueda
    busqueda=""
    busqueda=request.form["buscar"]
    if busqueda in usuarios:
        resultado=usuarios[busqueda]
        return redirect("/usuario/eliminar")
    else:
        return "no encontrado"

#elimina usuario seleccionado
@app.route("/eliminar2",methods=["POST"])
def eliminar2():
    global busqueda,resultado
    if busqueda!=nom:
        usuarios.pop(busqueda)
        busqueda=""
        resultado=""
        return redirect("/usuario/eliminar")
    else:
        return"no se puede eliminar usuario logueado"

@app.route("/usuario/crear", methods=["GET"])
def cusuario():
    return render("cusuario.html",nom=nom,rol=rol,usuarios=usuarios)

#renderiza pagina cambio de contraseña
@app.route("/usuario/cambiar_password",methods=["GET"])
def cbiopwd():
    return render("cbiopwd.html",nom=nom,rol=rol,usuarios=usuarios,resultado=resultado)

#Realiza el cambio de contraseña
@app.route("/cbiopwdok",methods=["POST"])
def cbiopwdok():
    global nom
    cactual=request.form["cactual"] 
    #return f"{cactual}{nom}"
    if cactual == usuarios[nom]["clave"]:
        cnueva=request.form["cnueva"] 
        ccnueva=request.form["ccnueva"] 
        if cnueva==ccnueva:
            usuarios[nom]["clave"]=cnueva
        else:
            return "no coinciden las contraseñas"
    else:
        return "contraseña actual incorrecta"
    return redirect("/servicios")

#rutas sin usar
# @app.route("/perfil", methods=["GET","POST"])
# def perfil():
#     return "perfil"

# @app.route("/producto/<id_producto>", methods=["GET"])
# def info_producto(id_producto):
#     try:
#         id_producto=int(id_producto)
#     except Exception as e:
#         id_noticia=0
    
#     if id_producto in productos:
#         return f"estas viendo el producto: {id_producto}"   
#     else:
#         return f"error, el usuario {id_producto} no existe"

# @app.route("/productos", methods=["GET"])
# def productos():
#     return render("productos.html",nom=nom,rol=rol)
#hasta aqui   

if __name__== "__main__":
    app.run(debug=True)