"""Genera documentación Markdown de las clases del API desde sus docstrings.

Uso:
    python docs/generate_api_docs.py

Genera archivos en docs/api/{modulo}/{Clase}.md para cada clase que
tenga docstring en el código fuente de escatastrolib. Formatea
docstrings estilo Google (Args, Returns, Raises, Example) como Markdown
listo para wiki.
"""

from __future__ import annotations

import ast
import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src" / "escatastrolib"
DOCS_DIR = Path(__file__).resolve().parent / "api"

MODULES_TO_SCAN = [
    # Models
    "models/Callejero.py",
    "models/RegionCatastral.py",
    "models/GeometriaCatastral.py",
    "models/Construction.py",
    "models/ValorUrbano.py",
    "models/ValorRustico.py",
    "models/Documentacion.py",
    "models/ParcelaCatastral.py",
    # Clients
    "clients/base.py",
    "clients/CatastroES.py",
    "clients/Araba.py",
    "clients/Bizkaia.py",
    "clients/Gipuzkoa.py",
    "clients/Navarra.py",
    # Services
    "services/ParcelaCatastral.py",
    "services/Municipio.py",
    "services/Calle.py",
    # Providers
    "providers/CatastroES/Callejero.py",
    "providers/CatastroES/CartoCiudad.py",
    "providers/CatastroES/Coordenadas.py",
    "providers/CatastroES/Croquis.py",
    "providers/CatastroES/INSPIREBuildings.py",
    "providers/CatastroES/INSPIREParcelas.py",
    "providers/CatastroES/MapaValoresRusticos.py",
    "providers/CatastroES/MapaValoresUrbanos.py",
    # Composers
    "composers/ParcelaCatastral.py",
    "composers/mappers/GeometriaMapper.py",
    "composers/mappers/ConstructionMapper.py",
    "composers/mappers/ParcelaRusticaMapper.py",
    "composers/mappers/ParcelaUrbanaMapper.py",
    "composers/mappers/MunicipioMapper.py",
    "composers/mappers/DocumentoMapper.py",
    "composers/mappers/CalleMapper.py",
    "composers/mappers/ValorRusticoMapper.py",
    "composers/mappers/ValorUrbanoMapper.py",
    "composers/mappers/RegionCatastralMapper.py",
    # Parsers
    "parsers/CatastroES/Callejero/parser.py",
    "parsers/CatastroES/CartoCiudad/parser.py",
    "parsers/CatastroES/Coordenadas/parser.py",
    "parsers/CatastroES/Croquis/parser.py",
    "parsers/CatastroES/INSPIREBuildings/parser.py",
    "parsers/CatastroES/INSPIREParcels/parser.py",
    "parsers/CatastroES/MapaValoresRusticos/parser.py",
    "parsers/CatastroES/MapaValoresUrbanos/parser.py",
    "parsers/common/dtos_geometria.py",
    "parsers/typing.py",
    # Exporters
    "exporters/_base.py",
    "exporters/json_exporter.py",
    "exporters/csv_exporter.py",
    "exporters/geojson_exporter.py",
    "exporters/gis_exporters.py",
    "exporters/dataframe_exporter.py",
    # Errors
    "errors/ErrorServidorDGC.py",
    # Utils
    "utils/Mappings.py",
    "utils/Parsers.py",
    "utils/territories.py",
]


def get_module_name(filepath: str) -> str:
    """Obtiene el nombre del módulo (carpeta) a partir de la ruta del archivo."""
    rel = os.path.relpath(filepath, str(SRC_DIR))
    parts = Path(rel).parts
    if parts[0] == "composers" and len(parts) > 2:
        return "composers/mappers"
    return parts[0]


