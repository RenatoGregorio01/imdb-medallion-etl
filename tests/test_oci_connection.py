import oci
import os
import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>",
)


def test_oci_connection():
    """
    Testa a conexão com o OCI Object Storage e verifica se o bucket
    'imdb-medallion-etl' está acessível.
    """
    try:
        # Tenta carregar a configuração. Se a variável OCI_CONFIG_FILE estiver definida, usa ela.
        config_path = os.getenv("OCI_CONFIG_FILE", os.path.expanduser("~/.oci/config"))

        if not os.path.exists(config_path):
            logger.error(f"Arquivo de configuração não encontrado em: {config_path}")
            return

        config = oci.config.from_file(file_location=config_path)
        object_storage = oci.object_storage.ObjectStorageClient(config)

        # Obtém o namespace de forma segura
        response = object_storage.get_namespace()
        if response is None or response.data is None:
            logger.error("Falha ao obter o namespace da OCI: A resposta veio vazia.")
            return

        namespace = response.data
        logger.info(f"Conexão autenticada! Namespace: {namespace}")

        # Lista os buckets
        buckets_response = object_storage.list_buckets(
            namespace_name=namespace, compartment_id=config["tenancy"]
        )

        if buckets_response is None or buckets_response.data is None:
            logger.error("Falha ao listar buckets: A resposta do OCI está vazia.")
            return

        buckets = buckets_response.data
        bucket_name_to_find = "imdb-medallion-etl"
        bucket_exists = any(b.name == bucket_name_to_find for b in buckets)

        if bucket_exists:
            logger.success(f"Sucesso! Bucket '{bucket_name_to_find}' encontrado.")
        else:
            logger.warning(
                f"Conectado, mas o bucket '{bucket_name_to_find}' não foi encontrado."
            )

    except Exception as e:
        logger.error(f"Erro crítico na conexão com OCI: {e}")


if __name__ == "__main__":
    test_oci_connection()
