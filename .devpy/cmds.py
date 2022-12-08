import click
from devpy import util
from devpy.cmds.util import get_site_packages, set_pythonpath, run


@click.command()
@click.option(
    "-test-dep", is_flag=True, help="If to install test dependecies"
)
@click.option(
    "-doc-dep", is_flag=True, help="If to install test dependecies"
)
def install_dependencies(test_dep=False, doc_dep=False):
    """Command that accesses `pyproject.toml` configuration"""
    config = util.get_config()
    default_dependencies = config["project"]['dependencies']
    print("Installing dependencies", default_dependencies)
    run(
        ["pip", "install"] + list(default_dependencies),
    )
    if test_dep:
        test_dependencies = config["project.optional-dependencies"]['test']
        print("Installing test-dependencies", config["project.optional-dependencies"]['test'])
        run(
            ["pip", "install"] + list(test_dependencies),
        )
    if doc_dep:
        doc_dependencies = config["project.optional-dependencies"]['doc']
        print("Installing doc-dependencies", doc_dependencies)
        run(
            ["pip", "install"] + list(doc_dependencies),
        )


@click.command()
@click.option(
    "--build-dir", default="build", help="Build directory; default is `$PWD/build`"
)
@click.argument("codecov_args", nargs=-1)
def codecov(build_dir, codecov_args):
    """🔧 Run codecov in the build directory
    CODECOV_ARGS are passed through directly to codecov, e.g.:
    ./dev.py codecov -- -v
    """

    site_path = get_site_packages(build_dir)
    set_pythonpath(build_dir)

    run(
        ["codecov"] + list(codecov_args),
        cwd=site_path,
    )