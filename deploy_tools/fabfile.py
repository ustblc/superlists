from fabric.contrib.files import append, exists, sed
from fabric.api import env, run
import random

REPO_URL = "https://github.com/ustblc/superlists.git"


def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    source_folder = site_folder + "/source"
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_venv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for sub_folder in ("database", "static", "venv", "source"):
        run(f"mkdir -p {site_folder}/{sub_folder}")


def _get_latest_source(source_folder):
    if exists(source_folder + "/.git"):
        run(f"cd {source_folder} && git pull origin master")
    else:
        run(f"git clone {REPO_URL} {source_folder}")


def _update_settings(source_folder, sitename):
    setting_path = source_folder + "/superlists/settings.py"
    sed(setting_path, "DEBUG = True", "DEBUG = False")
    sed(setting_path, "ALLOWED_HOSTS = .+$", f'ALLOWED_HOSTS = ["{sitename}"]')
    secret_key_file = source_folder + "/superlists/secret_key.py"
    if not exists(secret_key_file):
        chars = "sdjklfjsfkl!~sada.@#$@#(_+s"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f"SECRET_KEY = '{key}'")
    append(setting_path, "\nfrom .secret_key import SECRET_KEY")


def _update_venv(source_folder):
    venv_folder = source_folder + "/../venv"
    if not exists(venv_folder + "/bin/pip"):
        run(f"virtualenv {venv_folder}")
    run(f"{venv_folder}/bin/pip install -r {source_folder}/requirements.txt")


def _update_static_files(source_folder):
    run(
        f"cd {source_folder}"
        " && ../venv/bin/python manage.py collectstatic --noinput"
    )


def _update_database(source_folder):
    run(
        f"cd {source_folder}"
        " && ../venv/bin/python manage.py migrate --noinput"
    )
