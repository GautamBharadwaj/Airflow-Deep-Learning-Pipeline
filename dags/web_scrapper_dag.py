from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from webscrapper import download_google_images
from object_detection import GenerateObjectEmbedding

def scrape_images(search_term: str = 'dog', max_images: int = 10):
    download_google_images(search_term, max_images)

def generate_embeddings(dataset_path, embeddings_output_path):
    embedding_generator = GenerateObjectEmbedding(dataset_path, embeddings_output_path)
    embedding_generator.genObjectEmbedding()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'image_scraping_and_embedding_pipeline_with_api',
    default_args=default_args,
    description='A pipeline for scraping images, generating embeddings, and serving predictions via API',
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
)

scrape_images_task = PythonOperator(
    task_id='scrape_images',
    python_callable=scrape_images,
    op_kwargs={'search_term': 'dog', 'max_images': 10},
    dag=dag,
)

generate_embeddings_task = PythonOperator(
    task_id='generate_embeddings',
    python_callable=generate_embeddings,
    op_kwargs={
        'dataset_path': '/opt/airflow/images/images_dog',
        'embeddings_output_path': '/opt/airflow/images/object_embeddings.pkl'
    },
    dag=dag,
)

scrape_images_task >> generate_embeddings_task
