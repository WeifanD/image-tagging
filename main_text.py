from sqlalchemy import *
from src.models.TextGeneration import TextGeneration
from jinjasql import JinjaSql
import os
import re
import random
import numpy as np

handler = TextGeneration()
universe_list = handler.get_universe()

for universe_id in universe_list:
	handler.update_content(universe_id)