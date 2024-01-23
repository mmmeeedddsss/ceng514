# This file specifically created for Codalabs
FROM codalab/default-cpu:latest

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py


RUN python3.8 -m pip install tqdm==4.66.1
RUN python3.8 -m pip install openai==1.9.0
RUN python3.8 -m pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN python3.8 -m pip install --no-cache-dir sentence-transformers


CMD ["/bin/bash"]
