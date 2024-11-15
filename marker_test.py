import os

from marker.convert import convert_single_pdf
from marker.logger import configure_logging
from marker.models import load_all_models
from marker.output import save_markdown



fname = 'hult.pdf'
model_lst = load_all_models()
full_text, images, out_meta = convert_single_pdf(fname, model_lst)

fname = os.path.basename(fname)
subfolder_path = save_markdown('marker-output', fname, full_text, images, out_meta)

print(f"Saved markdown to the {subfolder_path} folder")