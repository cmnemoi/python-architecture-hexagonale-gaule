import re
from pathlib import Path

import pytest
from pytestarch import EvaluableArchitecture, Rule, get_evaluable_architecture

_SOURCES = Path(__file__).parent.parent / "src"
_DOMAINE = "src.pythonoramix.domain"
_API = "src.pythonoramix.apix"
_ADAPTATEURS = "src.pythonoramix.adapters"
_INFRASTRUCTURE = "src.pythonoramix.infrastructure"
_COMPOSITION = "src.pythonoramix.config"
_FASTAPI = "fastapi"


@pytest.fixture(scope="module")
def architecture() -> EvaluableArchitecture:
    return get_evaluable_architecture(
        str(_SOURCES),
        str(_SOURCES / "pythonoramix"),
        exclude_external_libraries=False,
    )


# @spec architecture::domaine-isole
@pytest.mark.parametrize("module_interdit", [_INFRASTRUCTURE, _ADAPTATEURS, _API, _COMPOSITION, _FASTAPI])
def test_le_domaine_n_importe_ni_l_extérieur_ni_fastapi(
    architecture: EvaluableArchitecture, module_interdit: str
) -> None:
    _vérifier_interdiction(architecture, _DOMAINE, module_interdit)


# @spec architecture::api-depend-du-domaine
@pytest.mark.parametrize("module_interdit", [_INFRASTRUCTURE, _ADAPTATEURS, _COMPOSITION])
def test_l_api_dépend_uniquement_du_domaine(architecture: EvaluableArchitecture, module_interdit: str) -> None:
    _vérifier_interdiction(architecture, _API, module_interdit)


# @spec architecture::adaptateurs-relient-domaine-et-infrastructure
@pytest.mark.parametrize("module_interdit", [_API, _COMPOSITION, _FASTAPI])
def test_les_adaptateurs_relient_uniquement_domaine_et_infrastructure(
    architecture: EvaluableArchitecture, module_interdit: str
) -> None:
    _vérifier_interdiction(architecture, _ADAPTATEURS, module_interdit)


def _vérifier_interdiction(architecture: EvaluableArchitecture, module: str, module_interdit: str) -> None:
    module_ou_sous_module_interdit = rf"^{re.escape(module_interdit)}(\.|$)"
    Rule().modules_that().are_sub_modules_of(module).should_not().import_modules_that().have_name_matching(
        module_ou_sous_module_interdit
    ).assert_applies(architecture)
