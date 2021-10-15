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
    4:"Renold4",
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
    if nom!="":
        return redirect("/servicios")
    else:
        return redirect("/ingreso")

@app.route("/servicios", methods=["GET"])
def servicios():
    if nom!="":
        return render("servicios.html",nom=nom,rol=rol)
    else:
        return redirect("/ingreso")

@app.route("/servicios/dash", methods=["GET"])
def dash():
    if nom!="":
        return render("dashboard.html",nom=nom,rol=rol)
    else:
        return redirect("/ingreso")

#//////////////////////phphphphprrr

#ruta que muestra perfil de usuario
@app.route("/usuarios/<id_usuario>", methods=["GET"])
def info_usuario(id_usuario):
    if nom!="":
        if id_usuario in usuarios:
            return render("pusuario.html",nom=nom,rol=rol,usuarios=usuarios,resultado=resultado)
        else:
            return f"error, el usuario {id_usuario} no existe"
    else:
        return redirect("/ingreso")

#renderizar pagina edusuario
@app.route("/usuario/editar", methods=["GET"])
def editar_usuario():
    if nom!="":
        return render("edusuario.html",nom=nom,rol=rol,usuarios=usuarios,resultadoed=resultadoed)
    else:
        return redirect("/ingreso")

#busqueda usuario para editar
@app.route("/busuarioe",methods=["POST"])
def busuarioe():
    if nom != "":
        global resultadoed,busquedaed
        busquedaed=""
        busquedaed=request.form["buscar"]
        #return f"{busqueda}"
        if busquedaed in usuarios:
            resultadoed=usuarios[busquedaed]
            return redirect("/usuario/editar")
        else:
            return "no encontrado"
    else:
        return redirect("/ingreso")

@app.route("/gedicion",methods=["POST"])
def gedicion():
    global busquedaed,resultadoed,nom
    if nom != "":
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
            #nom=usu
            resultadoed=""
            busquedaed=""
            return redirect("/usuario/editar")
            
        else:
            if usu in usuarios:
                return"usuario existe"
            else:
                usuarios[usu]=usuarios.pop(busquedaed)
                usuarios[usu]['nombre']=nombre
                usuarios[usu]['usuario']=usu
                usuarios[usu]['td']=tdoc
                usuarios[usu]['clave']=clav
                usuarios[usu]['foto']=foto
                usuarios[usu]['rol']=rol
                if nom==busquedaed:
                    nom=usu
                
                resultadoed=""
                busquedaed=""
                return redirect("/usuario/editar")
    else:
        return redirect("/ingreso")
             

@app.route("/salvar",methods=["POST"])
def salvar():
    if nom != "":
        nombre=request.form["nom"]    
        usu=request.form["usu"] 
        tdoc=request.form["tdoc"] 
        clav=request.form["clav"] 
        foto=request.form["foto"] 
        rol=request.form["rol"] 
        usuarios.setdefault(usu,{'nombre':nombre,'usuario':usu,'td':tdoc,'clave':clav,'foto':foto,'rol':rol})
        return redirect("/servicios")
    else:
        return redirect("/ingreso")

@app.route("/usuario/buscar",methods=["GET"])
def busuario():
    if nom!="":
        return render("busuarios.html",nom=nom,rol=rol,usuarios=usuarios,resultado=resultado)
    else:
        return redirect("/ingreso")

@app.route("/buscar",methods=["POST"])
def buscar():
    if nom!="":
        global resultado
        busqueda=""
        busqueda=request.form["buscar"]
        if busqueda in usuarios:
            resultado=usuarios[busqueda]
            return redirect("/usuario/buscar")
        else:
            return "no encontrado"
    else:
        return redirect("/ingreso")

#Ruta para renderizar pagina de visualizar usuarios
@app.route("/usuarios/visualizar", methods=["GET"])
def vusuarios():
    if nom!="":
        return render("vusuarios.html",nom=nom,rol=rol,usuarios=usuarios)
    else:
        return redirect("/ingreso")

#render al pagina eusuario
@app.route("/usuario/eliminar", methods=["GET"])
def eusuario():
    if nom!="":    
        return render("eusuario.html",nom=nom,rol=rol,usuarios=usuarios,        resultado=resultado)
    else:
        return redirect("/ingreso")

#busca usuario a eliminar
@app.route("/eliminar",methods=["POST"])
def eliminar():
    if nom!="":
        global resultado, busqueda
        busqueda=""
        busqueda=request.form["buscar"]
        if busqueda in usuarios:
            resultado=usuarios[busqueda]
            return redirect("/usuario/eliminar")
        else:
            return "no encontrado"
    else:
        return redirect("/ingreso")

#elimina usuario seleccionado
@app.route("/eliminar2",methods=["POST"])
def eliminar2():
    if nom!="":
        global busqueda,resultado
        if busqueda!=nom:
            usuarios.pop(busqueda)
            busqueda=""
            resultado=""
            return redirect("/usuario/eliminar")
        else:
            return"no se puede eliminar usuario logueado"
    else:
        return redirect("/ingreso")

