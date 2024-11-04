import logging
import ai_agent.utils.configuration as configuration

import ai_agent.api.api as api
import ai_agent.client.client as client
import ai_agent.core.core as core
import ai_agent.server.server as server
import ai_agent.core.index_data as index_job
import subprocess

configuration.configure_logging()

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting {{ project-prefix }}-{{ app-name }} Ai Agent")

    api.execute()
    client.execute()
    core.execute()
    subprocess.run(["python", "-m", "streamlit", "run", "ai_agent/core/app.py","--server.port={{ chatbot-port }}","--server.address=0.0.0.0", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"])
    server.execute()
    

if __name__ == '__main__':
    main()
