# llm-jobs

## Progress Report
1. Installed all the dependencies I needed in the HPC. First loaded [conda](https://icl-rcs-user-guide.readthedocs.io/en/latest/hpc/applications/guides/conda/), then used it to install [langchain](https://github.com/conda-forge/langchain-community-feedstock), [ollama](https://github.com/conda-forge/ollama-feedstock), pandas etc.
2. [In `old-code`] Tried running `pneumonia-trial-1.py`, didn't even work because ollama [naturally binds](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-can-i-expose-ollama-on-my-network) to port 127.0.0.1 port 11434 by default but when running on a new cluster, this needed to be specified in the code. Otherwise the code went all the way through the main and then got stuck at the llm.invoke() call.

> GOT CODE RUNNING ON CLUSTER, JUST 3x SLOWER:
3. [In `old-code`] Used `test-invoke.py` to debug and realised how base_url gets specified. Then got pneumonia detection code working `pneumonia-trial-2.py`. At this point, to simply run this code I need to execute the following commands:

```
ssh an1321@login.hpc.imperial.ac.uk
module load anaconda3/personal
ollama serve &
python3 pneumonia-trial-2.py
```

Once I had it running using just `python3 pneumonia-trial-2.py`, I realised that the performance is much slower. The trends are similar (the cluster is 3x slower).

```
Performance on cluster
Patient Number: 0, HADM ID: 20015730, Discharge Text Length: 24729, Pneumonia Detected: Yes, Time Taken: 179
Patient Number: 1, HADM ID: 20022465, Discharge Text Length: 9219, Pneumonia Detected: No, Time Taken: 71
Patient Number: 2, HADM ID: 20025172, Discharge Text Length: 29166, Pneumonia Detected: Yes, Time Taken: 182
Patient Number: 3, HADM ID: 20031665, Discharge Text Length: 9779, Pneumonia Detected: No, Time Taken: 69
Patient Number: 4, HADM ID: 20038242, Discharge Text Length: 10198, Pneumonia Detected: Yes, Time Taken: 75
Patient Number: 5, HADM ID: 20050336, Discharge Text Length: 16691, Pneumonia Detected: Yes, Time Taken: 126
Patient Number: 6, HADM ID: 20060499, Discharge Text Length: 7772, Pneumonia Detected: Yes, Time Taken: 58
Patient Number: 7, HADM ID: 20067108, Discharge Text Length: 3581, Pneumonia Detected: No, Time Taken: 29
...

Performance on local computer
Patient Number: 0, HADM ID: 20015730, Discharge Text Length: 24729, Pneumonia Detected: Yes, Time Taken: 60
Patient Number: 1, HADM ID: 20022465, Discharge Text Length: 9219, Pneumonia Detected: Yes, Time Taken: 23
Patient Number: 2, HADM ID: 20025172, Discharge Text Length: 29166, Pneumonia Detected: Yes, Time Taken: 63
Patient Number: 3, HADM ID: 20031665, Discharge Text Length: 9779, Pneumonia Detected: No, Time Taken: 23
Patient Number: 4, HADM ID: 20038242, Discharge Text Length: 10198, Pneumonia Detected: Yes, Time Taken: 25
Patient Number: 5, HADM ID: 20050336, Discharge Text Length: 16691, Pneumonia Detected: Yes, Time Taken: 42
Patient Number: 6, HADM ID: 20060499, Discharge Text Length: 7772, Pneumonia Detected: Yes, Time Taken: 20
Patient Number: 7, HADM ID: 20067108, Discharge Text Length: 3581, Pneumonia Detected: No, Time Taken: 10
...
```

4. I tried setting up a job, `job-1.sh`, and running `job-trial-1.py` (identical to `pneumonia-trial-2.py`).