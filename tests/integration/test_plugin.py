import os
import pathlib
import subprocess

import pytest
from flytekit.common import launch_plan
from flytekit.models import literals

PROJECT = "flytesnacks"
DOMAIN = "development"
VERSION = os.getpid()

@pytest.fixture(scope="session")
def flyte_workflows_register(request):
    proto_path = request.config.getoption("--proto-path")
    subprocess.check_call(
        f"flytectl register files {proto_path} -p {PROJECT} -d {DOMAIN} --version=v{VERSION}",
        shell=True,
    )


def test_stub(flyteclient, flyte_workflows_register):
    projects = flyteclient.list_projects_paginated(limit=5, token=None)
    assert len(projects) <= 5


def test_launch_workflow(flyteclient, flyte_workflows_register):
    lp = launch_plan.SdkLaunchPlan.fetch(
        "flytesnacks",
        "development",
        "workflows.hello_world.my_wf",
        f"v{VERSION}",
    )
    execution = lp.launch_with_literals(
        "flytesnacks", "development", literals.LiteralMap({})
    )
    print(execution.id.name)