@app.route("/usuario/crear", methods=["GET"])
def cusuario():
    if nom !="":
        return render("cusuario.html",nom=nom,rol=rol,usuarios=usuarios)
    else:
        return redirect("/ingreso")

#renderiza pagina cambio de contraseña
@app.route("/usuario/cambiar_password",methods=["GET"])
def cbiopwd():
    if nom !="":
        return render("cbiopwd.html",nom=nom,rol=rol,usuarios=usuarios,resultado=resultado)
    else:
        return redirect("/ingreso")

#Realiza el cambio de contraseña
@app.route("/cbiopwdok",methods=["POST"])
def cbiopwdok():
    global nom
    if nom !="":
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
    else:
        return redirect("/ingreso")

#Aqui empieza la funcionalidad del menu de proveedores
    
#Aqui comienzo la funcion guardar con su ruta
#Creando diccionario vacio
proveedores = {}

#Aqui comienzan la ruta guardar proveedor/render a pagina de creacion
@app.route("/crear/proveedor")
def crearPod():
    return render("crearProvee.html", proveedores = proveedores, nom=nom, rol=rol, usuarios=usuarios)

#Esta es la ruta, más la funcion guardar
@app.route("/guardar", methods = ["GET","POST"])
def agregar():
    #Tomando los datos de la variable pasadas por el input
    codigo = request.form["codigo"]
    name = request.form["name"]
    razonsocial = request.form["razonsocial"]
    domicilio = request.form["domicilio"]
    postal = request.form["postal"]
    localidad = request.form["localidad"]
    provincia = request.form["provincia"]
    pais = request.form["pais"]
    tlf = request.form["tlf"]
    correo = request.form["correo"]
    web = request.form["web"]
    rut = request.form["rut"]

    #Aqui se agregan los datos tomados al diccionario PROVEEDORES
    proveedores[codigo] = {"nombre": name, "rsocial": razonsocial, "domicilio": domicilio, "postal": postal, "localidad": localidad, "provincia": provincia, "pais": pais, "telefono": tlf, "correo": correo, "web": web, "rut": rut}
    return redirect("/crear/proveedor")

    #Metodo eliminar

#Ruta plantilla eliminar proveedor
@app.route("/eliminar/proveedor" )
def delproveedor():
    return render("eliminarprovee.html", proveedores = proveedores, nom=nom, rol=rol, usuarios=usuarios)

#Ruta que recibe los parametros y aplica funcion elimninar
@app.route("/eliminar_proveedor", methods = ["GET","POST"])
def eliminar_proveedor():
    dato = request.form["eliminarp"]
    del (proveedores[dato]) 

    return redirect("/eliminar/proveedor")

#Ruta de busqueda de proveeedor
@app.route("/buscar/proveedor")
def buscar_proveedor():
    return render("buscarprovee.html", busqueda = busqueda, nom=nom, rol=rol, usuarios=usuarios)

busqueda = []

#Funcion buscar proveedor
@app.route("/buscar_proveedor", methods =["POST"])
def buscar_prov():
    global busqueda
    provee_buscado = ""
    provee_buscado = request.form["datos"]
    
    if provee_buscado in proveedores:
        busqueda = proveedores[provee_buscado]
        return redirect("/buscar/proveedor")
    
    else:
        return " Proveedor no encontrado"

#Aqui comienza el editar proveedor
busqueda2 = []
provee_buscado2 = ""


#Ruta que lleva ala pagina editar
@app.route("/editar/proveedor")
def editar_prov():
    return render("editar_prov.html",  proveedores = proveedores, busqueda2 = busqueda2, nom=nom, rol=rol, usuarios=usuarios)

@app.route("/editar", methods = ["GET","POST"])
def editar():
    global busqueda2
    global provee_buscado2 
    provee_buscado2 = request.form["datos2"]
    if provee_buscado2 in proveedores:
        busqueda2 = proveedores[provee_buscado2]

        return redirect("/editar/proveedor")

    else:
        return "Proveedor no encontrado"

@app.route("/guardaredit", methods = ["GET", "POST"])
def guardar_edit():

    #Tomando los datos de la variable pasadas por el input
    
    name = request.form["name2"]
    razonsocial = request.form["razonsocial2"]
    domicilio = request.form["domicilio2"]
    postal = request.form["postal2"]
    localidad = request.form["localidad2"]
    provincia = request.form["provincia2"]
    pais = request.form["pais2"]
    tlf = request.form["tlf2"]
    correo = request.form["correo2"]
    web = request.form["web2"]
    rut = request.form["rut2"]

    #Aqui se agregan los valores editados a proveedores
    proveedores[provee_buscado2] = {"nombre": name, "rsocial": razonsocial, "domicilio": domicilio, "postal": postal, "localidad": localidad, "provincia": provincia, "pais": pais, "telefono": tlf, "correo": correo, "web": web, "rut": rut}
    return redirect("/editar/proveedor")

@app.route("/proveedores")
def list_proveedores():
    return render("resultado.html", proveedores = proveedores, nom=nom, rol=rol, usuarios=usuarios)


if __name__== "__main__":
    app.run(host='0.0.0.0')