import pytest
from unittest.mock import patch
from src.utils.oci_utils import upload_to_oci


# Teste 1: Garantir que o upload é pulado se não estiver no Airflow
def test_upload_skipped_locally():
    with patch.dict("os.environ", {}, clear=True):  # Simula ambiente sem AIRFLOW_HOME
        result = upload_to_oci("fake_file.parquet", "test_object.parquet")
        assert result is None  # A função deve retornar antes de tentar conectar


# Teste 2: Garantir que o erro é levantado se o arquivo não existir
def test_upload_fails_if_file_missing():
    with patch.dict("os.environ", {"AIRFLOW_HOME": "/opt/airflow"}):
        with pytest.raises(FileNotFoundError):
            upload_to_oci("non_existent_file.parquet", "test.parquet")


# Teste 3: Simular falha de conexão com a OCI
@patch("src.utils.oci_utils.get_object_storage_client")
def test_upload_critical_error(mock_client):
    #  mock a lançar um erro
    mock_client.side_effect = Exception("OCI Connection Failed")

    with patch.dict("os.environ", {"AIRFLOW_HOME": "/opt/airflow"}):
        with patch("os.path.exists", return_value=True):
            with pytest.raises(Exception, match="OCI Connection Failed"):
                upload_to_oci("existing_file.parquet", "test.parquet")
