#this file used to start and stop the Cloud Functions and the scheduler when I was using managed services instead of VM 

from google.cloud import scheduler_v1
import os
import sys
import time

# Set the path to the service account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'weather', 'key.json')

def deploy_prediction_function(project_id='nico-playground-384514', location_id='europe-west2'):
    """Deploys the prediction collection Cloud Function"""
    print("Deploying prediction collection function...")
    
    # Get the absolute path to the cloud_functions directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one directory since we're in cloud_functions
    parent_dir = os.path.dirname(current_dir)
    source_dir = os.path.join(parent_dir, 'cloud_functions')
    
    print(f"Deploying from source directory: {source_dir}")
    
    if not os.path.exists(source_dir):
        print(f"Error: Source directory not found at {source_dir}")
        return False
        
    if not os.path.exists(os.path.join(source_dir, 'main.py')):
        print(f"Error: main.py not found in {source_dir}")
        return False

    # First, ensure any existing function is deleted
    delete_command = f"""
    gcloud functions delete collect_predictions \
    --region {location_id} \
    --quiet
    """
    os.system(delete_command)
    
    # Wait a moment for the deletion to complete
    time.sleep(10)

    deploy_command = f"""
    gcloud functions deploy collect_predictions \
    --gen2 \
    --runtime python39 \
    --trigger-http \
    --region {location_id} \
    --source "{source_dir}" \
    --entry-point collect_predictions \
    --allow-unauthenticated \
    --service-account {project_id}@appspot.gserviceaccount.com \
    --build-service-account projects/{project_id}/serviceAccounts/{project_id}@appspot.gserviceaccount.com
    """
    
    print(f"Running command: {deploy_command}")
    result = os.system(deploy_command)
    if result == 0:
        print("Function deployed successfully")
        return True
    else:
        print("Error deploying function")
        return False

def setup_scheduler(project_id='nico-playground-384514', location_id='europe-west2'):
    """Sets up the Cloud Scheduler job to trigger the function every minute"""
    print("Setting up scheduler...")
    
    function_url = f"https://{location_id}-{project_id}.cloudfunctions.net/collect_predictions"
    
    # Create scheduler job using gcloud command
    scheduler_command = f"""
    gcloud scheduler jobs create http collect-predictions-job \
    --schedule="*/1 * * * *" \
    --uri="{function_url}" \
    --http-method=POST \
    --location={location_id} \
    --oidc-service-account-email={project_id}@appspot.gserviceaccount.com \
    --oidc-token-audience={function_url} \
    --time-zone="Europe/London" \
    --attempt-deadline=30s
    """
    
    try:
        # Try to create new job
        result = os.system(scheduler_command)
        if result == 0:
        print("Scheduler job created successfully")
            return True
        else:
            print("Error creating scheduler job")
            return False
    except Exception as e:
            print(f"Error setting up scheduler: {str(e)}")
            return False

def delete_prediction_function(project_id='nico-playground-384514', location_id='europe-west2'):
    """Deletes the prediction collection Cloud Function"""
    print("Deleting prediction collection function...")
    
    delete_command = f"""
    gcloud functions delete collect_predictions \
    --region {location_id} \
    --quiet
    """
    
    result = os.system(delete_command)
    if result == 0:
        print("Function deleted successfully")
        return True
    else:
        print("Error deleting function")
        return False

def delete_scheduler(project_id='nico-playground-384514', location_id='europe-west2'):
    """Deletes the Cloud Scheduler job"""
    print("Deleting scheduler job...")
    
    client = scheduler_v1.CloudSchedulerClient()
    job_name = f"projects/{project_id}/locations/{location_id}/jobs/collect-predictions-job"
    
    try:
        client.delete_job({"name": job_name})
        print("Scheduler job deleted successfully")
        return True
    except Exception as e:
        print(f"Error deleting scheduler: {str(e)}")
        return False

def start_services():
    """Deploys the function and sets up the scheduler"""
    print("Starting prediction services...")
    if deploy_prediction_function():
        setup_scheduler()
    print("Services startup complete")

def stop_services():
    """Stops all prediction services"""
    print("Stopping prediction services...")
    delete_scheduler()
    delete_prediction_function()
    print("Services stopped")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
        if action == 'start':
            start_services()
        elif action == 'stop':
            stop_services()
        else:
            print("Usage: python manage_prediction_services.py [start|stop]")
    else:
        print("Usage: python manage_prediction_services.py [start|stop]")