def get_method_signature(func_node: ast.FunctionDef) -> str:
    """Extrae la firma del método como string."""
    args = func_node.args
    parts = []

    # Args posicionales (excluyendo 'self')
    defaults_offset = len(args.args) - len(args.defaults)
    for i, arg in enumerate(args.args[1:]):  # skip 'self'
        name = arg.arg
        annotation = ""
        if arg.annotation:
            try:
                annotation = f": {ast.unparse(arg.annotation)}"
            except Exception:
                pass
        default_idx = i - defaults_offset
        if default_idx >= 0 and default_idx < len(args.defaults):
            try:
                default_val = ast.unparse(args.defaults[default_idx])
                parts.append(f"{name}{annotation} = {default_val}")
            except Exception:
                parts.append(f"{name}{annotation}")
        else:
            parts.append(f"{name}{annotation}")

    # *args
    if args.vararg:
        try:
            ann = ast.unparse(args.vararg.annotation) if args.vararg.annotation else ""
            parts.append(f"*{args.vararg.arg}" + (f": {ann}" if ann else ""))
        except Exception:
            parts.append(f"*{args.vararg.arg}")

    # keyword-only args
    kw_defaults_offset = len(args.kwonlyargs) - len(args.kw_defaults)
    for i, arg in enumerate(args.kwonlyargs):
        name = arg.arg
        annotation = ""
        if arg.annotation:
            try:
                annotation = f": {ast.unparse(arg.annotation)}"
            except Exception:
                pass
        default_idx = i - kw_defaults_offset
        if default_idx >= 0 and default_idx < len(args.kw_defaults) and args.kw_defaults[default_idx]:
            try:
                default_val = ast.unparse(args.kw_defaults[default_idx])
                parts.append(f"{name}{annotation} = {default_val}")
            except Exception:
                parts.append(f"{name}{annotation}")
        else:
            parts.append(f"{name}{annotation}")

    # **kwargs
    if args.kwarg:
        try:
            ann = ast.unparse(args.kwarg.annotation) if args.kwarg.annotation else ""
            parts.append(f"**{args.kwarg.arg}" + (f": {ann}" if ann else ""))
        except Exception:
            parts.append(f"**{args.kwarg.arg}")

    return ", ".join(parts)


def format_google_docstring(docstring: str) -> str:
    """Formatea un docstring estilo Google a Markdown.

    Detecta secciones Args, Returns, Raises, Example, Attributes y las
    convierte a formato Markdown con tablas y bloques de código.
    """
    if not docstring:
        return ""

    lines = docstring.strip().split("\n")
    result = []
    current_section = None
    section_items = []

    section_headers = {
        "Args": "Argumentos",
        "Arguments": "Argumentos",
        "Returns": "Retorna",
        "Return": "Retorna",
        "Raises": "Excepciones",
        "Example": "Ejemplo",
        "Examples": "Ejemplos",
        "Attributes": "Atributos",
        "Note": "Nota",
        "Notes": "Notas",
        "See Also": "Ver también",
        "Todo": "Pendiente",
    }

    def flush_section():
        """Vacía los items acumulados de la sección actual."""
        if current_section and section_items:
            header = section_headers.get(current_section, current_section)
            result.append(f"**{header}:**")
            result.append("")
            for item in section_items:
                result.append(f"- {item}")
            result.append("")

    for line in lines:
        stripped = line.strip()

        # Detectar inicio de sección Google-style
        section_match = re.match(r"^(Args|Arguments|Returns|Return|Raises|Example|Examples|Attributes|Note|Notes|See Also|Todo)\s*:", stripped)
        if section_match:
            flush_section()
            current_section = section_match.group(1)
            section_items = []
            continue

        # Si estamos dentro de una sección, acumular items
        if current_section:
            if stripped.startswith("- ") or stripped.startswith("* "):
                section_items.append(stripped[2:].strip())
            elif re.match(r"^\w[\w\s]*:\s", stripped):
                # Línea tipo "param_name: description"
                section_items.append(f"`{stripped.split(':')[0].strip()}` — {''.join(stripped.split(':')[1:]).strip()}")
            elif stripped == "":
                # Línea vacía puede significar fin de sección
                if section_items:
                    flush_section()
                    current_section = None
                    section_items = []
                continue
            else:
                # Continuación del item anterior
                if section_items:
                    section_items[-1] += " " + stripped
                else:
                    section_items.append(stripped)
        else:
            # Texto fuera de sección
            if stripped:
                result.append(stripped)

    flush_section()

    return "\n".join(result)


