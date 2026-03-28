from playwright.sync_api import Page, expect
import subprocess
import time


def test_streamlit_ui_flow(page: Page):
    # Start Streamlit in the background for testing
    process = subprocess.Popen(["streamlit", "run", "ui/app.py", "--server.headless", "true"])

    # Increased wait time to allow the Random Forest model to train its 10,000 rows on initial boot
    time.sleep(5)

    try:
        page.goto("http://localhost:8501")

        # 1. Verify App loads correctly (Added a timeout to wait for the UI to fully render)
        expect(page.locator("text=Third Party / Blockchain MMF Trading DApp")).to_be_visible(timeout=15000)

        # 2. Verify AI Model Health Metrics in Sidebar
        expect(page.locator("text=🧠 AI Model Health")).to_be_visible()
        expect(page.locator("text=Training Accuracy")).to_be_visible()
        expect(page.locator("text=Precision Score")).to_be_visible()

        # 3. Verify AI recommendation rendered
        expect(page.locator("text=AI Asset Recommendations")).to_be_visible()
        expect(page.locator("text=Top Pick:")).to_be_visible()

        # 4. Verify Visualizations
        # Streamlit wraps Plotly graphs in a container with the class 'stPlotlyChart'.
        # We expect exactly 2 charts: The Speedometer (Gauge) and the Bar Chart.
        expect(page.locator(".stPlotlyChart")).to_have_count(2)

        # 5. Simulate a click on the DvP swap button
        page.locator("text=Initiate Delivery vs Payment").click()

        # 6. Verify Success Message appears
        expect(page.locator("text=DvP Locked: Swapped")).to_be_visible()

    finally:
        process.terminate()  # Ensure the background server is safely killed