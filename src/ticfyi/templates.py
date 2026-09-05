import hashlib
from http import HTTPStatus
import os
from pathlib import Path
import shutil
import subprocess
from typing import Final

from fastapi import Response
from fastapi.templating import Jinja2Templates
from PIL import Image
from rcssmin import cssmin
from rjsmin import jsmin

from ticfyi.webring import WEB_RING_MEMBERS


__all__: tuple[str, ...] = (
    "templates",
)


def _get_most_recent_commit_hash() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip() or "unknown"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


class TemplateServer(Jinja2Templates):
    def __init__(self, directory: str) -> None:
        self._served_files: dict[str, str] = {}
        self._most_recent_commit_hash = _get_most_recent_commit_hash()
        super().__init__(directory=directory)
        self.env.filters["intcomma"] = lambda x: f"{int(x):,}"

    def _serve_images(self) -> None:
        image_dir = "src/ticfyi/public/images"
        for dirpath, _, filenames in os.walk(image_dir):
            rel_dir = os.path.relpath(dirpath, image_dir)
            if rel_dir == "writing":
                continue
            out_dir = os.path.normpath(os.path.join("_served/static/images", rel_dir))
            os.makedirs(out_dir, exist_ok=True)

            for file in filenames:
                file_name, file_ext = os.path.splitext(file)
                if file_ext not in (".png", ".jpg", ".jpeg", ".gif"):
                    continue

                avif_file_path = f"static/images/{rel_dir}/{file_name}.avif"
                if Path(f"_served/{avif_file_path}").exists():
                    self._served_files[os.path.normpath(f"public/images/{rel_dir}/{file}")] = avif_file_path
                    continue

                image = Image.open(os.path.join(dirpath, file))
                avif_path = os.path.join(out_dir, f"{file_name}.avif")
                image.save(avif_path, optimize=True, quality=50, format="AVIF", save_all=True)

                avif_image = Image.open(avif_path)
                pub_key = os.path.normpath(f"public/images/{rel_dir}/{file}")

                if avif_image.size > image.size:
                    # if the AVIF image is larger than the original, we will serve the original instead.
                    os.remove(avif_path)
                    image.save(os.path.join(out_dir, file), optimize=True, quality=50)
                    self._served_files[pub_key] = os.path.normpath(f"static/images/{rel_dir}/{file}")

                else:
                    self._served_files[pub_key] = os.path.normpath(avif_file_path)

    def _serve_css(self) -> None:
        css_dir = "src/ticfyi/public/css"
        os.makedirs("_served/static/css", exist_ok=True)
        for file in os.listdir(css_dir):
            if not file.endswith(".css"):
                continue
            file_name, _ = os.path.splitext(file)
            with open(f"{css_dir}/{file}", "r") as f:
                css_content = f.read()
            minified_css = str(cssmin(css_content))
            md5hash = hashlib.md5(css_content.encode()).hexdigest()[:6]
            new_file_name = f"{file_name}.{md5hash}.css"
            with open(f"_served/static/css/{new_file_name}", "w") as f:
                f.write(str(minified_css))
            self._served_files["public/css/" + file] = f"static/css/{new_file_name}"

    def _serve_js(self) -> None:
        js_dir = "src/ticfyi/public/js"
        os.makedirs("_served/static/js", exist_ok=True)
        for file in os.listdir(js_dir):
            if not file.endswith(".js"):
                continue
            file_name, _ = os.path.splitext(file)
            with open(f"{js_dir}/{file}", "r") as f:
                js_content = f.read()
            minified_js = str(jsmin(js_content))
            md5hash = hashlib.md5(js_content.encode()).hexdigest()[:6]
            new_file_name = f"{file_name}.{md5hash}.js"
            with open(f"_served/static/js/{new_file_name}", "w") as f:
                f.write(str(minified_js))
            self._served_files["public/js/" + file] = f"static/js/{new_file_name}"

    def _serve_misc(self) -> None:
        fonts_dir = "src/ticfyi/public/fonts"
        os.makedirs("_served/static/fonts", exist_ok=True)
        for file in os.listdir(fonts_dir):
            if not file.endswith((".woff", ".woff2", ".ttf", ".otf")):
                continue
            shutil.copyfile(f"{fonts_dir}/{file}", f"_served/static/fonts/{file}")
            self._served_files["public/fonts/" + file] = f"static/fonts/{file}"

    def load(self) -> None:
        self._serve_images()
        self._serve_css()
        self._serve_js()
        self._serve_misc()

    def _get_file(self, file_path: str) -> str:
        path = self._served_files.get(file_path, "")
        return f"/{path}" if path else ""

    def _get_file_type(self, file_path: str) -> str:
        import mimetypes

        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or "application/octet-stream"

    def serve_template(self, template_name: str, status_code: HTTPStatus, context: dict) -> Response:
        template = self.get_template(template_name)
        template.globals.update({
            "get_file": self._get_file,
            "get_file_type": self._get_file_type,
            "most_recent_commit_hash": self._most_recent_commit_hash,
            "WEB_RING_MEMBERS": WEB_RING_MEMBERS,
        })
        template_content = template.render(context)
        return Response(
            content=template_content,
            media_type="text/html",
            status_code=status_code,
        )


templates = TemplateServer(
    directory="src/ticfyi/templates",
)
