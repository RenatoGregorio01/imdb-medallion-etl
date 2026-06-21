import oci
import os
from loguru import logger

def get_object_storage_client():
    """
    Cria e retorna um cliente OCI Object Storage autenticado.
    """
    default_local_path = os.path.expanduser("~/.oci/config")
    config_path = os.getenv("OCI_CONFIG_FILE", default_local_path)
    
    if not os.path.exists(config_path):
        logger.error(f"Arquivo de configuração OCI não encontrado em: {config_path}")
        raise FileNotFoundError(f"Configuração OCI ausente em {config_path}")
        
    config = oci.config.from_file(file_location=config_path)
    return oci.object_storage.ObjectStorageClient(config)

def get_namespace_safely(client: oci.object_storage.ObjectStorageClient):
    """
    Obtém o namespace da tenancy de forma segura.
    """
    response = client.get_namespace()
    if not response or not response.data:
        logger.error("Falha ao obter o namespace da OCI: A resposta retornou vazia.")
        raise ValueError("Namespace da OCI indisponível.")
    return response.data

def upload_to_oci(file_path: str, object_name: str):
    """
    Realiza o upload para OCI apenas se estiver rodando dentro do Airflow.
    """
    # Verifica se estamos no ambiente do Airflow para permitir o upload
    if not os.getenv("AIRFLOW_HOME"):
        logger.info("[SKIP] Ambiente local detectado: Upload de {} ignorado.", object_name)
        return

    try:
        # Verifica se o arquivo local existe antes de tentar abrir
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo local não encontrado: {file_path}")

        client = get_object_storage_client()
        namespace = get_namespace_safely(client)
        bucket_name = "imdb-medallion-etl"
        
        logger.info(f"Iniciando upload de {file_path} para {bucket_name}/{object_name}...")
        
        with open(file_path, "rb") as f:
            client.put_object(
                namespace_name=namespace,
                bucket_name=bucket_name,
                object_name=object_name,
                put_object_body=f
            )
            
        logger.success(f"Upload realizado com sucesso: {object_name}")
        
    except Exception as e:
        logger.error(f"Falha crítica ao subir arquivo para OCI: {e}")
        raise
    