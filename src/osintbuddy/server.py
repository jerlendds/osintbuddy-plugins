
from fastapi import FastAPI
import osintbuddy

app = FastAPI(title=f"OSINTBuddy Plugins v{osintbuddy.__version__}")