def extract_class_info(filepath: str) -> list[dict]:
    """Extrae información de clases y sus docstrings de un archivo Python."""
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node)
            if docstring:
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        bases.append(base.attr)

                attributes = []
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        attr_name = item.target.id
                        attr_type = ""
                        if item.annotation:
                            try:
                                attr_type = ast.unparse(item.annotation)
                            except Exception:
                                attr_type = ""
                        default = ""
                        if item.value:
                            try:
                                default = ast.unparse(item.value)
                            except Exception:
                                default = ""
                        attributes.append({
                            "name": attr_name,
                            "type": attr_type,
                            "default": default,
                        })

                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if item.name.startswith("_") and item.name != "__init__":
                            continue
                        method_docstring = ast.get_docstring(item)
                        is_property = any(
                            isinstance(d, ast.Name) and d.id == "property"
                            for d in item.decorator_list
                        )
                        is_staticmethod = any(
                            isinstance(d, ast.Name) and d.id == "staticmethod"
                            for d in item.decorator_list
                        )
                        signature = get_method_signature(item)
                        methods.append({
                            "name": item.name,
                            "docstring": method_docstring,
                            "is_property": is_property,
                            "is_static": is_staticmethod,
                            "signature": signature,
                        })

                classes.append({
                    "name": node.name,
                    "bases": bases,
                    "docstring": docstring,
                    "attributes": attributes,
                    "methods": methods,
                })

    return classes


def generate_markdown(class_info: dict, module_name: str) -> str:
    """Genera el contenido Markdown para una clase."""
    lines = []

    # Título
    lines.append(f"# {class_info['name']}")
    lines.append("")

    # Módulo
    lines.append(f"**Módulo:** `{module_name}`")
    lines.append("")

    # Herencia
    if class_info["bases"]:
        bases_str = ", ".join(f"`{b}`" for b in class_info["bases"])
        lines.append(f"**Hereda de:** {bases_str}")
        lines.append("")

    # Docstring de clase (formateado)
    formatted_class_doc = format_google_docstring(class_info["docstring"])
    lines.append(formatted_class_doc)
    lines.append("")

    # Atributos (si es dataclass)
    if class_info["attributes"]:
        lines.append("## Atributos")
        lines.append("")
        lines.append("| Atributo | Tipo | Default |")
        lines.append("|----------|------|---------|")
        for attr in class_info["attributes"]:
            tipo = f"`{attr['type']}`" if attr["type"] else "-"
            default = f"`{attr['default']}`" if attr["default"] else "-"
            lines.append(f"| `{attr['name']}` | {tipo} | {default} |")
        lines.append("")

    # Métodos
    if class_info["methods"]:
        lines.append("## Métodos")
        lines.append("")
        for method in class_info["methods"]:
            # Firma del método
            prefix = "@staticmethod " if method["is_static"] else ""
            suffix = " *(property)*" if method["is_property"] else ""
            lines.append(f"### `{prefix}{method['name']}({method['signature']})`{suffix}")
            lines.append("")

            # Docstring del método formateado
            if method["docstring"]:
                formatted = format_google_docstring(method["docstring"])
                lines.append(formatted)
            else:
                lines.append("*Sin documentación.*")
            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines)


def main():
    """Función principal: genera los archivos Markdown."""
    if DOCS_DIR.exists():
        for f in DOCS_DIR.rglob("*.md"):
            f.unlink()
        for d in reversed(list(DOCS_DIR.rglob("*"))):
            if d.is_dir():
                try:
                    d.rmdir()
                except OSError:
                    pass

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    total_classes = 0

    for module_file in MODULES_TO_SCAN:
        filepath = SRC_DIR / module_file
        if not filepath.exists():
            print(f"⚠ No encontrado: {filepath}")
            continue

        classes = extract_class_info(str(filepath))
        module_name = get_module_name(str(filepath))

        for class_info in classes:
            md_content = generate_markdown(class_info, module_name)

            module_dir = DOCS_DIR / module_name
            module_dir.mkdir(parents=True, exist_ok=True)

            md_path = module_dir / f"{class_info['name']}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)

            print(f"✓ {module_name}/{class_info['name']}.md")
            total_classes += 1

    print(f"\n✅ Generados {total_classes} archivos Markdown en {DOCS_DIR}")


if __name__ == "__main__":
    main()
