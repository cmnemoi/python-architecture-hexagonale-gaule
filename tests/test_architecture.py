import re
from pathlib import Path

import pytest
from pytestarch import EvaluableArchitecture, Rule, get_evaluable_architecture


# @spec architecture::domaine-isole
@pytest.mark.parametrize(
    "module_interdit",
    [
        "src.pythonoramix.infrastructure",
        "src.pythonoramix.adapters",
        "src.pythonoramix.apix",
        "src.pythonoramix.config",
        "fastapi",
    ],
)
def test_le_domaine_n_importe_ni_l_extérieur_ni_fastapi(
    architecture: EvaluableArchitecture, module_interdit: str
) -> None:
    _vérifier_l_interdiction(architecture, "src.pythonoramix.domain", module_interdit)


# @spec architecture::api-depend-du-domaine
@pytest.mark.parametrize(
    "module_interdit",
    [
        "src.pythonoramix.infrastructure",
        "src.pythonoramix.adapters",
        "src.pythonoramix.config",
    ],
)
def test_l_api_dépend_uniquement_du_domaine(architecture: EvaluableArchitecture, module_interdit: str) -> None:
    _vérifier_l_interdiction(architecture, "src.pythonoramix.apix", module_interdit)


# @spec architecture::adaptateurs-relient-domaine-et-infrastructure
@pytest.mark.parametrize(
    "module_interdit",
    [
        "src.pythonoramix.apix",
        "src.pythonoramix.config",
        "fastapi",
    ],
)
def test_les_adaptateurs_relient_uniquement_domaine_et_infrastructure(
    architecture: EvaluableArchitecture, module_interdit: str
) -> None:
    _vérifier_l_interdiction(architecture, "src.pythonoramix.adapters", module_interdit)


@pytest.fixture(scope="module")
def architecture() -> EvaluableArchitecture:
    sources = Path(__file__).parent.parent / "src"
    return get_evaluable_architecture(
        str(sources),
        str(sources / "pythonoramix"),
        exclude_external_libraries=False,
    )


def _vérifier_l_interdiction(architecture: EvaluableArchitecture, module: str, module_interdit: str) -> None:
    module_ou_sous_module_interdit = rf"^{re.escape(module_interdit)}(\.|$)"
    Rule().modules_that().are_sub_modules_of(module).should_not().import_modules_that().have_name_matching(
        module_ou_sous_module_interdit
    ).assert_applies(architecture)
