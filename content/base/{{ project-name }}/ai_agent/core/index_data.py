import os
import time
import pinecone
from llama_index import Document, VectorStoreIndex, ServiceContext, StorageContext
from llama_index.vector_stores import PineconeVectorStore
from pinecone.core.client.exceptions import NotFoundException
from llama_index.embeddings import OpenAIEmbedding
from llama_index.embeddings import HuggingFaceEmbedding
import boto3
import awswrangler as wr
import logging
from ai_agent.core.config import SOLUTION_PREFIX, SEGMENTS, PINECONE_ENV, PINECONE_API_KEY, PINECONE_INDEX_METRIC, \
    EMBEDDING_MODEL_DIMENSIONS, SOLUTION_NAME

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def create_pinecone_index(documents, index_name, pinecone_api_key, pinecone_env, embedding_model_name,
                          embedding_model_dimensions, index_metric):
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

    if index_name not in pinecone.list_indexes():
        # pinecone.create_index(index_name, metric=index_metric, pod_type="p1")
        pinecone.create_index(index_name, dimension=embedding_model_dimensions, metric=index_metric, pod_type="p1")

    pinecone_index = pinecone.Index(index_name)
    time.sleep(5)
    # try:
    #     pinecone_index.delete(delete_all=True)
    # except NotFoundException:
    #     logger.info("Pinecone index not found. Skipping deletion.")

    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    logger.info("loading HF model")
    embed_model = HuggingFaceEmbedding(embedding_model_name)
    logger.info("completed loading HF model")

    # service_context = ServiceContext.from_defaults(embed_model=f"local:{embed_model}", chunk_size=4096 * 2)

    service_context = ServiceContext.from_defaults(embed_model=embed_model, chunk_size=4096 * 2)
    # service_context = ServiceContext.from_defaults(embed_model=embedding_model_name, chunk_size=4096 * 2)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context,
                                            show_progress=True)
    return index


def init_df_index(df, df_column, index_name):
    data_array = df[df_column].to_numpy().flatten()
    documents = [Document(text=str(data)) for data in data_array]
    embedding_model_name = "BAAI/bge-small-en-v1.5"
    embedding_model_dimensions = 384
    # embedding_model_name = OpenAIEmbedding(model="text-embedding-3-small")
    # embedding_model_dimensions = 1536

    create_pinecone_index(documents, index_name, PINECONE_API_KEY, PINECONE_ENV, embedding_model_name,
                          embedding_model_dimensions, PINECONE_INDEX_METRIC)


def main():
    logger.info("Inside Index Data")
    os.environ["OPENAI_API_KEY"] = ''
    # boto3.setup_default_session(region_name="us-west-2")
    # boto3.setup_default_session(profile_name='prod')
    sts = boto3.client('sts')
    response = sts.assume_role(
        RoleArn="arn:aws:iam::288163945356:role/GlueDataConsumer",
        RoleSessionName="glue-session"
    )
    boto3.setup_default_session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                                aws_session_token=response['Credentials']['SessionToken'], region_name="us-west-2")

    for segment_name in SEGMENTS:
        logger.info(f"Fetching Segment --> {segment_name} ")
        if segment_name == 'all-segments':
            query = f'''
                WITH twitter_data as(
                    SELECT source_name,
                        source_data,
                        solution_name
                    FROM "social"."twitter"
                    where solution_name = '{SOLUTION_NAME}'
                ),
                talkwalker_data as(
                    SELECT source_name,
                        source_data,
                        solution_name
                    FROM "social"."talkwalker_iceberg"
                    where solution_name = '{SOLUTION_NAME}'
                )
                SELECT source_data body
                FROM twitter_data
                UNION ALL
                SELECT source_data body
                FROM talkwalker_data
                limit 100
            '''
        else:
            query = f"SELECT body FROM social.talkwalker_segmented where contains(interests,'{segment_name}') limit 100"
        df = wr.athena.read_sql_query(query, database='social', data_source='social', ctas_approach=False)
        logger.info(f"{segment_name} Segment Name-> {segment_name}")
        logger.info(f"{segment_name} Segment Size-> {df.shape}")
        logger.info(f"{segment_name} Segment Top5-> {df.head()}")
        init_df_index(df, "body", f"{SOLUTION_PREFIX}-agent-{segment_name.lower()}")
    logger.info("Completed Index job")


if __name__ == "__main__":
    main()
